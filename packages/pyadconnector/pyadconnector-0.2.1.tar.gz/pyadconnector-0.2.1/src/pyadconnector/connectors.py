from typing import Any, Literal

import ldap
from ldap.ldapobject import LDAPObject

from . import utils
from .exceptions import ADError, UserDoesNotFound
from .models import ADGroup, ADGroups, ADUser, ADUsers, SearchRawOut, ADObject
from .settings import ActiveDirectorySettings

LdapScope = Literal["onelevel", "base", "subtree"]


class ActiveDirectoryConnector:
    def __init__(self, settings: ActiveDirectorySettings):
        self.connection: LDAPObject | None = None
        self.settings = settings

    @classmethod
    def get_scope(cls, scope: LdapScope) -> int:
        # scope: one_level [SCOPE_ONELEVEL] base [SCOPE_BASE] subtree [SCOPE_SUBTREE]
        ldap_scope = getattr(ldap, f"SCOPE_{scope.upper()}", ldap.SCOPE_ONELEVEL)  # pyright: ignore
        return ldap_scope

    def bind(self, ldap_options: dict[Any, Any] | None = None):
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)  # pyright: ignore
        if ldap_options:
            for (
                option,
                value,
            ) in ldap_options.items():
                ldap.set_option(option, value)

        self.connection: LDAPObject = ldap.initialize(
            str(self.settings.domain_controllers.primary_uri)
        )
        self.connection.start_tls_s()
        self.connection.simple_bind_s(self.settings.bind_dn, self.settings.bind_password)

    def search(
        self,
        to_search: str,
        base_dn: str = "",
        scope: LdapScope | None = None,
        attributes: list | None = None,
    ) -> SearchRawOut:
        base_dn = base_dn or self.settings.base_dn
        scope = scope if scope else "onelevel"
        results = self.connection.search_s(
            base_dn, self.get_scope(scope=scope), to_search, attributes
        )
        return SearchRawOut(results)

    def list_objects(
        self,
        out_object: ADObject,
        to_search: str | None = None,
        base_dn: str = "",
        scope: LdapScope | None = None,
        attributes: list[str] | None = None,
    ) -> ADUsers | ADGroups:
        attributes = attributes or out_object.attributes()
        if "sAMAccountName" not in attributes:
            attributes += ["sAMAccountName"]

        ADObjectOut = None
        if out_object == ADUser:
            to_search = utils.FILTER_SEARCH_USERS
            ADObjectOut = ADUsers
        elif out_object == ADGroup:
            to_search = utils.FILTER_SEARCH_GROUPS
            ADObjectOut = ADGroups
        else:
            raise Exception(f"Object class {out_object} not supported")

        if not to_search:
            raise Exception("Specificare filter search")
        try:
            results = self.search(
                to_search=to_search,
                base_dn=base_dn,
                scope=scope,
                attributes=attributes,
            )
        except ldap.NO_SUCH_OBJECT:
            return ADObjectOut()
        except ldap.LDAPError as exc:
            raise ADError(ldap_error=exc) from exc
        objects = {data[1]["sAMAccountName"][0].lower(): out_object(**data[1]) for data in results}
        return ADObjectOut(objects)

    def list_users(
        self, base_dn: str = "", scope: LdapScope | None = None, attributes: list[str] | None = None
    ) -> ADUsers:
        return self.list_objects(
            out_object=ADUser, base_dn=base_dn, scope=scope, attributes=attributes
        )

    def list_groups(
        self, base_dn: str = "", scope: LdapScope | None = None, attributes: list[str] | None = None
    ) -> ADUsers:
        return self.list_objects(
            out_object=ADGroup, base_dn=base_dn, scope=scope, attributes=attributes
        )

    def get_user(
        self,
        username: str,
        base_dn: str = "",
        scope: LdapScope | None = None,
        attributes: list | None = None,
    ) -> ADUser:
        to_search = utils.FILTER_SEARCH_USER_BY_SAMACC.format(username=username)
        attributes = attributes or ADUser.attributes()
        try:
            results = self.search(
                to_search=to_search, base_dn=base_dn, scope=scope, attributes=attributes
            )
        except ldap.LDAPError as exc:
            raise ADError(ldap_error=exc) from exc
        if len(results) == 0:
            raise UserDoesNotFound(f"User '{username}' not found in '{base_dn}'")
        return ADUser(**results[0][1])

    def get_domain_data(self, base_dn: str = "", attributes=None) -> SearchRawOut:
        base_dn = base_dn or self.settings.base_dn
        try:
            return self.search(
                to_search="(objectCategory=domain)",
                base_dn=base_dn,
                scope="subtree",  # pylint: disable=no-member # pyright: ignore
                attributes=attributes,
            )
        except ldap.LDAPError as exc:
            raise ADError(ldap_error=exc) from exc

    def disable_user(self, user_dn: str) -> None:
        mod_list_attrs = [(ldap.MOD_REPLACE, "userAccountControl", b"514")]  # pyright: ignore
        res = self.connection.modify_s(user_dn, mod_list_attrs)
        return res

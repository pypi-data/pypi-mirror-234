class ADError(Exception):
    def __init__(self, ldap_error: Exception | None = None):
        super().__init__(ldap_error)
        self.ldap_error = ldap_error


class ObjectDoesNotFound(ADError):
    pass


class UserDoesNotFound(ObjectDoesNotFound):
    pass

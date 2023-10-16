from pydantic import AnyUrl, BaseModel, ConfigDict
from pydantic_settings import BaseSettings


class DomainControllersSettings(BaseModel):
    primary_uri: AnyUrl
    secondary_uri: AnyUrl | None = None


class UsersSettings(BaseModel):
    dns: list[str] | None = None


class ActiveDirectorySettings(BaseSettings):
    base_dn: str = ""
    bind_dn: str = ""
    bind_password: str = ""
    domain_controllers: DomainControllersSettings
    users: UsersSettings | None = None


class IntegrationTestData(BaseModel):
    model_config = ConfigDict(extra="allow")

    base_dn: str | None = None
    attributes: list[dict[str, str]] | None = None


class IntegrationTestsSections(BaseModel):
    model_config = ConfigDict(extra="allow")

    users: IntegrationTestData | None = None
    get_user: IntegrationTestData | None = None
    list_users: IntegrationTestData | None = None
    list_groups: IntegrationTestData | None = None

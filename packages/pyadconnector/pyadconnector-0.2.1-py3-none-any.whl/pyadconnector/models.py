from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    RootModel,
    field_validator,
)
from pydantic.alias_generators import to_camel
from .utils import sid_to_str
from .enums import AccountControlEnum


class ADObject(BaseModel):
    model_config = ConfigDict(
        extra="allow", alias_generator=to_camel, validate_assignment=True, populate_by_name=True
    )

    cn: str | None = None
    distinguished_name: str | None = None
    object_sid: str | None = None
    samaccount_name: str | None = Field(None, alias="sAMAccountName")

    @classmethod
    def attributes(cls) -> list:
        schema = cls.model_json_schema()
        return list(schema["properties"].keys())

    @field_validator("object_sid", mode="before")
    def convert_sid(cls, v):
        if isinstance(v, list):
            if len(v) == 1:
                try:
                    return sid_to_str(v[0])
                except Exception as e:
                    raise ValueError(f"Error on covert into sid string [{e}] -> {v[0]}") from e
            else:
                raise ValueError(f"List to validate must be have only one element -> {v}")
        return v


class ADUser(ADObject):
    mail: EmailStr | None = None
    sn: str | None = None
    given_name: str | None = None
    user_account_control: AccountControlEnum | None = None
    member_of: list[str] = []
    user_principal_name: str | None = None

    @field_validator(
        "mail",
        "distinguished_name",
        "cn",
        "sn",
        "given_name",
        "user_account_control",
        "samaccount_name",
        "user_principal_name",
        mode="before",
    )
    def extract_first(cls, v):
        if isinstance(v, list):
            if len(v) == 1:
                return v[0]
            else:
                raise ValueError(f"List to validate must be have only one element -> {v}")
        return v

    def is_active(self) -> bool:
        if self.user_account_control and self.user_account_control == AccountControlEnum.ENABLED:
            return True
        return False


class ADGroup(ADObject):
    instance_type: int | None = None
    member: list[str] = []
    member_of: list[str] = []

    @field_validator(
        "distinguished_name",
        "cn",
        "instance_type",
        "samaccount_name",
        mode="before",
    )
    def extract_first(cls, v):
        if isinstance(v, list):
            if len(v) == 1:
                return v[0]
            else:
                raise ValueError(f"List to validate must be have only one element -> {v}")
        return v


class SearchRawOut(RootModel):
    root: list[tuple[str | None, dict | list]]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item: str | int) -> tuple[str | None, dict]:
        if isinstance(item, int):
            return self.root[item]
        if isinstance(item, str):
            for t in self.root:
                if t[0] == item:
                    return t
        raise IndexError

    def __len__(self):
        return len(self.root)

    def __contains__(self, item):
        if item in [t[0] for t in self.root]:
            return True
        return False


class ADObjects(RootModel):
    root: dict[str, ADObject] = {}

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item) -> ADObject:
        return self.root[item]

    def __contains__(self, item) -> bool:
        if item in self.root:
            return True
        return False

    def __len__(self) -> int:
        return len(self.root.items())


class ADUsers(ADObjects):
    root: dict[str, ADUser] = {}


class ADGroups(ADObjects):
    root: dict[str, ADGroup] = {}

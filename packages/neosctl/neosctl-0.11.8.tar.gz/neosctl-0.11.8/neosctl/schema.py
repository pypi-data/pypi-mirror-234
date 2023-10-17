import configparser
import dataclasses
from typing import Optional, Union

from pydantic import BaseModel


class Auth(BaseModel):
    access_token: str = ""
    expires_in: Optional[int] = None
    refresh_token: str = ""
    refresh_expires_in: Optional[int] = None


class OptionalProfile(BaseModel):
    gateway_api_url: str = ""
    registry_api_url: str = ""
    iam_api_url: str = ""
    storage_api_url: str = ""
    user: str = ""
    access_token: str = ""
    refresh_token: str = ""
    ignore_tls: bool = False
    account: str = ""


class Profile(OptionalProfile):
    gateway_api_url: str
    registry_api_url: str
    iam_api_url: str
    storage_api_url: str
    user: str
    access_token: str
    refresh_token: str
    ignore_tls: bool
    account: str = "root"  # backwards compat default


class Credential(BaseModel):
    access_key_id: str
    secret_access_key: str


@dataclasses.dataclass
class Common:
    gateway_api_url: str
    registry_api_url: str
    iam_api_url: str
    storage_api_url: str
    profile_name: str
    config: configparser.ConfigParser
    credential: configparser.ConfigParser
    profile: Optional[Union[Profile, OptionalProfile]]

    def get_account(self) -> str:
        """Return system account."""
        if self.profile:
            return self.profile.account

        return "root"

    def get_gateway_api_url(self) -> str:
        """Return gateway api url.

        If a user profile is provided and defines a gateway url, return that,
        otherwise or fall back to cli defined default.
        """
        if self.profile and self.profile.gateway_api_url:
            return self.profile.gateway_api_url
        return self.gateway_api_url

    def get_registry_api_url(self) -> str:
        """Return registry api url.

        If a user profile is provided and defines a registry url, return that,
        otherwise or fall back to cli defined default.
        """
        if self.profile and self.profile.registry_api_url:
            return self.profile.registry_api_url
        return self.registry_api_url

    def get_iam_api_url(self) -> str:
        """Return iam api url.

        If a user profile is provided and defines a iam url, return that,
        otherwise or fall back to cli defined default.
        """
        if self.profile and self.profile.iam_api_url:
            return self.profile.iam_api_url
        return self.iam_api_url

    def get_storage_api_url(self) -> str:
        """Return storage api url.

        If a user profile is provided and defines a storage url, return that,
        otherwise or fall back to cli defined default.
        """
        if self.profile and self.profile.storage_api_url:
            return self.profile.storage_api_url
        return self.storage_api_url

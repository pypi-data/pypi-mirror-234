# This file was automatically generated. DO NOT EDIT.
# If you have any remark or suggestion do not hesitate to open an issue.
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from scaleway_core.bridge import (
    Region,
)
from scaleway_core.utils import (
    StrEnumMeta,
)


class ListFoldersRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"

    def __str__(self) -> str:
        return str(self.value)


class ListSecretsRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"
    UPDATED_AT_ASC = "updated_at_asc"
    UPDATED_AT_DESC = "updated_at_desc"

    def __str__(self) -> str:
        return str(self.value)


class Product(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)


class SecretStatus(str, Enum, metaclass=StrEnumMeta):
    READY = "ready"
    LOCKED = "locked"

    def __str__(self) -> str:
        return str(self.value)


class SecretType(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN_SECRET_TYPE = "unknown_secret_type"
    OPAQUE = "opaque"
    CERTIFICATE = "certificate"

    def __str__(self) -> str:
        return str(self.value)


class SecretVersionStatus(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN = "unknown"
    ENABLED = "enabled"
    DISABLED = "disabled"
    DESTROYED = "destroyed"

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class PasswordGenerationParams:
    additional_chars: str
    """
    Additional ascii characters to be included in the alphabet.
    """

    no_digits: bool
    """
    Do not include digits by default in the alphabet.
    """

    no_uppercase_letters: bool
    """
    Do not include upper case letters by default in the alphabet.
    """

    no_lowercase_letters: bool
    """
    Do not include lower case letters by default in the alphabet.
    """

    length: int
    """
    Length of the password to generate (between 1 and 1024).
    """


@dataclass
class Folder:
    path: str
    """
    Location of the folder in the directory structure.
    """

    name: str
    """
    Name of the folder.
    """

    project_id: str
    """
    ID of the Project containing the folder.
    """

    id: str
    """
    ID of the folder.
    """

    created_at: Optional[datetime]
    """
    Date and time of the folder's creation.
    """


@dataclass
class SecretVersion:
    is_latest: bool
    """
    Returns `true` if the version is the latest.
    """

    status: SecretVersionStatus
    """
    * `unknown`: the version is in an invalid state.
* `enabled`: the version is accessible.
* `disabled`: the version is not accessible but can be enabled.
* `destroyed`: the version is permanently deleted. It is not possible to recover it.
    """

    secret_id: str
    """
    ID of the secret.
    """

    revision: int
    """
    The first version of the secret is numbered 1, and all subsequent revisions augment by 1.
    """

    created_at: Optional[datetime]
    """
    Date and time of the version's creation.
    """

    updated_at: Optional[datetime]
    """
    Last update of the version.
    """

    description: Optional[str]
    """
    Description of the version.
    """


@dataclass
class Secret:
    is_managed: bool
    """
    Returns `true` for secrets that are managed by another product.
    """

    type_: SecretType
    """
    See `Secret.Type` enum for description of values.
    """

    version_count: int
    """
    Number of versions for this secret.
    """

    id: str
    """
    ID of the secret.
    """

    path: str
    """
    Location of the secret in the directory structure.
    """

    region: Region
    """
    Region of the secret.
    """

    status: SecretStatus
    """
    * `ready`: the secret can be read, modified and deleted.
* `locked`: no action can be performed on the secret. This status can only be applied and removed by Scaleway.
    """

    name: str
    """
    Name of the secret.
    """

    project_id: str
    """
    ID of the Project containing the secret.
    """

    is_protected: bool
    """
    Returns `true` for protected secrets that cannot be deleted.
    """

    tags: List[str]
    """
    List of the secret's tags.
    """

    description: Optional[str]
    """
    Updated description of the secret.
    """

    updated_at: Optional[datetime]
    """
    Last update of the secret.
    """

    created_at: Optional[datetime]
    """
    Date and time of the secret's creation.
    """


@dataclass
class AccessSecretVersionByNameRequest:
    revision: str
    """
    The first version of the secret is numbered 1, and all subsequent revisions augment by 1. Value can be either:
- a number (the revision number)
- "latest" (the latest revision)
- "latest_enabled" (the latest enabled revision).
    """

    secret_name: str
    """
    Name of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    project_id: Optional[str]
    """
    (Optional.) If not specified, Secret Manager will look for the secret version in all Projects.
    """


@dataclass
class AccessSecretVersionRequest:
    revision: str
    """
    The first version of the secret is numbered 1, and all subsequent revisions augment by 1. Value can be either:
- a number (the revision number)
- "latest" (the latest revision)
- "latest_enabled" (the latest enabled revision).
    """

    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class AccessSecretVersionResponse:
    data: str
    """
    The base64-encoded secret payload of the version.
    """

    revision: int
    """
    The first version of the secret is numbered 1, and all subsequent revisions augment by 1.
    """

    secret_id: str
    """
    ID of the secret.
    """

    data_crc32: Optional[int]
    """
    This field is only available if a CRC32 was supplied during the creation of the version.
    """


@dataclass
class AddSecretOwnerRequest:
    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    product_name: Optional[str]
    """
    (Deprecated: use `product` field) Name of the product to add.
    """

    product: Optional[Product]
    """
    See `Product` enum for description of values.
    """


@dataclass
class CreateFolderRequest:
    name: str
    """
    Name of the folder.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    project_id: Optional[str]
    """
    ID of the Project containing the folder.
    """

    path: Optional[str]
    """
    (Optional.) Location of the folder in the directory structure. If not specified, the path is `/`.
    """


@dataclass
class CreateSecretRequest:
    name: str
    """
    Name of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    project_id: Optional[str]
    """
    ID of the Project containing the secret.
    """

    tags: Optional[List[str]]
    """
    List of the secret's tags.
    """

    description: Optional[str]
    """
    Description of the secret.
    """

    type_: Optional[SecretType]
    """
    (Optional.) See `Secret.Type` enum for description of values. If not specified, the type is `Opaque`.
    """

    path: Optional[str]
    """
    (Optional.) Location of the secret in the directory structure. If not specified, the path is `/`.
    """


@dataclass
class CreateSecretVersionRequest:
    data: str
    """
    The base64-encoded secret payload of the version.
    """

    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    description: Optional[str]
    """
    Description of the version.
    """

    disable_previous: Optional[bool]
    """
    (Optional.) If there is no previous version or if the previous version was already disabled, does nothing.
    """

    password_generation: Optional[PasswordGenerationParams]
    """
    (Optional.) If specified, a random password will be generated. The `data` and `data_crc32` fields must be empty. By default, the generator will use upper and lower case letters, and digits. This behavior can be tuned using the generation parameters.
    """

    data_crc32: Optional[int]
    """
    If specified, Secret Manager will verify the integrity of the data received against the given CRC32 checksum. An error is returned if the CRC32 does not match. If, however, the CRC32 matches, it will be stored and returned along with the SecretVersion on future access requests.
    """


@dataclass
class DeleteFolderRequest:
    folder_id: str
    """
    ID of the folder.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class DeleteSecretRequest:
    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class DestroySecretVersionRequest:
    revision: str
    """
    The first version of the secret is numbered 1, and all subsequent revisions augment by 1. Value can be either:
- a number (the revision number)
- "latest" (the latest revision)
- "latest_enabled" (the latest enabled revision).
    """

    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class DisableSecretVersionRequest:
    revision: str
    """
    The first version of the secret is numbered 1, and all subsequent revisions augment by 1. Value can be either:
- a number (the revision number)
- "latest" (the latest revision)
- "latest_enabled" (the latest enabled revision).
    """

    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class EnableSecretVersionRequest:
    revision: str
    """
    The first version of the secret is numbered 1, and all subsequent revisions augment by 1. Value can be either:
- a number (the revision number)
- "latest" (the latest revision)
- "latest_enabled" (the latest enabled revision).
    """

    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class GeneratePasswordRequest:
    length: int
    """
    Length of the password to generate (between 1 and 1024 characters).
    """

    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    description: Optional[str]
    """
    Description of the version.
    """

    disable_previous: Optional[bool]
    """
    This has no effect if there is no previous version or if the previous version was already disabled.
    """

    no_lowercase_letters: Optional[bool]
    """
    (Optional.) Exclude lower case letters by default in the password character set.
    """

    no_uppercase_letters: Optional[bool]
    """
    (Optional.) Exclude upper case letters by default in the password character set.
    """

    no_digits: Optional[bool]
    """
    (Optional.) Exclude digits by default in the password character set.
    """

    additional_chars: Optional[str]
    """
    (Optional.) Additional ASCII characters to be included in the password character set.
    """


@dataclass
class GetSecretByNameRequest:
    secret_name: str
    """
    Name of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    project_id: Optional[str]
    """
    (Optional.) If not specified, Secret Manager will look for the secret in all Projects.
    """


@dataclass
class GetSecretRequest:
    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class GetSecretVersionByNameRequest:
    revision: str
    """
    The first version of the secret is numbered 1, and all subsequent revisions augment by 1. Value can be either:
- a number (the revision number)
- "latest" (the latest revision)
- "latest_enabled" (the latest enabled revision).
    """

    secret_name: str
    """
    Name of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    project_id: Optional[str]
    """
    (Optional.) If not specified, Secret Manager will look for the secret version in all Projects.
    """


@dataclass
class GetSecretVersionRequest:
    revision: str
    """
    The first version of the secret is numbered 1, and all subsequent revisions augment by 1. Value can be either:
- a number (the revision number)
- "latest" (the latest revision)
- "latest_enabled" (the latest enabled revision).
    """

    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class ListFoldersRequest:
    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    project_id: Optional[str]
    """
    Filter by Project ID (optional).
    """

    path: Optional[str]
    """
    Filter by path (optional).
    """

    page: Optional[int]

    page_size: Optional[int]

    order_by: Optional[ListFoldersRequestOrderBy]


@dataclass
class ListFoldersResponse:
    total_count: int
    """
    Count of all folders matching the requested criteria.
    """

    folders: List[Folder]
    """
    List of folders.
    """


@dataclass
class ListSecretVersionsByNameRequest:
    secret_name: str
    """
    Name of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    page: Optional[int]

    page_size: Optional[int]

    status: Optional[List[SecretVersionStatus]]
    """
    Filter results by status.
    """

    project_id: Optional[str]
    """
    (Optional.) If not specified, Secret Manager will look for the secret in all Projects.
    """


@dataclass
class ListSecretVersionsRequest:
    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    page: Optional[int]

    page_size: Optional[int]

    status: Optional[List[SecretVersionStatus]]
    """
    Filter results by status.
    """


@dataclass
class ListSecretVersionsResponse:
    total_count: int
    """
    Number of versions.
    """

    versions: List[SecretVersion]
    """
    Single page of versions.
    """


@dataclass
class ListSecretsRequest:
    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    organization_id: Optional[str]
    """
    Filter by Organization ID (optional).
    """

    project_id: Optional[str]
    """
    Filter by Project ID (optional).
    """

    order_by: Optional[ListSecretsRequestOrderBy]

    page: Optional[int]

    page_size: Optional[int]

    tags: Optional[List[str]]
    """
    List of tags to filter on (optional).
    """

    name: Optional[str]
    """
    Filter by secret name (optional).
    """

    is_managed: Optional[bool]
    """
    Filter by managed / not managed (optional).
    """

    path: Optional[str]
    """
    Filter by path (optional).
    """


@dataclass
class ListSecretsResponse:
    total_count: int
    """
    Count of all secrets matching the requested criteria.
    """

    secrets: List[Secret]
    """
    Single page of secrets matching the requested criteria.
    """


@dataclass
class ListTagsRequest:
    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    project_id: Optional[str]
    """
    (Optional.) If not specified, Secret Manager will look for tags in all Projects.
    """

    page: Optional[int]

    page_size: Optional[int]


@dataclass
class ListTagsResponse:
    total_count: int
    """
    Count of all tags matching the requested criteria.
    """

    tags: List[str]
    """
    List of tags.
    """


@dataclass
class ProtectSecretRequest:
    secret_id: str
    """
    ID of the secret to protect.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class UnprotectSecretRequest:
    secret_id: str
    """
    ID of the secret to unprotect.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class UpdateSecretRequest:
    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    name: Optional[str]
    """
    Secret's updated name (optional).
    """

    tags: Optional[List[str]]
    """
    Secret's updated list of tags (optional).
    """

    description: Optional[str]
    """
    Description of the secret.
    """

    path: Optional[str]
    """
    (Optional.) Location of the folder in the directory structure. If not specified, the path is `/`.
    """


@dataclass
class UpdateSecretVersionRequest:
    revision: str
    """
    The first version of the secret is numbered 1, and all subsequent revisions augment by 1. Value can be either:
- a number (the revision number)
- "latest" (the latest revision)
- "latest_enabled" (the latest enabled revision).
    """

    secret_id: str
    """
    ID of the secret.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    description: Optional[str]
    """
    Description of the version.
    """

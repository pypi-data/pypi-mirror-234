# This file was automatically generated. DO NOT EDIT.
# If you have any remark or suggestion do not hesitate to open an issue.
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from scaleway_core.utils import (
    StrEnumMeta,
)


class BearerType(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN_BEARER_TYPE = "unknown_bearer_type"
    USER = "user"
    APPLICATION = "application"

    def __str__(self) -> str:
        return str(self.value)


class ListAPIKeysRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"
    UPDATED_AT_ASC = "updated_at_asc"
    UPDATED_AT_DESC = "updated_at_desc"
    EXPIRES_AT_ASC = "expires_at_asc"
    EXPIRES_AT_DESC = "expires_at_desc"
    ACCESS_KEY_ASC = "access_key_asc"
    ACCESS_KEY_DESC = "access_key_desc"

    def __str__(self) -> str:
        return str(self.value)


class ListApplicationsRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"
    UPDATED_AT_ASC = "updated_at_asc"
    UPDATED_AT_DESC = "updated_at_desc"
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"

    def __str__(self) -> str:
        return str(self.value)


class ListGroupsRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"
    UPDATED_AT_ASC = "updated_at_asc"
    UPDATED_AT_DESC = "updated_at_desc"
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"

    def __str__(self) -> str:
        return str(self.value)


class ListJWTsRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"
    UPDATED_AT_ASC = "updated_at_asc"
    UPDATED_AT_DESC = "updated_at_desc"

    def __str__(self) -> str:
        return str(self.value)


class ListPermissionSetsRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"

    def __str__(self) -> str:
        return str(self.value)


class ListPoliciesRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    POLICY_NAME_ASC = "policy_name_asc"
    POLICY_NAME_DESC = "policy_name_desc"
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"

    def __str__(self) -> str:
        return str(self.value)


class ListQuotaRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"

    def __str__(self) -> str:
        return str(self.value)


class ListSSHKeysRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"
    UPDATED_AT_ASC = "updated_at_asc"
    UPDATED_AT_DESC = "updated_at_desc"
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"

    def __str__(self) -> str:
        return str(self.value)


class ListUsersRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"
    UPDATED_AT_ASC = "updated_at_asc"
    UPDATED_AT_DESC = "updated_at_desc"
    EMAIL_ASC = "email_asc"
    EMAIL_DESC = "email_desc"
    LAST_LOGIN_ASC = "last_login_asc"
    LAST_LOGIN_DESC = "last_login_desc"

    def __str__(self) -> str:
        return str(self.value)


class PermissionSetScopeType(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN_SCOPE_TYPE = "unknown_scope_type"
    PROJECTS = "projects"
    ORGANIZATION = "organization"
    ACCOUNT_ROOT_USER = "account_root_user"

    def __str__(self) -> str:
        return str(self.value)


class UserStatus(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN_STATUS = "unknown_status"
    INVITATION_PENDING = "invitation_pending"
    ACTIVATED = "activated"

    def __str__(self) -> str:
        return str(self.value)


class UserType(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN_TYPE = "unknown_type"
    GUEST = "guest"
    OWNER = "owner"

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class RuleSpecs:
    permission_set_names: Optional[List[str]]
    """
    Names of permission sets bound to the rule.
    """

    project_ids: Optional[List[str]]

    organization_id: Optional[str]


@dataclass
class JWT:
    user_agent: str
    """
    User-agent used during the creation of the JWT.
    """

    ip: str
    """
    IP address used during the creation of the JWT.
    """

    audience_id: str
    """
    ID of the user targeted by the JWT.
    """

    issuer_id: str
    """
    ID of the user who issued the JWT.
    """

    jti: str
    """
    JWT ID.
    """

    created_at: Optional[datetime]
    """
    Creation date of the JWT.
    """

    updated_at: Optional[datetime]
    """
    Last update date of the JWT.
    """

    expires_at: Optional[datetime]
    """
    Expiration date of the JWT.
    """


@dataclass
class APIKey:
    creation_ip: str
    """
    IP address of the device that created the API key.
    """

    editable: bool
    """
    Defines whether or not the API key is editable.
    """

    default_project_id: str
    """
    Default Project ID specified for this API key.
    """

    description: str
    """
    Description of API key.
    """

    access_key: str
    """
    Access key of the API key.
    """

    secret_key: Optional[str]
    """
    Secret key of the API Key.
    """

    created_at: Optional[datetime]
    """
    Date and time of API key creation.
    """

    updated_at: Optional[datetime]
    """
    Date and time of last API key update.
    """

    expires_at: Optional[datetime]
    """
    Date and time of API key expiration.
    """

    application_id: Optional[str]

    user_id: Optional[str]


@dataclass
class Application:
    nb_api_keys: int
    """
    Number of API keys attributed to the application.
    """

    editable: bool
    """
    Defines whether or not the application is editable.
    """

    organization_id: str
    """
    ID of the Organization.
    """

    description: str
    """
    Description of the application.
    """

    name: str
    """
    Name of the application.
    """

    id: str
    """
    ID of the application.
    """

    created_at: Optional[datetime]
    """
    Date and time application was created.
    """

    updated_at: Optional[datetime]
    """
    Date and time of last application update.
    """


@dataclass
class Group:
    application_ids: List[str]
    """
    IDs of applications attached to this group.
    """

    user_ids: List[str]
    """
    IDs of users attached to this group.
    """

    description: str
    """
    Description of the group.
    """

    name: str
    """
    Name of the group.
    """

    organization_id: str
    """
    ID of Organization linked to the group.
    """

    id: str
    """
    ID of the group.
    """

    created_at: Optional[datetime]
    """
    Date and time of group creation.
    """

    updated_at: Optional[datetime]
    """
    Date and time of last group update.
    """


@dataclass
class PermissionSet:
    description: str
    """
    Description of the permission set.
    """

    scope_type: PermissionSetScopeType
    """
    Scope of the permission set.
    """

    name: str
    """
    Name of the permission set.
    """

    id: str
    """
    Id of the permission set.
    """

    categories: Optional[List[str]]
    """
    Categories of the permission set.
    """


@dataclass
class Policy:
    nb_permission_sets: int
    """
    Number of permission sets of the policy.
    """

    nb_scopes: int
    """
    Number of policy scopes.
    """

    nb_rules: int
    """
    Number of rules of the policy.
    """

    editable: bool
    """
    Defines whether or not a policy is editable.
    """

    organization_id: str
    """
    Organization ID of the policy.
    """

    description: str
    """
    Description of the policy.
    """

    name: str
    """
    Name of the policy.
    """

    id: str
    """
    Id of the policy.
    """

    created_at: Optional[datetime]
    """
    Date and time of policy creation.
    """

    updated_at: Optional[datetime]
    """
    Date and time of last policy update.
    """

    user_id: Optional[str]

    group_id: Optional[str]

    application_id: Optional[str]

    no_principal: Optional[bool]


@dataclass
class Quotum:
    name: str
    """
    Name of the quota.
    """

    limit: Optional[int]

    unlimited: Optional[bool]


@dataclass
class Rule:
    permission_sets_scope_type: PermissionSetScopeType
    """
    Permission_set_names have the same scope_type.
    """

    id: str
    """
    Id of rule.
    """

    permission_set_names: Optional[List[str]]
    """
    Names of permission sets bound to the rule.
    """

    project_ids: Optional[List[str]]

    organization_id: Optional[str]

    account_root_user_id: Optional[str]


@dataclass
class SSHKey:
    disabled: bool
    """
    SSH key status.
    """

    project_id: str
    """
    ID of Project linked to the SSH key.
    """

    organization_id: str
    """
    ID of Organization linked to the SSH key.
    """

    fingerprint: str
    """
    Fingerprint of the SSH key.
    """

    public_key: str
    """
    Public key of SSH key.
    """

    name: str
    """
    Name of SSH key.
    """

    id: str
    """
    ID of SSH key.
    """

    created_at: Optional[datetime]
    """
    Creation date of SSH key.
    """

    updated_at: Optional[datetime]
    """
    Last update date of SSH key.
    """


@dataclass
class User:
    account_root_user_id: str
    """
    ID of the account root user associated with the user.
    """

    mfa: bool
    """
    Defines whether MFA is enabled.
    """

    status: UserStatus
    """
    Status of user invitation.
    """

    type_: UserType
    """
    Type of user.
    """

    deletable: bool
    """
    Deletion status of user. Owners cannot be deleted.
    """

    organization_id: str
    """
    ID of the Organization.
    """

    email: str
    """
    Email of user.
    """

    id: str
    """
    ID of user.
    """

    created_at: Optional[datetime]
    """
    Date user was created.
    """

    updated_at: Optional[datetime]
    """
    Date of last user update.
    """

    last_login_at: Optional[datetime]
    """
    Date of the last login.
    """

    two_factor_enabled: Optional[bool]
    """
    Deprecated, use "mfa" instead.
    """


@dataclass
class AddGroupMemberRequest:
    group_id: str
    """
    ID of the group.
    """

    user_id: Optional[str]

    application_id: Optional[str]


@dataclass
class AddGroupMembersRequest:
    group_id: str
    """
    ID of the group.
    """

    user_ids: Optional[List[str]]
    """
    IDs of the users to add.
    """

    application_ids: Optional[List[str]]
    """
    IDs of the applications to add.
    """


@dataclass
class ClonePolicyRequest:
    policy_id: str


@dataclass
class CreateAPIKeyRequest:
    description: str
    """
    Description of the API key (max length is 200 characters).
    """

    expires_at: Optional[datetime]
    """
    Expiration date of the API key.
    """

    default_project_id: Optional[str]
    """
    Default Project ID to use with Object Storage.
    """

    application_id: Optional[str]

    user_id: Optional[str]


@dataclass
class CreateApplicationRequest:
    description: str
    """
    Description of the application (max length is 200 characters).
    """

    name: Optional[str]
    """
    Name of the application to create (max length is 64 characters).
    """

    organization_id: Optional[str]
    """
    ID of the Organization.
    """


@dataclass
class CreateGroupRequest:
    description: str
    """
    Description of the group to create (max length is 200 chars).
    """

    organization_id: Optional[str]
    """
    ID of Organization linked to the group.
    """

    name: Optional[str]
    """
    Name of the group to create (max length is 64 chars). MUST be unique inside an Organization.
    """


@dataclass
class CreatePolicyRequest:
    description: str
    """
    Description of the policy to create (max length is 200 characters).
    """

    name: Optional[str]
    """
    Name of the policy to create (max length is 64 characters).
    """

    organization_id: Optional[str]
    """
    ID of the Organization.
    """

    rules: Optional[List[RuleSpecs]]
    """
    Rules of the policy to create.
    """

    user_id: Optional[str]

    group_id: Optional[str]

    application_id: Optional[str]

    no_principal: Optional[bool]


@dataclass
class CreateSSHKeyRequest:
    public_key: str
    """
    SSH public key. Currently only the ssh-rsa, ssh-dss (DSA), ssh-ed25519 and ecdsa keys with NIST curves are supported. Max length is 65000.
    """

    name: Optional[str]
    """
    Name of the SSH key. Max length is 1000.
    """

    project_id: Optional[str]
    """
    Project the resource is attributed to.
    """


@dataclass
class CreateUserRequest:
    email: str
    """
    Email of the user.
    """

    organization_id: Optional[str]
    """
    ID of the Organization.
    """


@dataclass
class DeleteAPIKeyRequest:
    access_key: str
    """
    Access key to delete.
    """


@dataclass
class DeleteApplicationRequest:
    application_id: str
    """
    ID of the application to delete.
    """


@dataclass
class DeleteGroupRequest:
    group_id: str
    """
    ID of the group to delete.
    """


@dataclass
class DeleteJWTRequest:
    jti: str
    """
    JWT ID of the JWT to delete.
    """


@dataclass
class DeletePolicyRequest:
    policy_id: str
    """
    Id of policy to delete.
    """


@dataclass
class DeleteSSHKeyRequest:
    ssh_key_id: str


@dataclass
class DeleteUserRequest:
    user_id: str
    """
    ID of the user to delete.
    """


@dataclass
class GetAPIKeyRequest:
    access_key: str
    """
    Access key to search for.
    """


@dataclass
class GetApplicationRequest:
    application_id: str
    """
    ID of the application to find.
    """


@dataclass
class GetGroupRequest:
    group_id: str
    """
    ID of the group.
    """


@dataclass
class GetJWTRequest:
    jti: str
    """
    JWT ID of the JWT to get.
    """


@dataclass
class GetPolicyRequest:
    policy_id: str
    """
    Id of policy to search.
    """


@dataclass
class GetQuotumRequest:
    quotum_name: str
    """
    Name of the quota to get.
    """

    organization_id: Optional[str]
    """
    ID of the Organization.
    """


@dataclass
class GetSSHKeyRequest:
    ssh_key_id: str
    """
    ID of the SSH key.
    """


@dataclass
class GetUserRequest:
    user_id: str
    """
    ID of the user to find.
    """


@dataclass
class ListAPIKeysRequest:
    order_by: Optional[ListAPIKeysRequestOrderBy]
    """
    Criteria for sorting results.
    """

    page: Optional[int]
    """
    Page number. Value must be greater or equal to 1.
    """

    page_size: Optional[int]
    """
    Number of results per page. Value must be between 1 and 100.
    """

    organization_id: Optional[str]
    """
    ID of Organization.
    """

    editable: Optional[bool]
    """
    Defines whether to filter out editable API keys or not.
    """

    expired: Optional[bool]
    """
    Defines whether to filter out expired API keys or not.
    """

    access_key: Optional[str]
    """
    Filter by access key.
    """

    description: Optional[str]
    """
    Filter by description.
    """

    bearer_id: Optional[str]
    """
    Filter by bearer ID.
    """

    bearer_type: Optional[BearerType]
    """
    Filter by type of bearer.
    """

    application_id: Optional[str]

    user_id: Optional[str]


@dataclass
class ListAPIKeysResponse:
    total_count: int
    """
    Total count of API Keys.
    """

    api_keys: List[APIKey]
    """
    List of API keys.
    """


@dataclass
class ListApplicationsRequest:
    order_by: Optional[ListApplicationsRequestOrderBy]
    """
    Criteria for sorting results.
    """

    page_size: Optional[int]
    """
    Number of results per page. Value must be between 1 and 100.
    """

    page: Optional[int]
    """
    Page number. Value must be greater than 1.
    """

    name: Optional[str]
    """
    Name of the application to filter.
    """

    organization_id: Optional[str]
    """
    ID of the Organization to filter.
    """

    editable: Optional[bool]
    """
    Defines whether to filter out editable applications or not.
    """

    application_ids: Optional[List[str]]
    """
    Filter by list of IDs.
    """


@dataclass
class ListApplicationsResponse:
    total_count: int
    """
    Total count of applications.
    """

    applications: List[Application]
    """
    List of applications.
    """


@dataclass
class ListGroupsRequest:
    order_by: Optional[ListGroupsRequestOrderBy]
    """
    Sort order of groups.
    """

    page: Optional[int]
    """
    Requested page number. Value must be greater or equal to 1.
    """

    page_size: Optional[int]
    """
    Number of items per page. Value must be between 1 and 100.
    """

    organization_id: Optional[str]
    """
    Filter by Organization ID.
    """

    name: Optional[str]
    """
    Name of group to find.
    """

    application_ids: Optional[List[str]]
    """
    Filter by a list of application IDs.
    """

    user_ids: Optional[List[str]]
    """
    Filter by a list of user IDs.
    """

    group_ids: Optional[List[str]]
    """
    Filter by a list of group IDs.
    """


@dataclass
class ListGroupsResponse:
    total_count: int
    """
    Total count of groups.
    """

    groups: List[Group]
    """
    List of groups.
    """


@dataclass
class ListJWTsRequest:
    order_by: Optional[ListJWTsRequestOrderBy]
    """
    Criteria for sorting results.
    """

    audience_id: Optional[str]
    """
    ID of the user to search.
    """

    page_size: Optional[int]
    """
    Number of results per page. Value must be between 1 and 100.
    """

    page: Optional[int]
    """
    Page number. Value must be greater to 1.
    """

    expired: Optional[bool]
    """
    Filter out expired JWTs or not.
    """


@dataclass
class ListJWTsResponse:
    total_count: int

    jwts: List[JWT]


@dataclass
class ListPermissionSetsRequest:
    order_by: Optional[ListPermissionSetsRequestOrderBy]
    """
    Criteria for sorting results.
    """

    page_size: Optional[int]
    """
    Number of results per page. Value must be between 1 and 100.
    """

    page: Optional[int]
    """
    Page number. Value must be greater than 1.
    """

    organization_id: Optional[str]
    """
    Filter by Organization ID.
    """


@dataclass
class ListPermissionSetsResponse:
    total_count: int
    """
    Total count of permission sets.
    """

    permission_sets: List[PermissionSet]
    """
    List of permission sets.
    """


@dataclass
class ListPoliciesRequest:
    order_by: Optional[ListPoliciesRequestOrderBy]
    """
    Criteria for sorting results.
    """

    page_size: Optional[int]
    """
    Number of results per page. Value must be between 1 and 100.
    """

    page: Optional[int]
    """
    Page number. Value must be greater than 1.
    """

    organization_id: Optional[str]
    """
    ID of the Organization to filter.
    """

    editable: Optional[bool]
    """
    Defines whether or not filter out editable policies.
    """

    user_ids: Optional[List[str]]
    """
    Defines whether or not to filter by list of user IDs.
    """

    group_ids: Optional[List[str]]
    """
    Defines whether or not to filter by list of group IDs.
    """

    application_ids: Optional[List[str]]
    """
    Filter by a list of application IDs.
    """

    no_principal: Optional[bool]
    """
    Defines whether or not the policy is attributed to a principal.
    """

    policy_name: Optional[str]
    """
    Name of the policy to fetch.
    """


@dataclass
class ListPoliciesResponse:
    total_count: int
    """
    Total count of policies.
    """

    policies: List[Policy]
    """
    List of policies.
    """


@dataclass
class ListQuotaRequest:
    order_by: Optional[ListQuotaRequestOrderBy]
    """
    Criteria for sorting results.
    """

    page_size: Optional[int]
    """
    Number of results per page. Value must be between 1 and 100.
    """

    page: Optional[int]
    """
    Page number. Value must be greater than 1.
    """

    organization_id: Optional[str]
    """
    Filter by Organization ID.
    """


@dataclass
class ListQuotaResponse:
    total_count: int
    """
    Total count of quota.
    """

    quota: List[Quotum]
    """
    List of quota.
    """


@dataclass
class ListRulesRequest:
    policy_id: str
    """
    Id of policy to search.
    """

    page_size: Optional[int]
    """
    Number of results per page. Value must be between 1 and 100.
    """

    page: Optional[int]
    """
    Page number. Value must be greater than 1.
    """


@dataclass
class ListRulesResponse:
    total_count: int
    """
    Total count of rules.
    """

    rules: List[Rule]
    """
    Rules of the policy.
    """


@dataclass
class ListSSHKeysRequest:
    order_by: Optional[ListSSHKeysRequestOrderBy]
    """
    Sort order of the SSH keys.
    """

    page: Optional[int]
    """
    Requested page number. Value must be greater or equal to 1.
    """

    page_size: Optional[int]
    """
    Number of items per page. Value must be between 1 and 100.
    """

    organization_id: Optional[str]
    """
    Filter by Organization ID.
    """

    name: Optional[str]
    """
    Name of group to find.
    """

    project_id: Optional[str]
    """
    Filter by Project ID.
    """

    disabled: Optional[bool]
    """
    Defines whether to include disabled SSH keys or not.
    """


@dataclass
class ListSSHKeysResponse:
    total_count: int
    """
    Total count of SSH keys.
    """

    ssh_keys: List[SSHKey]
    """
    List of SSH keys.
    """


@dataclass
class ListUsersRequest:
    order_by: Optional[ListUsersRequestOrderBy]
    """
    Criteria for sorting results.
    """

    page_size: Optional[int]
    """
    Number of results per page. Value must be between 1 and 100.
    """

    page: Optional[int]
    """
    Page number. Value must be greater or equal to 1.
    """

    organization_id: Optional[str]
    """
    ID of the Organization to filter.
    """

    user_ids: Optional[List[str]]
    """
    Filter by list of IDs.
    """

    mfa: Optional[bool]
    """
    Filter by MFA status.
    """


@dataclass
class ListUsersResponse:
    total_count: int
    """
    Total count of users.
    """

    users: List[User]
    """
    List of users.
    """


@dataclass
class RemoveGroupMemberRequest:
    group_id: str
    """
    ID of the group.
    """

    user_id: Optional[str]

    application_id: Optional[str]


@dataclass
class SetGroupMembersRequest:
    group_id: str

    user_ids: Optional[List[str]]

    application_ids: Optional[List[str]]


@dataclass
class SetRulesRequest:
    policy_id: str
    """
    Id of policy to update.
    """

    rules: Optional[List[RuleSpecs]]
    """
    Rules of the policy to set.
    """


@dataclass
class SetRulesResponse:
    rules: List[Rule]
    """
    Rules of the policy.
    """


@dataclass
class UpdateAPIKeyRequest:
    access_key: str
    """
    Access key to update.
    """

    default_project_id: Optional[str]
    """
    New default Project ID to set.
    """

    description: Optional[str]
    """
    New description to update.
    """


@dataclass
class UpdateApplicationRequest:
    application_id: str
    """
    ID of the application to update.
    """

    name: Optional[str]
    """
    New name for the application (max length is 64 chars).
    """

    description: Optional[str]
    """
    New description for the application (max length is 200 chars).
    """


@dataclass
class UpdateGroupRequest:
    group_id: str
    """
    ID of the group to update.
    """

    name: Optional[str]
    """
    New name for the group (max length is 64 chars). MUST be unique inside an Organization.
    """

    description: Optional[str]
    """
    New description for the group (max length is 200 chars).
    """


@dataclass
class UpdatePolicyRequest:
    policy_id: str
    """
    Id of policy to update.
    """

    name: Optional[str]
    """
    New name for the policy (max length is 64 characters).
    """

    description: Optional[str]
    """
    New description of policy (max length is 200 characters).
    """

    user_id: Optional[str]

    group_id: Optional[str]

    application_id: Optional[str]

    no_principal: Optional[bool]


@dataclass
class UpdateSSHKeyRequest:
    ssh_key_id: str

    name: Optional[str]
    """
    Name of the SSH key. Max length is 1000.
    """

    disabled: Optional[bool]
    """
    Enable or disable the SSH key.
    """

"""Helpers for interacting with the GitHub API within the Sym SDK."""


from typing import Iterable, List, Literal, Union

from sym.sdk.exceptions import GitHubError  # noqa
from sym.sdk.user import User

GitHubDefaultRolesT = Literal["read", "triage", "write", "maintain", "admin"]
GitHubRoleT = Union[GitHubDefaultRolesT, str]


def get_repo_collaborators(*, repo_name: str, roles: Iterable[GitHubRoleT]) -> List[User]:
    """Get all collaborators of the specified repository with the given role(s), mapped to their
    Sym User objects.

    This is useful to, for example, set the approvers of a request to be users with "admin" access
    to the specified repository.

    Note that ``roles`` are mutually exclusive in GitHub—for example, users with the "admin" role
    technically have write permissions, but not the "write" role. Because of this, "admin" users
    would not be listed if the "write" role were requested. To retrieve both sets of users, you may
    specify multiple roles, e.g., ``{"admin", "write"}``.

    Also note that ``repo_name`` should not include the organization; the organization is derived
    from your Terraform configuration.

    Caution: This method will only return collaborators that have a Sym user corresponding to their
    GitHub Identity. Users can be added and identities managed using the symflow CLI.

    Args:
        repo_name: The name, not including organization, of the repository to get the collaborators
            of
        roles: A set of one or more roles on which to filter collaborators.

    Returns:
        A list of :class:`Users <sym.sdk.user.User>` corresponding to collaborators with the specified role(s)
        of the specified repository.
    """

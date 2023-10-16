"""Helpers for interacting with the Jira API within the Sym SDK."""


from typing import Any, Dict, List, Optional

from sym.sdk.exceptions import JiraError  # noqa


def search_issues(
    jql: str,
    fields: Optional[List[str]] = None,
    expand: Optional[List[str]] = None,
) -> List[dict]:
    """Returns a list of issues matching the given JQL query.

    See Jira's API
    `docs <https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-postt>`_ for details.

    Args:
        jql: A non-empty JQL expression.
        fields: A list of fields to return for each issue. Use it to retrieve a subset of fields.
        expand: An optional list of strings indicating what additional information about issues to include in the response.

    Returns:
        A list of dictionaries representing Jira issues.

    Raises:
        :class:`~sym.sdk.exceptions.jira.JiraError`: If the JQL expression is empty.
    """


def add_comment_to_issue(
    issue_id_or_key: str,
    comment: str,
    expand: Optional[List[str]] = None,
) -> None:
    """Adds a comment to a Jira issue.

    See Jira's API docs
    `here <https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-comments/#api-rest-api-3-issue-issueidorkey-comment-post>`_ for details.

    Args:
        issue_id_or_key: The ID or key of the issue.
        comment: A string to be added as a comment to the Jira issue.
        expand: An optional list of strings indicating what additional information about issues to include in the response.

    Raises:
        :class:`~sym.sdk.exceptions.jira.JiraError`: If the issue does not exist.
    """


def create_issue(
    title: str,
    project_key: str,
    issue_type_name: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    labels: Optional[List[str]] = None,
    parent_issue_id_or_key: Optional[str] = None,
    priority_id: Optional[str] = None,
    custom_fields: Optional[Dict[str, Any]] = None,
) -> str:
    """Creates a Jira issue.

    To create a subtask issue:
        - ``issue_type_name`` must be set to the name of an issue type lower in `hierarchy <https://confluence.atlassian.com/jiraportfoliocloud/configuring-hierarchy-levels-828785179.html>`_ than the issue type of the parent issue.
        - ``parent_issue_id_or_key`` must contain the ID or key of the parent issue.

    See Jira's
    `API docs <https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post>`_ for details.

    Args:
        title: The title of the Jira issue.
        project_key: The key of the project to which the Jira issue should belong.
        issue_type_name: The name of the issue type to assign the Jira issue (e.g. "Bug").
        description: An optional description of the Jira issue.
        due_date: An optional due date of the Jira issue, in the YYYY-MM-DD format.
        labels: An optional list of labels to attach to the Jira issue.
        parent_issue_id_or_key: An optional ID or key of the parent issue.
        priority_id: An optional priority ID for the Jira issue.
        custom_fields: An optional dictionary of custom field names to custom field values.

            NOTES:
                - Custom fields must be added to the screen of the specified issue type. Read `more <https://community.atlassian.com/t5/Jira-Software-questions/How-do-I-add-custom-field-to-specific-issue-type/qaq-p/1320309>`_.
                - Anything passed to ``custom_fields`` will be passed as-is to the request body of the API call. Therefore, it is important to convert your custom field values to the appropriate format (e.g. multi-line text custom fields only take the Atlassian Document Format content). Please refer to the `Jira docs <https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/>`_ to convert your custom field values to the Jira-accepted format.

    Returns:
        The key of the Jira issue.

    Raises:
        :class:`~sym.sdk.exceptions.jira.JiraError`: If the project, issue type, parent issue or priority does not exist, or if the due date is invalid.
    """

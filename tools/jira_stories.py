"""Tool 2: Fetch Jira issues for one exact fix-version ID."""

from langchain_core.tools import tool
from .jira_version import _jira_get


@tool
def jira_story_fetcher(project_key: str, version_id: str) -> list[dict]:
    """Fetch Jira Cloud issues attached to the given fix version (max 200)."""
    project = project_key.strip().replace("\\", "\\\\").replace('"', '\\"')
    version = version_id.strip().replace("\\", "\\\\").replace('"', '\\"')
    jql = f'project = "{project}" AND fixVersion = "{version}" ORDER BY key ASC'

    issues = []
    next_page_token = None

    for _ in range(20):
        params = {
            "jql": jql,
            "maxResults": 100,
            "fields": "summary,description,issuetype,status,labels,components,priority",
        }
        if next_page_token:
            params["nextPageToken"] = next_page_token

        data = _jira_get("/rest/api/3/search/jql", params=params)
        issues.extend(data.get("issues", []))

        if len(issues) > 200:
            raise ValueError("More than 200 Jira issues found for this version.")

        next_page_token = data.get("nextPageToken")
        if not next_page_token or data.get("isLast") is True:
            break
    else:
        raise ValueError("Jira pagination exceeded 20 pages.")

    return issues

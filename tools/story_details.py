"""Tool 3: Extract concise fields from Jira issue records."""

from langchain_core.tools import tool


def _adf_text(value) -> str:
    """Flatten Jira Atlassian Document Format into plain text."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(_adf_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(filter(None, (
            str(value.get("text", "")),
            _adf_text(value.get("content", [])),
        ))).strip()
    return ""


@tool
def story_details_extractor(issues: list[dict]) -> list[dict]:
    """Normalize Jira issue fields into release-note evidence records."""
    stories = []

    for issue in issues:
        fields = issue.get("fields") or {}
        stories.append({
            "key": issue.get("key", ""),
            "summary": fields.get("summary") or "",
            "description": _adf_text(fields.get("description"))[:3500],
            "type": (fields.get("issuetype") or {}).get("name", ""),
            "status": (fields.get("status") or {}).get("name", ""),
            "labels": fields.get("labels") or [],
        })

    return stories

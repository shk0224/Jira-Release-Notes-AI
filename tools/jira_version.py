"""Tool 1: Find a Jira Cloud project fix version by its exact name."""

import os
from urllib.parse import quote

import requests
from langchain_core.tools import tool


def _jira_get(path: str, params: dict | None = None) -> dict | list:
    """Shared read-only Jira REST API helper, also used by jira_stories.py."""
    base_url = os.getenv("JIRA_BASE_URL", "").rstrip("/")
    email = os.getenv("JIRA_EMAIL", "")
    api_token = os.getenv("JIRA_API_TOKEN", "")

    if not all((base_url, email, api_token)):
        raise ValueError("Set JIRA_BASE_URL, JIRA_EMAIL and JIRA_API_TOKEN in .env.")
    if not base_url.startswith("https://"):
        raise ValueError("JIRA_BASE_URL must start with https://")

    response = requests.get(
        base_url + path,
        params=params,
        auth=(email, api_token),
        headers={"Accept": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


@tool
def jira_version_lookup(project_key: str, fix_version: str) -> dict:
    """Look up an exact fix version name in the given Jira Cloud project."""
    project = quote(project_key.strip(), safe="")
    versions = _jira_get(f"/rest/api/3/project/{project}/versions")

    matches = [
        version for version in versions
        if version.get("name", "").casefold() == fix_version.strip().casefold()
    ]
    if not matches:
        raise ValueError(
            f"Fix Version {fix_version!r} not found in project {project_key!r}."
        )

    version = matches[0]
    return {
        "id": str(version["id"]),
        "name": version["name"],
        "description": version.get("description", ""),
        "release_date": version.get("releaseDate", ""),
    }

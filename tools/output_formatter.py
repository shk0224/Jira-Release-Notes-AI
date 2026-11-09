"""Tool 4: Format a review-only maintenance or release-notes draft."""

from langchain_core.tools import tool


@tool
def output_formatter(title: str, body: str) -> str:
    """Combine a draft title and body; never post, send, or publish."""
    return f"{title.strip()}\n\n{body.strip()}\n"

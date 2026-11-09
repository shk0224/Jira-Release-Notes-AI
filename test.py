"""Test Jira API connection without OpenAI."""

from dotenv import load_dotenv
from tools.jira_version import _jira_get


# Load Jira credentials from .env
load_dotenv()


# Connect to Jira Cloud
jira_response = _jira_get("/rest/api/3/myself")


# Display connection status
print("Jira Connection Successful!")
print("Account:", jira_response.get("displayName"))
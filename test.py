
"""Test read-only Jira API connectivity without calling OpenAI."""

import os

import requests
from dotenv import load_dotenv
from tools.jira_version import _jira_get


def main():
    load_dotenv()
    print("Jira API connection test (read-only)")
    print("Project-specific approved proxy configured:", bool(os.getenv("JIRA_HTTPS_PROXY")))
    print("Standard HTTPS proxy configured:", bool(os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")))

    try:
        jira_response = _jira_get("/rest/api/3/myself")
    except requests.HTTPError as error:
        status = error.response.status_code if error.response is not None else "unknown"
        print(f"Jira returned HTTP {status}. Check approved API access and permissions.")
    except requests.ProxyError:
        print("Proxy connection failed. Confirm the approved proxy with IT.")
    except requests.SSLError:
        print("TLS certificate verification failed. Contact IT; do not disable verification.")
    except requests.Timeout:
        print("Jira connection timed out. Ask IT to check network access.")
    except requests.ConnectionError:
        print("Connection failed or was reset. Ask IT to confirm the approved network route.")
    except ValueError as error:
        print("Configuration error:", error)
    else:
        print("Jira Connection Successful!")
        print("Account:", jira_response.get("displayName", "(not provided)"))


if __name__ == "__main__":
    main()

"""FastAPI entry point. Start with: python app.py"""

import os
from pathlib import Path

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend import run_release_workflow

load_dotenv()

app = FastAPI(title="Jira Release Notes AI — LangGraph")
BASE_DIR = Path(__file__).resolve().parent

# Serve external CSS (same style as InvoiceFlow AI).
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


# ==========================================
# REQUEST MODEL
# Class: ReleaseRequest (Pydantic BaseModel)
# ==========================================

class ReleaseRequest(BaseModel):
    project_key: str = Field(min_length=1, max_length=40)
    fix_version: str = Field(min_length=1, max_length=150)
    output_type: str
    maintenance_start: str = ""
    maintenance_end: str = ""
    timezone: str = ""
    impact: str = ""


# ==========================================
# FASTAPI ENDPOINT 1: HOME PAGE
# Method: GET /
# ==========================================

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "templates" / "index.html")


# ==========================================
# FASTAPI ENDPOINT 2: HEALTH CHECK
# Method: GET /health
# ==========================================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "jira_configured": all(os.getenv(key) for key in (
            "JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN"
        )),
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
    }


# ==========================================
# FASTAPI ENDPOINT 3: GENERATE DRAFT
# Method: POST /api/generate
# Calls: backend.py -> run_release_workflow()
# ==========================================

@app.post("/api/generate")
def generate(request: ReleaseRequest):
    """Generate a review-only draft. Nothing is sent or published."""

    if request.output_type not in ("maintenance", "release_notes"):
        raise HTTPException(400, "Select Maintenance Notice or Release Notes.")

    try:
        result = run_release_workflow(request.model_dump())
        return {"result": result}

    except requests.HTTPError as error:
        # Do not expose request headers, API tokens, or raw Jira error bodies.
        status = error.response.status_code if error.response is not None else 502
        raise HTTPException(
            502, f"Jira request failed (HTTP {status}). Check Jira permissions."
        ) from None

    except requests.RequestException:
        raise HTTPException(502, "Cannot connect to Jira. Check configuration.") from None

    except ValueError as error:
        raise HTTPException(400, str(error)) from None

    except Exception:
        raise HTTPException(500, "Generation failed. Check server logs.") from None


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

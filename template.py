
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent

# Folder structure
folders = [
    "tools",
    "templates",
    "static",
    "tests",
    "output",
]

# File structure
files = [
    "app.py",
    "backend.py",
    "requirements.txt",
    ".env.example",
    ".gitignore",
    "tools/__init__.py",
    "tools/jira_tools.py",
    "templates/index.html",
    "tests/test_release_notes.py",
]

# Create folders
for folder in folders:
    folder_path = PROJECT_ROOT / folder
    folder_path.mkdir(parents=True, exist_ok=True)
    print(f"Folder created: {folder}")

# Create files
for file in files:
    file_path = PROJECT_ROOT / file
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=True)
    print(f"File ready: {file}")

print("\nJira-Release-Notes-AI project structure created successfully!")

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
    "README.md",
    "tools/__init__.py",
    "tools/jira_version.py",
    "tools/jira_stories.py",
    "tools/story_details.py",
    "tools/output_formatter.py",
    "templates/index.html",
    "static/style.css",
    "tests/test_release_notes.py",
]

# Create folders
for folder in folders:
    folder_path = PROJECT_ROOT / folder
    folder_path.mkdir(parents=True, exist_ok=True)
    print(f"Folder created: {folder}")

# Create files (never overwrite existing contents)
for file in files:
    file_path = PROJECT_ROOT / file
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=True)
    print(f"File ready: {file}")

print("\nJira-Release-Notes-AI project structure created successfully!")

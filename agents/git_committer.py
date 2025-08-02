from git import Repo
import os

def commit_and_push_changes(repo_path: str, commit_message: str) -> str:
    # If a file was passed instead of a folder, go one level up
    if os.path.isfile(repo_path):
        repo_path = os.path.dirname(repo_path)

    if not os.path.exists(os.path.join(repo_path, ".git")):
        return "❌ Not a valid git repository."

    # continue as normal...


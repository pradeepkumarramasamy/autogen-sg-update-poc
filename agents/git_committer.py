from git import Repo
import os

def commit_and_push_changes(repo_path: str, commit_message: str) -> str:
    try:
        repo = Repo(repo_path, search_parent_directories=True)
    except Exception as e:
        return f"❌ Failed to locate git repo: {e}"

    if repo.is_dirty(untracked_files=True):
        repo.git.add(update=True)
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
        return f"✅ Changes pushed with message: '{commit_message}'"
    else:
        return "⚠️ No changes to commit."

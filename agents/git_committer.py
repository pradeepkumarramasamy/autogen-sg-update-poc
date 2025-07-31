from git import Repo
import os

def commit_and_push_changes(repo_path: str, commit_message: str) -> None:
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print("❌ Not a valid git repository.")
        return

    repo = Repo(repo_path)

    if repo.is_dirty(untracked_files=True):
        repo.git.add(update=True)
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
        print(f"✅ Changes pushed with message: '{commit_message}'")
    else:
        print("⚠️ No changes to commit.")

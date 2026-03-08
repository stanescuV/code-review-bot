import os
import subprocess

def git_diff():

    base_sha = os.environ.get('BASE_SHA')
    head_sha = os.environ.get('HEAD_SHA')

    if not base_sha or not head_sha:
        print("Error: BASE_SHA and HEAD_SHA environment variables are required.")
        exit(1)

    result = subprocess.run(
    ['git', 'diff', base_sha, head_sha],
    capture_output=True,
    text=True
)

    if result.returncode != 0:
        print(f"Error running git diff: {result.stderr}")
        exit(1)

    diff = result.stdout

    if not diff:
        print("No changes detected between the two commits.")
        exit(0)
        
    return diff
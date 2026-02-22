import os
import subprocess
import sys

def run_git_command(command):
    """Executes a git command and returns the output as a string."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def main():
    base_sha = os.environ.get('BASE_SHA')
    head_sha = os.environ.get('HEAD_SHA')

    if not base_sha or not head_sha:
        print("Error: BASE_SHA or HEAD_SHA environment variable is missing.")
        sys.exit(1)

    print(f"Analyzing changes: Base ({base_sha}) -> Head ({head_sha})\n")

    status_cmd = ['git', 'diff', '--name-status', base_sha, head_sha]
    file_statuses = run_git_command(status_cmd)
    
    print("--- Changed Files ---")
    print(file_statuses)
    print("---------------------\n")

    diff_cmd = ['git', 'diff', base_sha, head_sha]
    full_diff = run_git_command(diff_cmd)

    if "TODO: FIX THIS HACK" in full_diff:
        print("❌ Error: Found a forbidden string in the diff. Blocking PR.")
        sys.exit(1)

    print("✅ Analysis complete. Everything looks good!")

if __name__ == "__main__":
    main()
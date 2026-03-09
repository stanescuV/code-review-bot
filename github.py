import httpx
import os

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


async def post_pr_comment(client: httpx.AsyncClient, repo: str, pr_number: int, body: str):
    await client.post(
        f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments",
        json={"body": body},
        headers=HEADERS
    )


async def post_commit_status(client: httpx.AsyncClient, repo: str, sha: str, state: str, description: str):
    await client.post(
        f"https://api.github.com/repos/{repo}/statuses/{sha}",
        json={
            "state": state,
            "description": description,
            "context": "code-review-bot"
        },
        headers=HEADERS
    )

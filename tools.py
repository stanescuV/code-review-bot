import os
import httpx
import resend


def _github_headers() -> dict:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }


def send_alert_email(message: str) -> str:
    """Send an alert email when a critical issue is found in the code review."""
    resend.api_key = os.environ.get("RESEND_API_KEY", "").strip()
    recipient = os.environ.get("RECIPIENT_EMAIL", "").strip()

    if not resend.api_key or not recipient:
        return "Email alert failed: missing RESEND_API_KEY or RECIPIENT_EMAIL in .env"

    resend.Emails.send({
        "from": "Code Review Bot <onboarding@resend.dev>",
        "to": recipient,
        "subject": "CRITICAL: Code Review Alert",
        "text": message,
    })

    return f"Alert email sent to {recipient}"


def post_pr_comment(repo: str, pr_number: int, body: str) -> str:
    """Post a comment on a GitHub pull request."""
    response = httpx.post(
        f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments",
        json={"body": body},
        headers=_github_headers()
    )
    return f"Comment posted (status {response.status_code})"


def post_commit_status(repo: str, sha: str, state: str, description: str) -> str:
    """Post a commit status on GitHub."""
    response = httpx.post(
        f"https://api.github.com/repos/{repo}/statuses/{sha}",
        json={"state": state, "description": description, "context": "code-review-bot"},
        headers=_github_headers()
    )
    return f"Status posted (status {response.status_code})"


TOOLS = [
    {
        "type": "function",
        "name": "send_alert_email",
        "description": (
            "Send an alert email to the team when a CRITICAL issue is found in the code review. "
            "Only call this for serious security vulnerabilities, data loss risk, or breaking changes."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The alert message describing the critical issue found."
                },
            },
            "required": ["message"]
        }
    },
    {
        "type": "function",
        "name": "post_pr_comment",
        "description": (
            "Post a review comment on the pull request. "
            "Use this for CRITICAL, HIGH, or MEDIUM issues. "
            "Start the comment with the severity label e.g. '[CRITICAL]', '[HIGH]', '[MEDIUM]'."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "body": {
                    "type": "string",
                    "description": "The comment body to post on the pull request."
                },
            },
            "required": ["body"]
        }
    }
]

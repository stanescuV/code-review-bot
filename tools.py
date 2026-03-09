import os
import resend


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

TOOLS = [
    {
        "type": "function",
        "name": "send_alert_email",
        "description": (
            "Send an alert email to the team when a CRITICAL issue is found in the code review. "
            "Only call this if the code contains a serious bug, security vulnerability, or breaking change."
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
    }
]





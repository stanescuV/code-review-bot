import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_alert_email(message: str) -> str:
    """Send an alert email when a critical issue is found in the code review."""
    sender = os.environ.get("ALERT_EMAIL", "").strip()
    password = os.environ.get("ALERT_EMAIL_PASSWORD", "").strip()
    recipient = os.environ.get("RECIPIENT_EMAIL", "").strip()

    if not sender or not password or not recipient:
        return "Email alert failed: missing EMAIL, EMAIL_PASSWORD, or RECIPIENT_EMAIL in .env"

    msg = MIMEText(message)
    msg["Subject"] = "CRITICAL: Code Review Alert"
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, recipient, msg.as_string())

    return f"Alert email sent to {recipient}"

print(send_alert_email("A critical issue was found in the code review."))

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





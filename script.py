
import json
import os
from openai import OpenAI
from tools import TOOLS, send_alert_email
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY", "").strip()

  
def run_code_review_with_tools(diff: str) -> tuple[str, bool]:
    client = OpenAI(api_key=api_key)
    critical = False

    messages = [
        {
            "role": "user",
            "content": (
                "You are a code reviewer. Review the following git diff and classify any issues you find by severity:\n\n"
                "- CRITICAL: security vulnerabilities, data loss risk, authentication bypass, exposed secrets. "
                "Call the send_alert_email tool AND write a comment.\n"
                "- HIGH or MEDIUM: severe bugs, broken logic, significant performance problems. "
                "Write a comment only, do NOT send an email.\n"
                "- LOW: minor style issues, small improvements, nitpicks. Ignore these entirely, do not comment.\n\n"
                "If there are no CRITICAL, HIGH, or MEDIUM issues, respond with an empty string.\n"
                "Be direct and concise in your comments. Start your comment with the severity level "
                "(e.g. '[CRITICAL]', '[HIGH]', '[MEDIUM]').\n\n"
                f"{diff}"
            )
        }
    ]

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=messages,
        tools=TOOLS,
    )

    for output in response.output:
        if output.type == "function_call" and output.name == "send_alert_email":
            args = json.loads(output.arguments)
            result = send_alert_email(args["message"])
            print(f"Tool called: send_alert_email -> {result}")
            critical = True

    return response.output_text, critical

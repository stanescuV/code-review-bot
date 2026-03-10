
import json
import os
from openai import OpenAI
from tools import TOOLS, send_alert_email, post_pr_comment
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY", "").strip()


def run_code_review_with_tools(diff: str, repo: str, pr_number: int) -> bool:
    client = OpenAI(api_key=api_key)
    critical = False

    messages = [
        {
            "role": "user",
            "content": (
                "You are a code reviewer. Review the following git diff and classify any issues by severity:\n\n"
                "- CRITICAL: security vulnerabilities, data loss risk, authentication bypass, exposed secrets. "
                "Call send_alert_email AND post_pr_comment.\n"
                "- HIGH or MEDIUM: severe bugs, broken logic, significant performance problems. "
                "Call post_pr_comment only.\n"
                "- LOW: minor style issues, small improvements, nitpicks. Ignore these entirely.\n\n"
                "If there are no CRITICAL, HIGH, or MEDIUM issues, do not call any tools.\n"
                "Start comments with the severity label e.g. '[CRITICAL]', '[HIGH]', '[MEDIUM]'.\n\n"
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
        if output.type == "function_call":
            args = json.loads(output.arguments)
            if output.name == "send_alert_email":
                result = send_alert_email(args["message"])
                print(f"Tool called: send_alert_email -> {result}")
                critical = True
            elif output.name == "post_pr_comment":
                result = post_pr_comment(repo, pr_number, args["body"])
                print(f"Tool called: post_pr_comment -> {result}")

    return critical

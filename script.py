
import json
import os
from openai import OpenAI
from tools import TOOLS, send_alert_email
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY", "").strip()

  
def run_code_review_with_tools(diff: str) -> str:
    client = OpenAI(api_key=api_key)

    messages = [
        {
            "role": "user",
            "content": (
                "You are a code reviewer. Review the following git diff and provide a short, "
                "concise code review. Focus on bugs, issues, and important observations only. "
                "Be direct and brief. If you find a CRITICAL issue (security vulnerability, "
                "data loss risk, or severe bug), call the send_alert_email tool.\n\n"
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

    return response.output_text

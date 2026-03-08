import os
from dotenv import load_dotenv
from openai import OpenAI
from git_diff import git_diff

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "").strip())

diff = git_diff()


response = client.responses.create(
    model="gpt-4.1-mini",
    input=(
        "You are a code reviewer. Review the following git diff and provide a short, "
        "concise code review. Focus on bugs, issues, and important observations only. "
        "Be direct and brief.\n\n"
        
        f"{diff}"
    )
)

print(response.output_text)

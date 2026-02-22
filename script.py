import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "").strip())

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

#TODO: Tools, 1 for snippets 1 for whole file. in order to reduce the token consumption and increase quality. 
#This is a reminder for the todo
#TEST
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

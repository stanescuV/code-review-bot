from dotenv import load_dotenv
load_dotenv()

import httpx
from fastapi import FastAPI, Request
from script import run_code_review_with_tools
from github import post_pr_comment, post_commit_status

app = FastAPI()


@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    action = payload.get("action")
    pr = payload.get("pull_request", {})

    if not pr:
        return {"status": "ignored", "reason": "not a pull_request event"}

    if action not in ("opened", "synchronize", "reopened"):
        return {"status": "ignored", "reason": f"action '{action}' does not require review"}

    head_sha = pr.get("head", {}).get("sha")
    repo = payload.get("repository", {}).get("full_name")
    pr_number = pr.get("number")
    pr_title = pr.get("title")

    print(f"PR #{pr_number} [{action}]: {pr_title}")
    print(f"  repo:     {repo}")
    print(f"  head_sha: {head_sha}")

    diff_url = pr.get("diff_url")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(diff_url)
        diff = response.text

        chatbot_answer, critical = run_code_review_with_tools(diff)

        if chatbot_answer:
            await post_pr_comment(client, repo, pr_number, chatbot_answer)

        if critical:
            await post_commit_status(client, repo, head_sha, "failure", "Critical issue detected — merge blocked.")
        else:
            await post_commit_status(client, repo, head_sha, "success", "Code review passed.")

    return {"status": "ok", "pr": pr_number, "action": action, "chatbot_answer": chatbot_answer}

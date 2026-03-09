import httpx
from fastapi import FastAPI, Request
from script import run_code_review_with_tools

app = FastAPI()

#THIS IS A SECRET PASSWORD FOR PRODUCTION : 12345QWEASDZXC
@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    action = payload.get("action")
    pr = payload.get("pull_request", {})

    if not pr:
        return {"status": "ignored", "reason": "not a pull_request event"}

    base_sha = pr.get("base", {}).get("sha")
    head_sha = pr.get("head", {}).get("sha")
    repo = payload.get("repository", {}).get("full_name")
    pr_number = pr.get("number")
    pr_title = pr.get("title")

    print(f"PR #{pr_number} [{action}]: {pr_title}")
    print(f"  repo:     {repo}")
    print(f"  base_sha: {base_sha}")
    print(f"  head_sha: {head_sha}")

    diff_url = pr.get("diff_url")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(diff_url)
        diff = response.text

    chatbot_answer = run_code_review_with_tools(diff)
    return {"status": "ok", "pr": pr_number, "action": action, "chatbot_answer": chatbot_answer}

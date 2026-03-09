# Code Review Bot

A GitHub webhook bot that automatically reviews pull requests using OpenAI. If a critical issue is detected (security vulnerability, severe bug, data loss risk), it sends an alert email via [Resend](https://resend.com).

---

## How It Works

1. GitHub sends a webhook to your server when a PR is opened/updated
2. The server fetches the PR diff and sends it to OpenAI for review
3. OpenAI returns a code review summary
4. If the issue is critical, OpenAI calls the `send_alert_email` tool and an email is sent automatically via Resend

---

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Docker (optional, for containerized deployment)
- A [Resend](https://resend.com) account (free tier: 3,000 emails/month)
- An OpenAI API key

---


## 1. Install uv
## I like UV because it's faster than PIP :D

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify the installation:
```bash
uv --version
```

---

## 2. Clone the Repository

```bash
git clone https://github.com/stanescuV/code-review-bot.git
cd code-review-bot
```

---

## 3. Install Dependencies

```bash
uv sync
```

This creates a virtual environment and installs all packages from `pyproject.toml`.

---

## 4. Configure Environment Variables

Copy the example env file:
```bash
cp .env.dist .env
```

Open `.env` and fill in the values:

```env
OPENAI_API_KEY=your_openai_api_key
RECIPIENT_EMAIL=recipient@example.com
RESEND_API_KEY=your_resend_api_key
```

### Getting your OpenAI API Key
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click **Create new secret key**
3. Copy and paste it as `OPENAI_API_KEY`

### Getting a Resend API Key
1. Sign up at [resend.com](https://resend.com) (free)
2. Go to **API Keys** → **Create API Key**
3. Copy and paste it as `RESEND_API_KEY`

> Free tier includes 3,000 emails/month and 100/day — more than enough for a code review bot.

---

## 5. Run Locally

```bash
uv run uvicorn api:app --host 0.0.0.0 --port 8000
```

The API is now running at `http://localhost:8000`.

---

## 6. Run with Docker

**Build the image:**
```bash
docker build -t code-review-bot .
```

**Run the container** (loads variables from your `.env`):
```bash
docker run -d --name code-review-bot --network host --env-file .env --restart unless-stopped code-review-bot
```

**Useful commands:**
```bash
docker logs code-review-bot        # view logs
docker logs -f code-review-bot     # follow logs live
docker ps                          # check running containers
```

---

## 7. Deploy Updates (VPS)

After pushing changes, run on your VPS:

```bash
git pull
docker build -t code-review-bot .
docker stop code-review-bot && docker rm code-review-bot
docker run -d --name code-review-bot --network host --env-file .env --restart unless-stopped code-review-bot
```

Or use the `deploy.sh` script:
```bash
bash deploy.sh
```

---

## 8. Connect GitHub Webhook

1. Go to your GitHub repository → **Settings** → **Webhooks** → **Add webhook**
2. Set **Payload URL** to your server's public URL:
   ```
   http://your-vps-ip:8000/webhook
   ```
3. Set **Content type** to `application/json`
4. Select **Pull request** events
5. Click **Add webhook**

### Expose localhost with ngrok (for local testing)
```bash
ngrok http 8000
```
Use the generated `https://xxxx.ngrok.io` URL as your webhook payload URL.

---

## 9. Test with curl

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "action": "opened",
    "pull_request": {
      "number": 1,
      "title": "Test PR",
      "diff_url": "https://github.com/stanescuV/code-review-bot/pull/5.diff",
      "base": {"sha": "abc123"},
      "head": {"sha": "def456"}
    },
    "repository": {
      "full_name": "stanescuV/code-review-bot"
    }
  }'
```

**Expected response:**
```json
{
  "status": "ok",
  "pr": 1,
  "action": "opened",
  "chatbot_answer": "..."
}
```

If a critical issue is found, an alert email is automatically sent to `RECIPIENT_EMAIL`.

---

## Project Structure

```
code-review-bot/
├── api.py          # FastAPI server, webhook endpoint
├── script.py       # OpenAI code review logic with tool calling
├── tools.py        # send_alert_email function + OpenAI tool schema
├── .env            # Environment variables (never commit this)
├── .env.dist       # Example env file (safe to commit)
├── pyproject.toml  # Dependencies
└── Dockerfile      # Docker configuration
```

---

## Environment Variables Reference

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `RECIPIENT_EMAIL` | Email address that receives critical alerts |
| `RESEND_API_KEY` | Your Resend API key for sending emails |

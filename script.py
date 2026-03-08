from openai import OpenAI


def create_code_review(diff, api_key):
    client = OpenAI(api_key=api_key)



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


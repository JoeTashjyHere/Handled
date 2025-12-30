import os

from openai import OpenAI

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_intake(summary: str) -> str:
    prompt = (
        "You are Handled, an AI life admin assistant. "
        "Summarize the request into actionable tasks and key details."
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": summary}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

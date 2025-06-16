import os
import openai

from app.utils import SummaryLength

openai.api_key = os.getenv("OPENAI_API_KEY")

async def summarize_text(text: str, summary_length: SummaryLength) -> str:
    prompt = (
        "You are a helpful assistant. "
        f"Please provide a **{summary_length.value}** summary of the following document text:\n\n"
        f"{text}\n\n"
        "Summary:"
    )

    max_tokens_map = {
        "short": 150,
        "medium": 200,
        "long": 350,
    }

    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens_map[summary_length.value],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

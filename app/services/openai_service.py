import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
print(f"ISSS OPENAI_API_KEY is set? {'Yes' if openai.api_key else 'No'}")
print(os.getenv("OPENAI_API_KEY"))

async def summarize_text(text: str) -> str:
    prompt = (
        "You are a helpful assistant. "
        "Please provide a concise summary of the following document text:\n\n"
        f"{text}\n\n"
        "Summary:"
    )

    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.3,
    )
    summary = response.choices[0].message.content.strip()
    return summary

# ai_writer.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_field(prompt: str) -> str:
    """Send a prompt to Groq and return the generated text."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional CV writer. "
                        "You write concise, impactful, and professional CV content. "
                        "Return only the requested content, no explanations or extra text."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Groq API error: {e}")
        return "Unable to generate content at this time."


def fill_ai_fields(data: dict) -> dict:
    """
    Takes the collected user data, finds all AI fields,
    generates content for each, and returns the completed data dict.
    """
    from cv_fields import AI_FIELDS

    for field in AI_FIELDS:
        try:
            # Fill the prompt placeholders with actual user data
            filled_prompt = field["ai_prompt"].format(**data)
            generated = generate_field(filled_prompt)
            data[field["key"]] = generated
            print(f"✓ AI generated: {field['key']}")
        except KeyError as e:
            print(f"Missing data for AI prompt placeholder: {e}")
            data[field["key"]] = ""

    return data
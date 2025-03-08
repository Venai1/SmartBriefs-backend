from dotenv import load_dotenv
from openai import OpenAI
import os

def generate_open_ai_summary(system_prompt):
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
        ]
    )
    return response.choices[0].message.content.strip()
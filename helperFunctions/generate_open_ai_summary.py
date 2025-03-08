from dotenv import load_dotenv
from openai import OpenAI
import os

def generate_open_ai_summary(system_prompt):
    """
    Generate a summary using OpenAI API with robust error handling.
    """
    load_dotenv()
    try:
        # Create OpenAI client WITHOUT proxy settings
        client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
        
        # Make the API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": system_prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating summary with OpenAI: {str(e)}")
        # Provide a fallback summary
        return "Your financial summary and market analysis for today's economic landscape."
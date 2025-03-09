from dotenv import load_dotenv
from openai import OpenAI
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_open_ai_summary(system_prompt):
    """
    Generate a summary using OpenAI API with robust error handling.
    
    Args:
        system_prompt (str): The prompt to send to OpenAI
        
    Returns:
        str: The generated summary or a fallback message
    """
    load_dotenv()
    
    # Get API key with proper error handling
    api_key = os.getenv("OPEN_AI_API_KEY")
    if not api_key:
        logger.error("OPEN_AI_API_KEY environment variable not found")
        return "Your personal financial summary. Check your accounts for details."
    
    try:
        # Create OpenAI client without any proxy settings
        # Make sure to only pass the api_key parameter
        client = OpenAI(api_key=api_key)
        
        # Log that we're making the API call
        logger.info(f"Making OpenAI API call with prompt: {system_prompt[:100]}...")
        
        # Make the API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": system_prompt}
            ]
        )
        
        # Extract and log the result
        result = response.choices[0].message.content.strip()
        logger.info(f"Successfully generated summary: {result[:100]}...")
        return result
        
    except Exception as e:
        logger.error(f"Error generating summary with OpenAI: {str(e)}")
        
        # Provide a more personalized fallback summary
        return "Your financial summary and market analysis for today's economic landscape."

if __name__ == "__main__":
    # Simple test prompt
    test_prompt = (
        "Create a friendly financial headline for John Doe. "
        "Net worth: $45,000, spending: $2,500, deposits: $3,200, debt: $15,000. "
        "Top spending: Restaurants, Shopping. Spending trend: decreasing."
    )
    
    # Run the test
    print("Testing OpenAI summary generation...")
    result = generate_open_ai_summary(test_prompt)
    print("\nResult:")
    print(result)
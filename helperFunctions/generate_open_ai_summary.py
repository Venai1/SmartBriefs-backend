from dotenv import load_dotenv
from openai import OpenAI
import os
import logging
import requests
import time
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_open_ai_summary(system_prompt):
    """
    Generate a summary using OpenAI API with robust error handling and diagnostics.
    
    Args:
        system_prompt (str): The prompt to send to OpenAI
        
    Returns:
        str: The generated summary or a fallback message
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key with proper error handling
    api_key = os.getenv("OPEN_AI_API_KEY")
    if not api_key:
        logger.error("OPEN_AI_API_KEY environment variable not found")
        return "Your personal financial summary. Check your accounts for details."

    # First, let's check connectivity to OpenAI's API
    try:
        logger.info("Testing connectivity to OpenAI API...")
        # Simple connectivity test
        response = requests.get("https://api.openai.com", timeout=5)
        logger.info(f"OpenAI API connectivity test status: {response.status_code}")
    except Exception as e:
        logger.error(f"Failed to connect to OpenAI API: {str(e)}")
        # Continue anyway since this is just a diagnostic test
    
    # Log the API key length for debugging (without revealing the key)
    logger.info(f"API key length: {len(api_key)}")
    logger.info(f"API key first 4 chars: {api_key[:4]}***")
    
    try:
        # Create OpenAI client with just the API key
        client = OpenAI(api_key=api_key)
        
        # Log that we're making the API call
        logger.info(f"Making OpenAI API call with prompt length: {len(system_prompt)}")
        
        # More detailed logging
        start_time = time.time()
        
        # Make the API call with timeout
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": system_prompt}
            ],
            timeout=30  # Set a timeout for the API call
        )
        
        # Calculate time taken
        time_taken = time.time() - start_time
        logger.info(f"API call completed in {time_taken:.2f} seconds")
        
        # Extract and log the result
        result = response.choices[0].message.content.strip()
        logger.info(f"Successfully generated summary: '{result[:50]}...' (length: {len(result)})")
        return result
        
    except Exception as e:
        logger.error(f"Error generating summary with OpenAI: {str(e)}")
        
        # Try a different approach - using requests directly for diagnostic purposes
        try:
            logger.info("Attempting direct API call using requests...")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful financial assistant."},
                    {"role": "user", "content": system_prompt}
                ]
            }
            direct_response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            logger.info(f"Direct API call status: {direct_response.status_code}")
            if direct_response.status_code == 200:
                response_json = direct_response.json()
                direct_result = response_json["choices"][0]["message"]["content"].strip()
                logger.info(f"Direct API call success, response: {direct_result[:50]}...")
                return direct_result
            else:
                logger.error(f"Direct API call failed: {direct_response.text}")
        except Exception as direct_e:
            logger.error(f"Direct API call also failed: {str(direct_e)}")
        
        # Generate a more personalized fallback based on the data
        # Extract key information from the prompt to create a more relevant fallback
        try:
            # This is a rough extraction, might need adjustment based on your exact prompt format
            name_match = system_prompt.split("directly to ")[1].split(".")[0]
            net_worth_match = system_prompt.split("net worth: $")[1].split(",")[0]
            
            # Create a slightly personalized fallback
            return f"Hello {name_match}! Here's your financial snapshot with a net worth of ${net_worth_match}. Review your accounts for detailed insights and spending patterns."
        except Exception:
            # If extraction fails, fall back to generic message
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
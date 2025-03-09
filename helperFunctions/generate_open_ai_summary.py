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
    
    # Test error handling with invalid API key
    print("\nTesting error handling...")
    original_key = os.environ.get("OPEN_AI_API_KEY")
    os.environ["OPEN_AI_API_KEY"] = "invalid_key"
    
    fallback = generate_open_ai_summary(test_prompt)
    print("\nFallback result:")
    print(fallback)
    
    # Restore original key if it existed
    if original_key:
        os.environ["OPEN_AI_API_KEY"] = original_key
import json
import pandas as pd
from openai import OpenAI
from anthropic import Anthropic
import os
from typing import Dict, Any

def generate_report_with_openai(customer_data: Dict[str, Any], model: str = "gpt-4-turbo") -> str:
    """
    Generate a financial report using OpenAI's API
    
    Parameters:
    - customer_data: Result from process_customer function
    - model: OpenAI model to use
    
    Returns:
    - Generated report as string
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Format data for prompt
    customer_info = customer_data["data_tables"]["customers"].iloc[0].to_dict() if not customer_data["data_tables"]["customers"].empty else {}
    
    # Convert pandas dataframes to json for the prompt
    prompt_data = {
        "customer_info": customer_info,
        "accounts": customer_data["data_tables"]["accounts"].to_dict(orient="records") if not customer_data["data_tables"]["accounts"].empty else [],
        "transactions": customer_data["data_tables"]["transactions"].to_dict(orient="records") if not customer_data["data_tables"]["transactions"].empty else [],
        "financial_metrics": customer_data["financial_metrics"],
        "transaction_summary": customer_data["transaction_summary"].to_dict(orient="records") if not isinstance(customer_data["transaction_summary"], pd.DataFrame) or not customer_data["transaction_summary"].empty else []
    }
    
    prompt = f"""
    You are a financial analyst AI that creates insightful customer financial reports. 
    Please analyze the following banking data and create a detailed financial report:
    
    {json.dumps(prompt_data, indent=2)}
    
    Include the following in your report:
    1. Customer profile summary
    2. Account overview
    3. Transaction analysis
    4. Spending patterns by transaction type
    5. Financial health assessment
    6. Recommendations based on spending habits
    
    Format the report professionally with clear sections and insights.
    """
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a financial analyst AI that creates insightful, accurate financial reports."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=2000
    )
    
    return response.choices[0].message.content

def generate_report_with_anthropic(customer_data: Dict[str, Any], model: str = "claude-3-opus-20240229") -> str:
    """
    Generate a financial report using Anthropic's API
    
    Parameters:
    - customer_data: Result from process_customer function
    - model: Anthropic model to use
    
    Returns:
    - Generated report as string
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Format data for prompt
    customer_info = customer_data["data_tables"]["customers"].iloc[0].to_dict() if not customer_data["data_tables"]["customers"].empty else {}
    
    # Convert pandas dataframes to json for the prompt
    prompt_data = {
        "customer_info": customer_info,
        "accounts": customer_data["data_tables"]["accounts"].to_dict(orient="records") if not customer_data["data_tables"]["accounts"].empty else [],
        "transactions": customer_data["data_tables"]["transactions"].to_dict(orient="records") if not customer_data["data_tables"]["transactions"].empty else [],
        "financial_metrics": customer_data["financial_metrics"],
        "transaction_summary": customer_data["transaction_summary"].to_dict(orient="records") if not isinstance(customer_data["transaction_summary"], pd.DataFrame) or not customer_data["transaction_summary"].empty else []
    }
    
    prompt = f"""
    You are a financial analyst AI that creates insightful customer financial reports. 
    Please analyze the following banking data and create a detailed financial report:
    
    {json.dumps(prompt_data, indent=2)}
    
    Include the following in your report:
    1. Customer profile summary
    2. Account overview
    3. Transaction analysis
    4. Spending patterns by transaction type
    5. Financial health assessment
    6. Recommendations based on spending habits
    
    Format the report professionally with clear sections and insights.
    """
    
    response = client.messages.create(
        model=model,
        max_tokens=2000,
        temperature=0.2,
        system="You are a financial analyst AI that creates insightful, accurate financial reports.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text

def save_report_to_file(report: str, customer_id: str, time_period: str = None) -> str:
    """
    Save the generated report to a file
    
    Parameters:
    - report: The generated report text
    - customer_id: ID of the customer
    - time_period: Time period used for the report
    
    Returns:
    - Path to the saved file
    """
    time_str = f"_{time_period}" if time_period else ""
    filename = f"financial_report_{customer_id}{time_str}.md"
    
    with open(filename, "w") as f:
        f.write(report)
    
    return filename

def main():
    # Set environment variables for API keys
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
    os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key"
    
    # Process customer data
    customer_id = "67cb640c9683f20dd518d16f"
    time_period = "30d"
    
    # Import the process_customer function
    from getBankData import process_customer
    
    # Get customer data
    customer_data = process_customer(customer_id, time_period)
    
    # Choose which LLM to use
    use_openai = True  # Set to False to use Anthropic
    
    if use_openai:
        report = generate_report_with_openai(customer_data)
    else:
        report = generate_report_with_anthropic(customer_data)
    
    # Save the report
    file_path = save_report_to_file(report, customer_id, time_period)
    
    print(f"Financial report saved to {file_path}")
    print("\nReport Preview:")
    print("=" * 50)
    print(report[:500] + "..." if len(report) > 500 else report)
    print("=" * 50)

if __name__ == "__main__":
    main()
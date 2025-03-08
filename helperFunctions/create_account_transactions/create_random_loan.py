import os
import random
from dotenv import load_dotenv
import requests
import json

def create_random_loan(account_id):
    """Create a random loan for a specific account"""
    load_dotenv()

    loan_data = {
        "type": "home",
        "status": "pending",
        "credit_score": random.randint(300, 780),
        "monthly_payment": random.randint(100, 2000),
        "amount": random.randint(1000, 50000),
        "description": random.choice([
            "Home renovation",
            "Car purchase",
            "Education expenses",
            "Debt consolidation",
            "Medical expenses"
        ])
    }

    # API endpoint for creating a loan
    url = f"{os.getenv('NESSIE_API_URL')}/accounts/{account_id}/loans?key={os.getenv('NESSIE_API_KEY')}"

    # Send request
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(
            url,
            data=json.dumps(loan_data),
            headers=headers
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating loan: {str(e)}")
        return None
import requests
import json
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

def create_random_deposit(account_id):
    """Create a random deposit for a specific account"""
    load_dotenv()

    deposit_data = {
        "medium": "balance",
        "transaction_date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
        "status": random.choice(["pending", "completed", "cancelled"]),
        "amount": round(random.uniform(10, 10000), 2),
        "description": random.choice([
            "Salary deposit",
            "Refund",
            "Transfer from external account",
            "Investment return",
            "Gift"
        ])
    }

    url = f"{os.getenv('NESSIE_API_URL')}/accounts/{account_id}/deposits?key={os.getenv('NESSIE_API_KEY')}"
    # Send request
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(
            url,
            data=json.dumps(deposit_data),
            headers=headers
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating deposit: {str(e)}")
        return None
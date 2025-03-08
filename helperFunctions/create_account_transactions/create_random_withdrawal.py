import json
import os
from datetime import datetime, timedelta
import random
import requests
from dotenv import load_dotenv


def create_random_withdrawal(account_id):
    """Create a random withdrawal for a specific account"""
    load_dotenv()
    withdrawal_data = {
        "medium": "balance",
        "transaction_date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
        "status": random.choice(["pending", "completed", "cancelled"]),
        "amount": round(random.uniform(10, 1000), 2),
        "description": random.choice([
            "ATM withdrawal",
            "Cash back",
            "Bill payment",
            "Transfer to external account",
            "Check withdrawal"
        ])
    }

    url = f"{os.getenv("NESSIE_API_URL")}/accounts/{account_id}/withdrawals?key={os.getenv('NESSIE_API_KEY')}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(
            url,
            data=json.dumps(withdrawal_data),
            headers=headers
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating withdrawal: {str(e)}")
        return None
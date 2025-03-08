import json
import os
from datetime import datetime, timedelta
from random import random
import requests
from dotenv import load_dotenv


def create_random_transfer(payer_account_id, payee_account_id):
    """Create a random transfer between two accounts"""
    load_dotenv()
    transfer_data = {
        "medium": "balance",
        "payee_id": payee_account_id,
        "amount": round(random.uniform(10, 1000), 2),
        "transaction_date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
        "status": "pending",  # API only accepts "pending"
        "description": random.choice([
            "Monthly transfer",
            "Debt payment",
            "Shared expense",
            "Family support",
            "Savings transfer"
        ])
    }

    url = f"{os.getenv("NESSIE_API_URL")}/accounts/{payer_account_id}/transfers?key={os.getenv("NESSIE_API_KEY")}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(
            url,
            data=json.dumps(transfer_data),
            headers=headers
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating transfer: {str(e)}")
        return None
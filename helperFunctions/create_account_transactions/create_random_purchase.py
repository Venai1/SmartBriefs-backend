import json
import os
import random
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv


def create_random_purchase(account_id, merchant_id):
    """Create a random purchase for a specific account with a merchant"""
    load_dotenv()
    purchase_data = {
        "merchant_id": merchant_id,
        "medium": "balance",
        "purchase_date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
        "amount": round(random.uniform(5, 1000), 2),
        "status": random.choice(["pending", "completed", "cancelled"]),
        "description": random.choice([
            "Grocery shopping",
            "Electronics",
            "Clothing",
            "Dining",
            "Entertainment",
            "Transportation",
            "Services"
        ])
    }

    url = f"{os.getenv('NESSIE_API_URL')}/accounts/{account_id}/purchases?key={os.getenv('NESSIE_API_KEY')}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(
            url,
            data=json.dumps(purchase_data),
            headers=headers
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating purchase: {str(e)}")
        return None
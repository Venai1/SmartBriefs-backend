import json
import os
import random
import string
import requests
from dotenv import load_dotenv


def create_random_account(customer_id):
    """Create a random account for a specific customer"""
    load_dotenv()

    account_types = ["Checking", "Savings", "Credit Card"]

    nicknames = ["Primary", "Secondary", "Emergency Fund", "Vacation",
                 "Home Savings", "Daily Expenses", "Travel", "Education"]

    account_number = ''.join(random.choices(string.digits, k=16))

    account_data = {
        "type": random.choice(account_types),
        "nickname": random.choice(nicknames),
        "rewards": random.randint(0, 10000),
        "balance": random.randint(1000, 50000),
        "account_number": account_number
    }

    url = f"{os.getenv("NESSIE_API_URL")}/customers/{customer_id}/accounts?key={os.getenv("NESSIE_API_KEY")}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(
            url,
            data=json.dumps(account_data),
            headers=headers
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating account: {str(e)}")
        return None
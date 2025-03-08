import requests
from dotenv import load_dotenv
from faker import Faker
import random
import json
import os

def create_random_merchants():
    """Create a random merchant using Faker"""
    fake = Faker()
    load_dotenv()
    merchant_data = {
        "name": fake.company(),
        "category": random.choice([
            "Food", "Retail", "Entertainment", "Healthcare",
            "Transportation", "Utilities", "Education"
        ]),
        "address": {
            "street_number": fake.building_number(),
            "street_name": fake.street_name(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip": fake.zipcode()
        },
        "geocode": {
            "lat": float(fake.latitude()),
            "lng": float(fake.longitude())
        }
    }

    # API endpoint for creating a merchant
    url = f"{os.getenv("NESSIE_API_URL")}/merchants?key={os.getenv("NESSIE_API_KEY")}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(
            url,
            data=json.dumps(merchant_data),
            headers=headers
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating merchant: {str(e)}")
        return None
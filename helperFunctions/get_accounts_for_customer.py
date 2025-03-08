import os
import requests
from dotenv import load_dotenv

def get_accounts_for_customer(customer_id):
    """Get all accounts for a customer"""
    load_dotenv()
    url = f"{os.getenv("NESSIE_API_URL")}/customers/{customer_id}/accounts?key={os.getenv("NESSIE_API_KEY")}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting accounts: {str(e)}")
        return []
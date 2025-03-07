import random
import string
import requests
import json
import time
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()

# API Constants
API_URL = "http://api.nessieisreal.com"
API_KEY = "9699a5b7260039b6a8fac75cf9dae5d0"

def create_random_account(customer_id):
    """Create a random account for a specific customer"""
    
    # Account types available in the Nessie API
    account_types = ["Checking", "Savings", "Credit Card"]
    
    # Generate a random nickname (e.g. "My Savings", "Emergency Fund")
    nicknames = ["Primary", "Secondary", "Emergency Fund", "Vacation", 
                "Home Savings", "Daily Expenses", "Travel", "Education"]
    
    # Generate random account number
    account_number = ''.join(random.choices(string.digits, k=16))
    
    # Create random account data
    account_data = {
        "type": random.choice(account_types),
        "nickname": random.choice(nicknames),
        "rewards": random.randint(0, 10000),
        "balance": random.randint(1000, 50000),
        "account_number": account_number
    }
    
    # API endpoint for creating an account for a customer
    url = f"{API_URL}/customers/{customer_id}/accounts?key={API_KEY}"
    
    # Send request to create account
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

def create_random_deposit(account_id):
    """Create a random deposit for a specific account"""
    
    # Generate random deposit data
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
    
    # API endpoint for creating a deposit
    url = f"{API_URL}/accounts/{account_id}/deposits?key={API_KEY}"
    
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

def create_random_loan(account_id):
    """Create a random loan for a specific account"""
    
    # Generate random loan data
    loan_data = {
        "type": "home",  # API seems to only accept "home"
        "status": "pending",  # API seems to only accept "pending"
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
    url = f"{API_URL}/accounts/{account_id}/loans?key={API_KEY}"
    
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

def create_random_merchant():
    """Create a random merchant using Faker"""
    
    # Generate random merchant data
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
    url = f"{API_URL}/merchants?key={API_KEY}"
    
    # Send request
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

def create_random_purchase(account_id, merchant_id):
    """Create a random purchase for a specific account with a merchant"""
    
    # Generate random purchase data
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
    
    # API endpoint for creating a purchase
    url = f"{API_URL}/accounts/{account_id}/purchases?key={API_KEY}"
    
    # Send request
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

def create_random_withdrawal(account_id):
    """Create a random withdrawal for a specific account"""
    
    # Generate random withdrawal data
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
    
    # API endpoint for creating a withdrawal
    url = f"{API_URL}/accounts/{account_id}/withdrawals?key={API_KEY}"
    
    # Send request
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

def create_random_transfer(payer_account_id, payee_account_id):
    """Create a random transfer between two accounts"""
    
    # Generate random transfer data
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
    
    # API endpoint for creating a transfer
    url = f"{API_URL}/accounts/{payer_account_id}/transfers?key={API_KEY}"
    
    # Send request
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

def get_accounts_for_customer(customer_id):
    """Get all accounts for a customer"""
    url = f"{API_URL}/customers/{customer_id}/accounts?key={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting accounts: {str(e)}")
        return []

def populate_account_with_transactions(account_id, other_account_ids=None):
    """Populate an account with various random transactions"""
    
    # Create 2-4 deposits
    num_deposits = random.randint(2, 4)
    for _ in range(num_deposits):
        try:
            create_random_deposit(account_id)
            # Small delay to avoid rate limiting
            time.sleep(0.2)
        except Exception as e:
            print(f"Error with deposit: {str(e)}")
    
    # Create 0-1 loans (25% chance)
    try:
        if random.random() < 0.25:  # 25% chance of creating a loan
            create_random_loan(account_id)
            time.sleep(0.2)
    except Exception as e:
        print(f"Error with loan: {str(e)}")
    
    # Create 5-10 merchants and associated purchases
    try:
        num_merchants = random.randint(5, 10)
        for _ in range(num_merchants):
            merchant_response = create_random_merchant()
            time.sleep(0.2)
            if merchant_response and 'objectCreated' in merchant_response:
                merchant_id = merchant_response['objectCreated']['_id']
                
                # Create 3-8 purchases per merchant
                num_purchases = random.randint(3, 8)
                for _ in range(num_purchases):
                    create_random_purchase(account_id, merchant_id)
                    time.sleep(0.2)
    except Exception as e:
        print(f"Error with merchant/purchase: {str(e)}")
    
    # Create 2-3 withdrawals
    try:
        num_withdrawals = random.randint(2, 3)
        for _ in range(num_withdrawals):
            create_random_withdrawal(account_id)
            time.sleep(0.2)
    except Exception as e:
        print(f"Error with withdrawal: {str(e)}")
    
    # Create 1-3 transfers if other accounts are available
    if other_account_ids and len(other_account_ids) > 0:
        try:
            num_transfers = random.randint(1, 3)
            for _ in range(num_transfers):
                payee_id = random.choice(other_account_ids)
                create_random_transfer(account_id, payee_id)
                time.sleep(0.2)
        except Exception as e:
            print(f"Error with transfer: {str(e)}")

def generate_accounts_for_customer(customer_id):
    """Generate multiple random accounts with transactions for a customer"""
    num_accounts = random.randint(2, 5)
    created_accounts = []
    
    print(f"Creating {num_accounts} accounts for customer {customer_id}...")
    
    for i in range(num_accounts):
        print(f"  Creating account {i+1}/{num_accounts}...")
        result = create_random_account(customer_id)
        if result and 'objectCreated' in result:
            account_id = result['objectCreated']['_id']
            created_accounts.append(account_id)
    
    print(f"Populating {len(created_accounts)} accounts with transactions...")
    
    # Add transactions to each account
    for i, account_id in enumerate(created_accounts):
        print(f"  Populating account {i+1}/{len(created_accounts)}...")
        # Pass all accounts except the current one as potential transfer targets
        other_accounts = [acc_id for acc_id in created_accounts if acc_id != account_id]
        populate_account_with_transactions(account_id, other_accounts)
        # Add a small delay to avoid rate limiting
        time.sleep(0.5)
    
    print(f"Successfully created and populated {len(created_accounts)} accounts for customer {customer_id}")
    return created_accounts

def fill_accounts_with_data(customer_id):
    """Main function to fill accounts with data for a specific customer"""
    print(f"Starting to fill accounts with data for customer {customer_id}")
    
    # First, check if the customer already has accounts
    existing_accounts = get_accounts_for_customer(customer_id)
    
    if existing_accounts and len(existing_accounts) > 0:
        print(f"Customer {customer_id} already has {len(existing_accounts)} accounts")
        
        # Option to add transactions to existing accounts
        account_ids = [account['_id'] for account in existing_accounts]
        
        for i, account_id in enumerate(account_ids):
            print(f"  Populating existing account {i+1}/{len(account_ids)}...")
            other_accounts = [acc_id for acc_id in account_ids if acc_id != account_id]
            populate_account_with_transactions(account_id, other_accounts)
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
    else:
        # Create new accounts with transactions
        generate_accounts_for_customer(customer_id)
    
    print(f"Finished filling accounts with data for customer {customer_id}")

# Example usage
if __name__ == "__main__":
    # Example customer ID - replace with actual ID when testing
    test_customer_id = "67cb45929683f20dd518d063"
    fill_accounts_with_data(test_customer_id)
import time
from random import random

from helperFunctions.create_account_transactions.populate_account_with_transactions import \
    populate_account_with_transactions
from helperFunctions.create_accounts.create_random_account import create_random_account


def generate_accounts_for_customer(customer_id):
    """Generate multiple random accounts with transactions for a customer"""
    num_accounts = random.randint(2, 5)
    created_accounts = []

    print(f"Creating {num_accounts} accounts for customer {customer_id}...")

    for i in range(num_accounts):
        print(f"Creating account {i+1}/{num_accounts}...")
        result = create_random_account(customer_id)
        if result and 'objectCreated' in result:
            account_id = result['objectCreated']['_id']
            created_accounts.append(account_id)

    print(f"Populating {len(created_accounts)} accounts with transactions...")

    for i, account_id in enumerate(created_accounts):
        print(f"  Populating account {i+1}/{len(created_accounts)}...")
        other_accounts = [acc_id for acc_id in created_accounts if acc_id != account_id]
        populate_account_with_transactions(account_id, other_accounts)
        time.sleep(0.5)

    print(f"Successfully created and populated {len(created_accounts)} accounts for customer {customer_id}")
    return created_accounts
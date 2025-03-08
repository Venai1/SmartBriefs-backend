import time
from helperFunctions.create_account_transactions.populate_account_with_transactions import populate_account_with_transactions
from helperFunctions.create_accounts.generate_random_customer_accounts import generate_accounts_for_customer
from helperFunctions.get_accounts_for_customer import get_accounts_for_customer


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

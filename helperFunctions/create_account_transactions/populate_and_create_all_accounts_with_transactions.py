import time
from helperFunctions.create_account_transactions.populate_account_with_transactions import populate_account_with_transactions
from helperFunctions.create_accounts.generate_random_customer_accounts import generate_accounts_for_customer
from helperFunctions.get_accounts_for_customer import get_accounts_for_customer
from helperFunctions.create_accounts import generate_random_customer_accounts


def fill_accounts_with_data(customer_id):
    """Main function to fill accounts with data for a specific customer"""

    print(f"Starting to fill accounts with data for customer {customer_id}")

    # First, check if the customer already has accounts
    existing_accounts = get_accounts_for_customer(customer_id)

    if not existing_accounts:
         # Create new accounts with transactions
        generate_random_customer_accounts.generate_accounts_for_customer(customer_id)
 


    print(f"Finished filling accounts with data for customer {customer_id}")

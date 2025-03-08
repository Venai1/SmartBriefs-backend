import random
import time
from helperFunctions.create_account_transactions.create_random_deposit import create_random_deposit
from helperFunctions.create_account_transactions.create_random_loan import create_random_loan
from helperFunctions.create_account_transactions.create_random_merchants import create_random_merchants
from helperFunctions.create_account_transactions.create_random_purchase import create_random_purchase
from helperFunctions.create_account_transactions.create_random_transfer import create_random_transfer
from helperFunctions.create_account_transactions.create_random_withdrawal import create_random_withdrawal


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
            merchant_response = create_random_merchants()
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
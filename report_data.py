from helperFunctions.get_bank_data import BankDataManager
from helperFunctions.get_stocks_data import get_stocks_data
from helperFunctions.get_news_articles_and_summary import get_news_articles_and_summary
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from openai import OpenAI # Assuming this is installed for LLM summary
from datetime import datetime
import json
from datetime import datetime
import numpy as np

def get_customer_banking_summary(customer_id: str, timestamp: str = None) -> Dict[str, Any]:
    """
    Retrieves comprehensive banking data for a customer and organizes it into a structured dictionary.
    
    Parameters:
    - customer_id: ID of the customer
    - timestamp: Optional time period for filtering transactions (e.g., "1d", "7d", "30d")
    
    Returns:
    Dictionary with comprehensive customer financial data
    """
    # Initialize bank manager
    api_url = "http://api.nessieisreal.com"
    api_key = "9699a5b7260039b6a8fac75cf9dae5d0"
    bank_manager = BankDataManager(api_url, api_key)
    
    # Fetch all customer data
    bank_manager.fetch_customer_data(customer_id)
    
    # Initialize result dictionary
    result = {}
    
    # Get basic customer information
    if bank_manager.customers_df is not None and not bank_manager.customers_df.empty:
        customer_info = bank_manager.customers_df.iloc[0]
        result["first_name"] = customer_info['first_name']
        result["last_name"] = customer_info['last_name']
        result["name"] = f"{customer_info['first_name']} {customer_info['last_name']}".strip()
    else:
        result["first_name"] = "Unknown"
        result["last_name"] = "Customer"
        result["name"] = "Unknown Customer"
    
    # Get financial metrics
    result["net_worth"] = round(bank_manager.calculate_customer_net_worth(customer_id), 2)
    result["money_owed"] = round(bank_manager.calculate_total_debt(customer_id), 2)
    
    # Process transactions
    money_spent = 0
    money_added = 0
    largest_transactions = []
    largest_deposits = []
    
    if bank_manager.transactions_df is not None and not bank_manager.transactions_df.empty:
        transactions = bank_manager.transactions_df
        
        # Apply time filter if specified
        if timestamp:
            transactions['transaction_date'] = pd.to_datetime(
                transactions['transaction_date'], errors='coerce'
            )
            if timestamp.endswith('d'):
                days = int(timestamp[:-1])
                cutoff_date = datetime.now() - pd.Timedelta(days=days)
                transactions = transactions[transactions['transaction_date'] >= cutoff_date]
        
        # Calculate money spent (purchases, withdrawals)
        expenses = transactions[transactions['transaction_type'].isin(['purchase', 'withdrawal'])]
        if not expenses.empty:
            money_spent = round(expenses['amount'].sum(), 2)
        
        # Calculate money added (deposits)
        deposits = transactions[transactions['transaction_type'] == 'deposit']
        if not deposits.empty:
            money_added = round(deposits['amount'].sum(), 2)
        
        # Get largest transactions (by absolute amount)
        transactions_copy = transactions.copy()
        transactions_copy['abs_amount'] = transactions_copy['amount'].abs()
        transactions_copy = transactions_copy.sort_values('abs_amount', ascending=False)
        
        # Extract top 3 largest transactions
        if len(transactions_copy) > 0:
            largest_tx = transactions_copy[
                transactions_copy['transaction_type'].isin(['purchase', 'withdrawal'])
            ].head(3)
            
            if not largest_tx.empty:
                largest_transactions = largest_tx[['transaction_id', 'amount', 'description', 'transaction_date']].to_dict('records')
                # Format transaction dates to remove time
                for tx in largest_transactions:
                    if isinstance(tx['transaction_date'], str) and ' ' in tx['transaction_date']:
                        tx['transaction_date'] = tx['transaction_date'].split()[0]
                    elif hasattr(tx['transaction_date'], 'date'):
                        tx['transaction_date'] = tx['transaction_date'].date().isoformat()
        
        # Extract top 3 largest deposits
        if len(deposits) > 0:
            largest_deps = deposits.sort_values('amount', ascending=False).head(3)
            
            if not largest_deps.empty:
                largest_deposits = largest_deps[['transaction_id', 'amount', 'description', 'transaction_date']].to_dict('records')
                # Format deposit dates to remove time
                for dep in largest_deposits:
                    if isinstance(dep['transaction_date'], str) and ' ' in dep['transaction_date']:
                        dep['transaction_date'] = dep['transaction_date'].split()[0]
                    elif hasattr(dep['transaction_date'], 'date'):
                        dep['transaction_date'] = dep['transaction_date'].date().isoformat()
    
    result["money_spent"] = abs(money_spent)  # Use absolute value for readability
    result["money_added"] = money_added
    result["largest_transactions"] = largest_transactions
    result["largest_deposits"] = largest_deposits
    
    # Get account balances
    account_balances = {}
    if bank_manager.accounts_df is not None and not bank_manager.accounts_df.empty:
        accounts = bank_manager.accounts_df[bank_manager.accounts_df['customer_id'] == customer_id]
        for _, account in accounts.iterrows():
            account_balances[account['nickname'] or f"Account {account['account_id']}"] = round(account['balance'], 2)
    
    result["account_balances"] = account_balances
    
    # Generate LLM summary
    try:
        # Get transaction categories and frequencies if available
        transaction_categories = {}
        if bank_manager.transactions_df is not None and not bank_manager.transactions_df.empty:
            purchases = bank_manager.transactions_df[bank_manager.transactions_df['transaction_type'] == 'purchase']
            if not purchases.empty and 'description' in purchases.columns:
                transaction_categories = purchases['description'].value_counts().to_dict()
        
        # Format transaction categories for the prompt
        top_categories = ""
        if transaction_categories:
            top_3_categories = dict(sorted(transaction_categories.items(), key=lambda x: x[1], reverse=True)[:3])
            top_categories = ", ".join(f"{cat}" for cat in top_3_categories.keys())
        
        # Calculate spending trend
        spending_trend = ""
        if bank_manager.transactions_df is not None and not bank_manager.transactions_df.empty:
            purchases = bank_manager.transactions_df[bank_manager.transactions_df['transaction_type'] == 'purchase']
            if not purchases.empty and len(purchases) > 1:
                purchases = purchases.copy()  # Create explicit copy to avoid SettingWithCopyWarning
                purchases['transaction_date'] = pd.to_datetime(purchases['transaction_date'], errors='coerce')
                purchases = purchases.sort_values('transaction_date')
                
                # Split into two halves
                half_point = len(purchases) // 2
                first_half = purchases.iloc[:half_point]
                second_half = purchases.iloc[half_point:]
                
                first_half_total = first_half['amount'].sum()
                second_half_total = second_half['amount'].sum()
                
                if second_half_total > first_half_total:
                    spending_trend = "increasing"
                elif second_half_total < first_half_total:
                    spending_trend = "decreasing"
                else:
                    spending_trend = "stable"
        
        summary_prompt = (
            f"Create a friendly, personalized financial headline for a newsletter addressed directly to {result['name']}. "
            f"Reference their current financial situation (net worth: ${result['net_worth']:.2f}, recent spending: ${result['money_spent']:.2f}, "
            f"deposits: ${result['money_added']:.2f}{' in the specified time period' if timestamp else ''}, debt: ${result['money_owed']:.2f}) "
            f"but focus on insights rather than just numbers. Use 'you' instead of 'they'. Keep it to 2-3 engaging sentences."
        )
        
        if top_categories:
            summary_prompt += f"Their top spending categories include {top_categories}. "
        
        if spending_trend:
            summary_prompt += f"Their spending trend is {spending_trend}. "
            
        if largest_transactions and len(largest_transactions) > 0:
            summary_prompt += f"Their largest recent transaction was ${abs(largest_transactions[0]['amount']):.2f} for {largest_transactions[0]['description']}. "
        
        # Replace this with your actual OpenAI API key
        client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial assistant that summarizes banking data in 1-2 concise sentences."},
                {
                    "role": "user", 
                    "content": summary_prompt
                }
            ]
        )
        result["accounts_summary"] = response.choices[0].message.content.strip()
    except Exception as e:
        result["accounts_summary"] = (
            f"{result['name']} has a net worth of ${result['net_worth']:.2f} with ${result['money_owed']:.2f} in debt. "
            f"Recently {'spent' if result['money_spent'] > result['money_added'] else 'saved'} more than "
            f"{'earned' if result['money_spent'] > result['money_added'] else 'spent'}."
        )
    
    return result

def save_to_json(data, filename="customer_summary.json"):
    """Save data dictionary to a JSON file"""

    
    # Handle datetime objects, NumPy types, and other non-serializable types
    def json_serial(obj):
        if isinstance(obj, datetime):
            return obj.date().isoformat()  # Return only the date part
        elif isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(round(obj, 2))  # Round floats to 2 decimal places
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.bool_)):
            return bool(obj)
        elif isinstance(obj, float):
            return round(obj, 2)  # Round Python floats too
        raise TypeError(f"Type {type(obj)} not serializable")
    
    # Pre-process the data to round floating point values
    def round_floats_in_dict(data_dict):
        if not isinstance(data_dict, dict):
            return data_dict
            
        for key, value in data_dict.items():
            if isinstance(value, float):
                data_dict[key] = round(value, 2)
            elif isinstance(value, dict):
                data_dict[key] = round_floats_in_dict(value)
            elif isinstance(value, list):
                data_dict[key] = [
                    round_floats_in_dict(item) if isinstance(item, dict) else
                    round(item, 2) if isinstance(item, float) else item
                    for item in value
                ]
        return data_dict
    
    # Round all floats in the data dictionary
    rounded_data = round_floats_in_dict(data.copy())
    
    with open(filename, 'w') as f:
        json.dump(rounded_data, f, default=json_serial, indent=4)
    
    print(f"Data saved to {filename}")

def get_report_data(customer_id,time_period):
    summary = get_customer_banking_summary(customer_id, time_period)
    news_data = get_news_articles_and_summary()
    tickers = ["^GSPC","^DJI","^IXIC"]
    summary["stocks"] = get_stocks_data(tickers)
    summary["news_ai_summary"] = news_data["summary"]
    summary["news_articles"] = news_data["articles"]

    return summary


# Example usage
if __name__ == "__main__":
    customer_id = "67cb640c9683f20dd518d16f"
    time_period = "30d"
    
    summary = get_customer_banking_summary(customer_id, time_period)
    news_data = get_news_articles_and_summary()
    tickers = ["^GSPC","^DJI","^IXIC"]
    summary["stocks"] = get_stocks_data(tickers)
    summary["news_ai_summary"] = news_data["summary"]
    summary["news_articles"] = news_data["articles"]
    save_to_json(summary)
    
    # Print key information
    print(f"Customer: {summary['name']}")
    print(f"Summary: {summary['accounts_summary']}")
    print(f"Net Worth: ${summary['net_worth']:.2f}")
    print(f"Total Debt: ${summary['money_owed']:.2f}")
    print(f"Money Spent: ${summary['money_spent']:.2f}")
    print(f"Money Added: ${summary['money_added']:.2f}")
    
    print("\nAccount Balances:")
    for account, balance in summary['account_balances'].items():
        print(f"  {account}: ${balance:.2f}")
    
    print("\nLargest Transactions:")
    for tx in summary['largest_transactions']:
        print(f"  ${abs(tx['amount']):.2f} - {tx['description']} ({tx['transaction_date']})")
    
    print("\nLargest Deposits:")
    for dep in summary['largest_deposits']:
        print(f"  ${dep['amount']:.2f} - {dep['description']} ({dep['transaction_date']})")
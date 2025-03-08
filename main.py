import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from pprint import pprint 
from helperFunctions.create_account_transactions.populate_account_with_transactions import populate_account_with_transactions
from helperFunctions.generate_open_ai_summary import generate_open_ai_summary
from helperFunctions.get_bank_data import BankDataManager
from helperFunctions.get_news_articles_and_summary import get_news_articles_and_summary
from helperFunctions.get_stocks_data import get_stocks_data

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

tickers = ["^GSPC", "^DJI", "^IXIC"]

app = FastAPI()
load_dotenv()

class Address(BaseModel):
    street_number: str
    street_name: str
    city: str
    state: str
    zip: str

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    address: Address
    email: str
    frequency: str


@app.post("/register")
def register_user(request: RegisterRequest):
    user_ref = db.collection("users").document(request.email)
    user_doc = user_ref.get()
    
    if user_doc.exists:
        user_data = user_doc.to_dict()
        address = {
            "street_number": "",
            "street_name": "",
            "city": "",
            "state": "",
            "zip": ""
        }
        
        # If address exists in the stored user data, use it
        if "address" in user_data:
            address = {
                "street_number": user_data["address"].get("street_number", ""),
                "street_name": user_data["address"].get("street_name", ""),
                "city": user_data["address"].get("city", ""),
                "state": user_data["address"].get("state", ""),
                "zip": user_data["address"].get("zip", "")
            }
        
        return {
            "status": "success",
            "message": "Customer created and data saved to database",
            "capital_one_response": {
                "code": 201,
                "message": "Customer created",
                "objectCreated": {
                    "first_name": user_data.get("first_name"),
                    "last_name": user_data.get("last_name"),
                    "address": address,
                    "_id": user_data.get("customer_id")
                }
            },
            "database_data": user_data
        }
    

    capital_one_data = {
        "first_name": request.first_name,
        "last_name": request.last_name,
        "address": {
            "street_number": request.address.street_number,
            "street_name": request.address.street_name,
            "city": request.address.city,
            "state": request.address.state,
            "zip": request.address.zip
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        url = f"{os.getenv("NESSIE_API_URL")}/customers?key={os.getenv("NESSIE_API_KEY")}"
        response = requests.post(
            url,
            data=json.dumps(capital_one_data),
            headers=headers
        )
        
        response.raise_for_status()
        capital_one_response = response.json()
        
        customer_id = capital_one_response.get('objectCreated', {}).get('_id')
        
        if customer_id:
            user_data = {
                "customer_id": customer_id,
                "email": request.email,
                "frequency": request.frequency,
                "first_name": request.first_name,
                "last_name": request.last_name,
                "address": {
                    "street_number": request.address.street_number,
                    "street_name": request.address.street_name,
                    "city": request.address.city,
                    "state": request.address.state,
                    "zip": request.address.zip
                }
            }
            
            db.collection("users").document(request.email).set(user_data)
            populate_account_with_transactions(customer_id)
            
            return {
                "status": "success",
                "message": "Customer created and data saved to database",
                "capital_one_response": capital_one_response,
                "database_data": user_data
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to get customer ID from API response")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling Capital One API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving to database: {str(e)}")

@app.post("/get_all_user_data/{customer_id}")
def get_all_user_data(customer_id:str):
    bank_manager = BankDataManager(os.getenv("NESSIE_API_URL"), os.getenv("NESSIE_API_KEY"))
    timestamp = "30d"
    bank_manager.fetch_customer_data(customer_id)

    result = {}

    if bank_manager.customers_df is not None and not bank_manager.customers_df.empty:
        customer_info = bank_manager.customers_df.iloc[0]
        result["first_name"] = customer_info['first_name']
        result["last_name"] = customer_info['last_name']
        result["name"] = f"{customer_info['first_name']} {customer_info['last_name']}".strip()
    else:
        result["first_name"] = "Unknown"
        result["last_name"] = "Customer"
        result["name"] = "Unknown Customer"

    result["net_worth"] = round(bank_manager.calculate_customer_net_worth(customer_id), 2)
    result["money_owed"] = round(bank_manager.calculate_total_debt(customer_id), 2)

    money_spent = 0
    money_added = 0
    largest_transactions = []
    largest_deposits = []

    if bank_manager.transactions_df is not None and not bank_manager.transactions_df.empty:
        transactions = bank_manager.transactions_df

        if timestamp:
            transactions['transaction_date'] = pd.to_datetime(
                transactions['transaction_date'], errors='coerce'
            )
            if timestamp.endswith('d'):
                days = int(timestamp[:-1])
                cutoff_date = datetime.now() - pd.Timedelta(days=days)
                transactions = transactions[transactions['transaction_date'] >= cutoff_date]

        expenses = transactions[transactions['transaction_type'].isin(['purchase', 'withdrawal'])]
        if not expenses.empty:
            money_spent = round(expenses['amount'].sum(), 2)

        deposits = transactions[transactions['transaction_type'] == 'deposit']
        if not deposits.empty:
            money_added = round(deposits['amount'].sum(), 2)

        transactions_copy = transactions.copy()
        transactions_copy['abs_amount'] = transactions_copy['amount'].abs()
        transactions_copy = transactions_copy.sort_values('abs_amount', ascending=False)

        if len(transactions_copy) > 0:
            largest_tx = transactions_copy[
                transactions_copy['transaction_type'].isin(['purchase', 'withdrawal'])
            ].head(3)

            if not largest_tx.empty:
                largest_transactions = largest_tx[['transaction_id', 'amount', 'description', 'transaction_date']].to_dict('records')
                for tx in largest_transactions:
                    if isinstance(tx['transaction_date'], str) and ' ' in tx['transaction_date']:
                        tx['transaction_date'] = tx['transaction_date'].split()[0]
                    elif hasattr(tx['transaction_date'], 'date'):
                        tx['transaction_date'] = tx['transaction_date'].date().isoformat()

        if len(deposits) > 0:
            largest_deps = deposits.sort_values('amount', ascending=False).head(3)
            if not largest_deps.empty:
                largest_deposits = largest_deps[['transaction_id', 'amount', 'description', 'transaction_date']].to_dict('records')
                for dep in largest_deposits:
                    if isinstance(dep['transaction_date'], str) and ' ' in dep['transaction_date']:
                        dep['transaction_date'] = dep['transaction_date'].split()[0]
                    elif hasattr(dep['transaction_date'], 'date'):
                        dep['transaction_date'] = dep['transaction_date'].date().isoformat()

    result["money_spent"] = abs(money_spent)
    result["money_added"] = money_added
    result["largest_transactions"] = largest_transactions
    result["largest_deposits"] = largest_deposits

    account_balances = {}
    if bank_manager.accounts_df is not None and not bank_manager.accounts_df.empty:
        accounts = bank_manager.accounts_df[bank_manager.accounts_df['customer_id'] == customer_id]
        for _, account in accounts.iterrows():
            account_balances[account['nickname'] or f"Account {account['account_id']}"] = round(account['balance'], 2)

    result["account_balances"] = account_balances

    try:
        transaction_categories = {}
        if bank_manager.transactions_df is not None and not bank_manager.transactions_df.empty:
            purchases = bank_manager.transactions_df[bank_manager.transactions_df['transaction_type'] == 'purchase']
            if not purchases.empty and 'description' in purchases.columns:
                transaction_categories = purchases['description'].value_counts().to_dict()

        top_categories = ""
        if transaction_categories:
            top_3_categories = dict(sorted(transaction_categories.items(), key=lambda x: x[1], reverse=True)[:3])
            top_categories = ", ".join(f"{cat}" for cat in top_3_categories.keys())

        spending_trend = ""
        if bank_manager.transactions_df is not None and not bank_manager.transactions_df.empty:
            purchases = bank_manager.transactions_df[bank_manager.transactions_df['transaction_type'] == 'purchase']
            if not purchases.empty and len(purchases) > 1:
                purchases = purchases.copy()
                purchases['transaction_date'] = pd.to_datetime(purchases['transaction_date'], errors='coerce')
                purchases = purchases.sort_values('transaction_date')

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

        result["accounts_summary"] = generate_open_ai_summary(summary_prompt)
    except Exception as e:
        result["accounts_summary"] = (
            f"{result['name']} has a net worth of ${result['net_worth']:.2f} with ${result['money_owed']:.2f} in debt. "
            f"Recently {'spent' if result['money_spent'] > result['money_added'] else 'saved'} more than "
            f"{'earned' if result['money_spent'] > result['money_added'] else 'spent'}."
        )



    result["stocks"] = get_stocks_data(tickers)
    news_data = get_news_articles_and_summary()
    result["news_ai_summary"] = news_data["summary"]
    result["news_articles"] = news_data["articles"]

    pprint(result)
    return result
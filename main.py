import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yfinance as yf
import requests
import json
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from helperFunctions.generate_open_ai_summary import generate_open_ai_summary
from helperFunctions.get_bank_data import BankDataManager
from helperFunctions.get_news_articles_and_summary import get_news_articles_and_summary
from helperFunctions.get_stocks_data import get_stocks_data
from helperFunctions.create_account_transactions import populate_and_create_all_accounts_with_transactions
import generate_newsletter
from starlette.middleware.cors import CORSMiddleware
import send_email

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

tickers = ["^GSPC", "^DJI", "^IXIC"]

app = FastAPI()
load_dotenv()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This adds a root endpoint to prevent 404 errors
@app.get("/")
def read_root():
    """Root endpoint to provide API information"""
    return {
        "app": "Financial Newsletter API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": [
            "/register",
            "/get_all_user_data/{customer_id}",
            "/cron/send_weekly_newsletters",
            "/cron/send_monthly_newsletters",
            "/diagnostic/all"  # New diagnostic endpoint
        ]
    }
    
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

def convert_numpy_types(obj):
    """Convert numpy types to Python native types recursively in dictionaries and lists."""
    import numpy as np

    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, (np.int8, np.int16, np.int32, np.int64,
                          np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float16, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return convert_numpy_types(obj.tolist())
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.void):
        return None
    else:
        return obj

@app.post("/register")
def register_user(request: RegisterRequest):
    user_ref = db.collection("users").document(request.email)
    user_doc = user_ref.get()

    if user_doc.exists:
        # Existing user handling logic remains the same
        user_data = user_doc.to_dict()
        address = {
            "street_number": "",
            "street_name": "",
            "city": "",
            "state": "",
            "zip": ""
        }

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
            "message": "Customer already created",
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

    # Format state and zip code properly
    # State should be a valid 2-letter US state code
    state = request.address.state.upper()[:2]  # Ensure 2 letter state code
    if len(state) < 2:
        state = "CA"  # Default to California if invalid

    # Zip should be a valid 5-digit US zip code
    zip_code = request.address.zip
    # Keep only digits
    zip_digits = ''.join(c for c in zip_code if c.isdigit())
    # Ensure 5 digits, pad with zeros if needed
    if len(zip_digits) < 5:
        zip_code = zip_digits.zfill(5)  # Pad with leading zeros
    else:
        zip_code = zip_digits[:5]  # Take only first 5 digits

    # Prepare data for Capital One API - ensure it strictly follows API requirements
    capital_one_data = {
        "first_name": request.first_name,
        "last_name": request.last_name,
        "address": {
            "street_number": request.address.street_number,
            "street_name": request.address.street_name,
            "city": request.address.city,
            "state": state,  # Using formatted state
            "zip": zip_code  # Using formatted zip
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        # Get API details from environment variables
        api_url = os.getenv('NESSIE_API_URL', 'http://api.nessieisreal.com')
        api_key = os.getenv('NESSIE_API_KEY')

        # Debug prints - remove in production
        print(f"Using API URL: {api_url}")
        print(f"Using API Key: {api_key[:5]}...") # Print only first 5 chars for security

        # Construct URL with proper error handling
        if not api_url or not api_key:
            raise ValueError("Missing NESSIE_API_URL or NESSIE_API_KEY environment variables")

        # Ensure the URL is properly constructed
        if api_url.endswith('/'):
            api_url = api_url[:-1]  # Remove trailing slash if present

        url = f"{api_url}/customers?key={api_key}"

        # Debug the request before sending
        print(f"Making request to: {url}")
        print(f"With headers: {headers}")
        print(f"With data: {json.dumps(capital_one_data)}")

        # Make the request with proper error handling
        json_data = json.dumps(capital_one_data)
        response = requests.post(
            url,
            data=json_data,
            headers=headers
        )

        # Debug the response
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        # Handle response status code explicitly
        if response.status_code == 400:
            error_detail = f"Bad request to Capital One API. Response: {response.text}"
            print(error_detail)
            raise HTTPException(status_code=400, detail=error_detail)

        response.raise_for_status()

        # Parse JSON response - with error handling
        try:
            capital_one_response = response.json()
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail=f"Invalid JSON response from Capital One API: {response.text}"
            )

        # Extract customer ID with proper validation
        customer_id = capital_one_response.get('objectCreated', {}).get('_id')

        if not customer_id:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get customer ID from API response: {capital_one_response}"
            )

        # Use the formatted address values in the database too
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
                "state": state,  # Using formatted state
                "zip": zip_code  # Using formatted zip
            }
        }

        db.collection("users").document(request.email).set(user_data)
        populate_and_create_all_accounts_with_transactions.fill_accounts_with_data(customer_id)

                # Send the email newsletter
        date_range = "30d"  # Default to 30 days - adjust as needed based on your requirements
        send_email.send_financial_newsletter(
            customer_id=user_data["customer_id"], 
            date_range=date_range, 
            recipient_email=user_data["email"]
        )
        return {
            "status": "success",
            "message": "Customer created and data saved to database",
            "capital_one_response": capital_one_response,
            "database_data": user_data
        }

    except requests.exceptions.RequestException as e:
        error_detail = f"Error calling Capital One API: {str(e)}"
        print(error_detail)
        if hasattr(e, 'response') and e.response:
            error_detail += f" Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=error_detail)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/get_all_user_data/{customer_id}")
def get_all_user_data(customer_id:str):
    bank_manager = BankDataManager(os.getenv('NESSIE_API_URL'), os.getenv('NESSIE_API_KEY'))
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

    result = convert_numpy_types(result)

    generate_newsletter.generate_newsletter(result)

    return result

# Add this endpoint to your main.py file

@app.get("/cron/send_weekly_newsletters")
def send_weekly_newsletters():
    """
    Endpoint to be called by a cron job to send newsletters to all users
    with frequency set to "weekly".
    
    Returns:
        dict: Summary of the operation results
    """
    try:
        # Query Firestore for users with frequency="weekly"
        users_ref = db.collection("users")
        weekly_users_query = users_ref.where("frequency", "==", "weekly")
        weekly_users = weekly_users_query.get()
        
        results = {
            "total_users": 0,
            "successful": 0,
            "failed": 0,
            "errors": []
        }
        
        # Iterate through weekly users
        for user_doc in weekly_users:
            user_data = user_doc.to_dict()
            results["total_users"] += 1
            
            # Check if user has required fields
            if not user_data.get("email") or not user_data.get("customer_id"):
                error_msg = f"User {user_doc.id} missing email or customer_id"
                results["errors"].append(error_msg)
                results["failed"] += 1
                continue
            
            try:
                # Send weekly newsletter (7 days data)
                send_email.send_financial_newsletter(
                    customer_id=user_data["customer_id"],
                    date_range="7d",
                    recipient_email=user_data["email"]
                )
                results["successful"] += 1
            except Exception as e:
                error_msg = f"Failed to send newsletter to {user_data.get('email')}: {str(e)}"
                results["errors"].append(error_msg)
                results["failed"] += 1
                print(error_msg)
        
        # Add timestamp for logging purposes
        results["timestamp"] = datetime.now().isoformat()
        
        # Store the results in Firestore for monitoring
        try:
            db.collection("cron_logs").document(f"weekly_newsletter_{datetime.now().strftime('%Y%m%d_%H%M%S')}").set(results)
        except Exception as e:
            print(f"Failed to log cron results to Firestore: {str(e)}")
        
        return results
    
    except Exception as e:
        error_detail = f"Error processing weekly newsletters: {str(e)}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=error_detail)


@app.get("/cron/send_monthly_newsletters")
def send_monthly_newsletters():
    """
    Endpoint to be called by a cron job to send newsletters to all users
    with frequency set to "monthly".
    
    Returns:
        dict: Summary of the operation results
    """
    try:
        # Query Firestore for users with frequency="monthly"
        users_ref = db.collection("users")
        monthly_users_query = users_ref.where("frequency", "==", "monthly")
        monthly_users = monthly_users_query.get()
        
        results = {
            "total_users": 0,
            "successful": 0,
            "failed": 0,
            "errors": []
        }
        
        # Iterate through monthly users
        for user_doc in monthly_users:
            user_data = user_doc.to_dict()
            results["total_users"] += 1
            
            # Check if user has required fields
            if not user_data.get("email") or not user_data.get("customer_id"):
                error_msg = f"User {user_doc.id} missing email or customer_id"
                results["errors"].append(error_msg)
                results["failed"] += 1
                continue
            
            try:
                # Send monthly newsletter (30 days data)
                send_email.send_financial_newsletter(
                    customer_id=user_data["customer_id"],
                    date_range="30d",
                    recipient_email=user_data["email"]
                )
                results["successful"] += 1
            except Exception as e:
                error_msg = f"Failed to send newsletter to {user_data.get('email')}: {str(e)}"
                results["errors"].append(error_msg)
                results["failed"] += 1
                print(error_msg)
        
        # Add timestamp for logging purposes
        results["timestamp"] = datetime.now().isoformat()
        
        # Store the results in Firestore for monitoring
        try:
            db.collection("cron_logs").document(f"monthly_newsletter_{datetime.now().strftime('%Y%m%d_%H%M%S')}").set(results)
        except Exception as e:
            print(f"Failed to log cron results to Firestore: {str(e)}")
        
        return results
    
    except Exception as e:
        error_detail = f"Error processing monthly newsletters: {str(e)}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=error_detail)

# Add this diagnostic router directly in your main.py after your other endpoint definitions
@app.get("/test-network")
def test_network():
    """Test basic network connectivity"""
    results = {}
    
    # Test some common websites
    sites = [
        {"name": "Google", "url": "https://www.google.com"},
        {"name": "OpenAI", "url": "https://api.openai.com"}
    ]
    
    for site in sites:
        try:
            start_time = time.time()
            response = requests.get(site["url"], timeout=5)
            elapsed = time.time() - start_time
            results[site["name"]] = {
                "status": response.status_code,
                "success": response.status_code == 200,
                "time_ms": round(elapsed * 1000, 2)
            }
        except Exception as e:
            results[site["name"]] = {
                "success": False,
                "error": str(e)
            }
    
    # Test DNS resolution
    domains = ["api.openai.com", "query1.finance.yahoo.com"]
    for domain in domains:
        try:
            ip = socket.gethostbyname(domain)
            results[f"DNS {domain}"] = {
                "success": True,
                "ip": ip
            }
        except Exception as e:
            results[f"DNS {domain}"] = {
                "success": False,
                "error": str(e)
            }
    
    return results

@app.get("/test-all-apis")
def test_all_apis():
    """Test all external APIs"""
    results = {}
    
    # Test OpenAI
    try:
        api_key = os.getenv("OPEN_AI_API_KEY")
        results["openai"] = {
            "api_key_configured": str(api_key)
        }
    except Exception as e:
        results["openai"] = {"error": str(e)}
    
    # Test Yahoo Finance
    try:
        for ticker in ["AAPL", "^GSPC"]:
            results[f"yahoo_finance_{ticker}"] = {"test_started": True}
            if has_yfinance:
                try:
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period="1d")
                    results[f"yahoo_finance_{ticker}"]["success"] = not hist.empty
                except Exception as e:
                    results[f"yahoo_finance_{ticker}"]["error"] = str(e)
            else:
                results[f"yahoo_finance_{ticker}"]["error"] = "yfinance not imported"
    except Exception as e:
        results["yahoo_finance"] = {"error": str(e)}
    
    # Test Resend
    try:
        api_key = os.getenv("RESEND_API_KEY")
        results["resend"] = {
            "api_key_configured": str(api_key)
        }
    except Exception as e:
        results["resend"] = {"error": str(e)}
    
    # Test Firebase
    try:
        results["firebase"] = {
            "client_initialized": db is not None,
            "service_account_file": os.path.get("serviceAccountKey.json")
        }
    except Exception as e:
        results["firebase"] = {"error": str(e)}
    
    return results
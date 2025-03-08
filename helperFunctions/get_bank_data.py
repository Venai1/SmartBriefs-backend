import requests
import pandas as pd
from datetime import datetime
import json
from typing import Dict

class BankDataManager:
    """Class to manage banking data retrieval and organization"""
    
    def __init__(self, api_url: str, api_key: str):
        """Initialize with API credentials"""
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Data storage
        self.customers_df = None
        self.accounts_df = None
        self.transactions_df = None
        self.merchants_df = None
        self.loans_df = None
        
    def _make_api_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Make an API request to the Nessie API"""
        url = f"{self.api_url}/{endpoint}?key={self.api_key}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, data=json.dumps(data) if data else None)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request error: {str(e)}")
            return {}
    
    def get_customer(self, customer_id: str) -> pd.DataFrame:
        """Retrieve a specific customer by ID and return as DataFrame"""
        customer = self._make_api_request(f"customers/{customer_id}")
        
        if not customer:
            return pd.DataFrame()
        
        # Create a record for the customer
        record = {
            "customer_id": customer.get("_id", ""),
            "first_name": customer.get("first_name", ""),
            "last_name": customer.get("last_name", "")
        }
        
        # Extract address if present
        address = customer.get("address", {})
        if address:
            record.update({
                "street_number": address.get("street_number", ""),
                "street_name": address.get("street_name", ""),
                "city": address.get("city", ""),
                "state": address.get("state", ""),
                "zip": address.get("zip", "")
            })
        
        # Create DataFrame with single customer
        self.customers_df = pd.DataFrame([record])
        return self.customers_df
    
    def get_customer_accounts(self, customer_id: str) -> pd.DataFrame:
        """Retrieve all accounts for a specific customer"""
        accounts = self._make_api_request(f"customers/{customer_id}/accounts")
        
        if not accounts:
            return pd.DataFrame()
        
        account_records = []
        for account in accounts:
            record = {
                "account_id": account.get("_id", ""),
                "customer_id": account.get("customer_id", ""),
                "type": account.get("type", ""),
                "nickname": account.get("nickname", ""),
                "rewards": account.get("rewards", 0),
                "balance": account.get("balance", 0),
                "account_number": account.get("account_number", "")
            }
            account_records.append(record)
            
        customer_accounts_df = pd.DataFrame(account_records)
        
        # Update accounts_df or create if it doesn't exist
        if self.accounts_df is None:
            self.accounts_df = customer_accounts_df
        else:
            self.accounts_df = pd.concat([self.accounts_df, customer_accounts_df], ignore_index=True)
            
        return customer_accounts_df
    
    def get_account_transactions(self, account_id: str) -> Dict[str, pd.DataFrame]:
        """Get all transaction types for an account"""
        
        transaction_types = {
            "deposits": self._get_account_deposits,
            "withdrawals": self._get_account_withdrawals,
            "transfers": self._get_account_transfers,
            "purchases": self._get_account_purchases
        }
        
        all_transactions = {}
        for tx_type, getter_method in transaction_types.items():
            transactions_df = getter_method(account_id)
            if not transactions_df.empty:
                all_transactions[tx_type] = transactions_df
                
                # Update the combined transactions dataframe
                if self.transactions_df is None:
                    self.transactions_df = transactions_df
                else:
                    self.transactions_df = pd.concat([self.transactions_df, transactions_df], ignore_index=True)
        
        return all_transactions
    
    def _get_account_deposits(self, account_id: str) -> pd.DataFrame:
        """Get all deposits for an account"""
        deposits = self._make_api_request(f"accounts/{account_id}/deposits")
        
        if not deposits:
            return pd.DataFrame()
        
        deposit_records = []
        for deposit in deposits:
            record = {
                "transaction_id": deposit.get("_id", ""),
                "account_id": account_id,
                "transaction_type": "deposit",
                "amount": deposit.get("amount", 0),
                "description": deposit.get("description", ""),
                "transaction_date": deposit.get("transaction_date", ""),
                "status": deposit.get("status", ""),
                "medium": deposit.get("medium", ""),
                "payee_id": deposit.get("payee_id", "")
            }
            deposit_records.append(record)
            
        return pd.DataFrame(deposit_records)
    
    def _get_account_withdrawals(self, account_id: str) -> pd.DataFrame:
        """Get all withdrawals for an account"""
        withdrawals = self._make_api_request(f"accounts/{account_id}/withdrawals")
        
        if not withdrawals:
            return pd.DataFrame()
        
        withdrawal_records = []
        for withdrawal in withdrawals:
            record = {
                "transaction_id": withdrawal.get("_id", ""),
                "account_id": account_id,
                "transaction_type": "withdrawal",
                "amount": withdrawal.get("amount", 0),
                "description": withdrawal.get("description", ""),
                "transaction_date": withdrawal.get("transaction_date", ""),
                "status": withdrawal.get("status", ""),
                "medium": withdrawal.get("medium", ""),
                "payer_id": withdrawal.get("payer_id", "")
            }
            withdrawal_records.append(record)
            
        return pd.DataFrame(withdrawal_records)
    
    def _get_account_transfers(self, account_id: str) -> pd.DataFrame:
        """Get all transfers for an account"""
        transfers = self._make_api_request(f"accounts/{account_id}/transfers")
        
        if not transfers:
            return pd.DataFrame()
        
        transfer_records = []
        for transfer in transfers:
            record = {
                "transaction_id": transfer.get("_id", ""),
                "account_id": account_id,
                "transaction_type": "transfer",
                "amount": transfer.get("amount", 0) if "amount" in transfer else 0,
                "description": transfer.get("description", ""),
                "transaction_date": transfer.get("transaction_date", ""),
                "status": transfer.get("status", ""),
                "medium": transfer.get("medium", ""),
                "payer_id": transfer.get("payer_id", ""),
                "payee_id": transfer.get("payee_id", "")
            }
            transfer_records.append(record)
            
        return pd.DataFrame(transfer_records)
    
    def _get_account_purchases(self, account_id: str) -> pd.DataFrame:
        """Get all purchases for an account"""
        purchases = self._make_api_request(f"accounts/{account_id}/purchases")
        
        if not purchases:
            return pd.DataFrame()
        
        purchase_records = []
        for purchase in purchases:
            record = {
                "transaction_id": purchase.get("_id", ""),
                "account_id": account_id,
                "transaction_type": "purchase",
                "amount": purchase.get("amount", 0),
                "description": purchase.get("description", ""),
                "transaction_date": purchase.get("purchase_date", ""),
                "status": purchase.get("status", ""),
                "medium": purchase.get("medium", ""),
                "merchant_id": purchase.get("merchant_id", ""),
                "payer_id": purchase.get("payer_id", "")
            }
            purchase_records.append(record)
            
        return pd.DataFrame(purchase_records)
    
    def get_merchant_info(self, merchant_id: str) -> Dict:
        """Get merchant information"""
        return self._make_api_request(f"merchants/{merchant_id}")
    
    def get_account_loans(self, account_id: str) -> pd.DataFrame:
        """Get loans associated with an account"""
        loans = self._make_api_request(f"accounts/{account_id}/loans")
        
        if not loans:
            return pd.DataFrame()
        
        loan_records = []
        for loan in loans:
            record = {
                "loan_id": loan.get("_id", ""),
                "account_id": account_id,
                "type": loan.get("type", ""),
                "status": loan.get("status", ""),
                "credit_score": loan.get("credit_score", 0),
                "monthly_payment": loan.get("monthly_payment", 0),
                "amount": loan.get("amount", 0),
                "description": loan.get("description", ""),
                "creation_date": loan.get("creation_date", "")
            }
            loan_records.append(record)
            
        loans_df = pd.DataFrame(loan_records)
        
        # Update loans_df or create if it doesn't exist
        if self.loans_df is None:
            self.loans_df = loans_df
        else:
            self.loans_df = pd.concat([self.loans_df, loans_df], ignore_index=True)
            
        return loans_df
    
    def get_all_merchant_data(self) -> pd.DataFrame:
        """Get all merchant data and store in DataFrame"""
        merchants = self._make_api_request("merchants")
        
        if not merchants:
            return pd.DataFrame()
        
        merchant_records = []
        for merchant in merchants:
            record = {
                "merchant_id": merchant.get("_id", ""),
                "name": merchant.get("name", ""),
                "category": merchant.get("category", "")
            }
            
            # Extract address if present
            address = merchant.get("address", {})
            if address:
                record.update({
                    "street_number": address.get("street_number", ""),
                    "street_name": address.get("street_name", ""),
                    "city": address.get("city", ""),
                    "state": address.get("state", ""),
                    "zip": address.get("zip", "")
                })
                
            # Extract geocode if present
            geocode = merchant.get("geocode", {})
            if geocode:
                record.update({
                    "latitude": geocode.get("lat", 0),
                    "longitude": geocode.get("lng", 0)
                })
                
            merchant_records.append(record)
            
        self.merchants_df = pd.DataFrame(merchant_records)
        return self.merchants_df
    
    def fetch_customer_data(self, customer_id: str) -> Dict[str, pd.DataFrame]:
        """Fetch all data for a single customer"""
        # Reset data storage to ensure we only have this customer's data
        self.customers_df = None
        self.accounts_df = None
        self.transactions_df = None
        self.loans_df = None
        
        # Get customer info directly
        self.customers_df = self.get_customer(customer_id)
        
        # Get accounts
        accounts_df = self.get_customer_accounts(customer_id)
        
        if accounts_df.empty:
            print(f"No accounts found for customer {customer_id}")
            return {
                "customers": self.customers_df if self.customers_df is not None else pd.DataFrame(),
                "accounts": pd.DataFrame(),
                "transactions": pd.DataFrame(),
                "loans": pd.DataFrame()
            }
        
        # For each account, get transactions and loans
        for account_id in accounts_df['account_id']:
            self.get_account_transactions(account_id)
            self.get_account_loans(account_id)
        
        # Get merchant data for any purchases
        if self.transactions_df is not None and not self.transactions_df.empty:
            # Check if there are any purchases
            purchases = self.transactions_df[self.transactions_df['transaction_type'] == 'purchase']
            if not purchases.empty:
                # Get unique merchant IDs
                merchant_ids = purchases['merchant_id'].unique()
                merchant_data = []
                
                # Get merchant info for each ID
                for merchant_id in merchant_ids:
                    if merchant_id:  # Skip empty merchant_ids
                        merchant_info = self.get_merchant_info(merchant_id)
                        if merchant_info:
                            merchant_data.append(merchant_info)
                
                # Create merchants DataFrame
                if merchant_data:
                    self.merchants_df = self.get_all_merchant_data()
        
        # Return all dataframes
        return {
            "customers": self.customers_df if self.customers_df is not None else pd.DataFrame(),
            "accounts": self.accounts_df if self.accounts_df is not None else pd.DataFrame(),
            "transactions": self.transactions_df if self.transactions_df is not None else pd.DataFrame(),
            "loans": self.loans_df if self.loans_df is not None else pd.DataFrame(),
            "merchants": self.merchants_df if self.merchants_df is not None else pd.DataFrame()
        }
    
    def calculate_customer_net_worth(self, customer_id: str) -> float:
        """Calculate net worth for a customer"""
        if self.accounts_df is None or self.accounts_df.empty:
            return 0
            
        # Get all accounts for this customer
        customer_accounts = self.accounts_df[self.accounts_df['customer_id'] == customer_id]
        
        if customer_accounts.empty:
            return 0
            
        # Sum balances from all accounts
        total_balance = customer_accounts['balance'].sum()
        
        # Subtract outstanding loans if available
        if self.loans_df is not None and not self.loans_df.empty:
            # Filter loans for customer's accounts
            customer_account_ids = customer_accounts['account_id'].tolist()
            customer_loans = self.loans_df[self.loans_df['account_id'].isin(customer_account_ids)]
            
            if not customer_loans.empty:
                # Only consider active loans
                active_loans = customer_loans[customer_loans['status'] != 'completed']
                if not active_loans.empty:
                    total_loan_amount = active_loans['amount'].sum()
                    total_balance -= total_loan_amount
        
        # Return without dividing by 100 - display the full value
        return total_balance
    
    def calculate_total_debt(self, customer_id: str) -> float:
        """Calculate total debt for a customer"""
        if self.loans_df is None or self.loans_df.empty:
            return 0
            
        # Get all accounts for this customer
        if self.accounts_df is None or self.accounts_df.empty:
            return 0
            
        customer_accounts = self.accounts_df[self.accounts_df['customer_id'] == customer_id]
        
        if customer_accounts.empty:
            return 0
            
        # Get account IDs for this customer
        customer_account_ids = customer_accounts['account_id'].tolist()
        
        # Filter loans for customer's accounts
        customer_loans = self.loans_df[self.loans_df['account_id'].isin(customer_account_ids)]
        
        if customer_loans.empty:
            return 0
            
        # Sum amounts from active loans
        active_loans = customer_loans[customer_loans['status'] != 'completed']
        if active_loans.empty:
            return 0
            
        # Return without dividing by 100 - display the full value
        return active_loans['amount'].sum()
    
    def get_transaction_summary(self, customer_id: str, time_period: str = None) -> pd.DataFrame:
        """
        Get a summary of transactions for a customer
        
        Parameters:
        - customer_id: ID of the customer
        - time_period: Optional period to filter (e.g., "30d" for last 30 days)
        
        Returns:
        DataFrame with transaction summary by type
        """
        if self.transactions_df is None or self.transactions_df.empty:
            return pd.DataFrame()
            
        # Get all accounts for this customer
        if self.accounts_df is None or self.accounts_df.empty:
            return pd.DataFrame()
            
        customer_accounts = self.accounts_df[self.accounts_df['customer_id'] == customer_id]
        
        if customer_accounts.empty:
            return pd.DataFrame()
            
        # Get account IDs for this customer
        customer_account_ids = customer_accounts['account_id'].tolist()
        
        # Filter transactions for customer's accounts
        customer_transactions = self.transactions_df[
            self.transactions_df['account_id'].isin(customer_account_ids)
        ]
        
        if customer_transactions.empty:
            return pd.DataFrame()
        
        # Apply time filter if specified
        if time_period:
            # Convert transaction_date to datetime
            customer_transactions['transaction_date'] = pd.to_datetime(
                customer_transactions['transaction_date'], errors='coerce'
            )
            
            # Parse time period format (e.g., "30d" for 30 days)
            if time_period.endswith('d'):
                days = int(time_period[:-1])
                cutoff_date = datetime.now() - pd.Timedelta(days=days)
                customer_transactions = customer_transactions[
                    customer_transactions['transaction_date'] >= cutoff_date
                ]
        
        # Group by transaction type and calculate stats
        summary = customer_transactions.groupby('transaction_type').agg({
            'amount': ['sum', 'mean', 'count'],
            'transaction_id': 'count'
        })
        
        # Flatten multi-level columns
        summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
        summary = summary.reset_index()
        
        return summary
    
    def to_dict_for_api(self, customer_id: str) -> Dict:
        """Format customer data for API consumption"""
        # Ensure we have data
        if (self.customers_df is None or self.accounts_df is None or 
            self.transactions_df is None):
            return {}
        
        # Get customer info
        customer_info = self.customers_df[self.customers_df['customer_id'] == customer_id]
        if customer_info.empty:
            return {}
        
        # Convert DataFrame to dict and handle NumPy types
        customer_data = json.loads(customer_info.iloc[0].to_json())
        
        # Get accounts
        accounts = self.accounts_df[self.accounts_df['customer_id'] == customer_id]
        if not accounts.empty:
            accounts_list = []
            
            for _, account in accounts.iterrows():
                account_id = account['account_id']
                # Convert account to dict with native Python types
                account_data = json.loads(account.to_json())
                
                # Get transactions for this account
                if self.transactions_df is not None and not self.transactions_df.empty:
                    account_transactions = self.transactions_df[
                        self.transactions_df['account_id'] == account_id
                    ]
                    
                    if not account_transactions.empty:
                        # Group transactions by type
                        transactions_by_type = {}
                        for tx_type, group in account_transactions.groupby('transaction_type'):
                            # Convert each transaction to dict with native Python types
                            tx_list = []
                            for _, tx in group.iterrows():
                                tx_list.append(json.loads(tx.to_json()))
                            transactions_by_type[tx_type] = tx_list
                            
                        account_data['transactions'] = transactions_by_type
                
                # Get loans for this account
                if self.loans_df is not None and not self.loans_df.empty:
                    account_loans = self.loans_df[self.loans_df['account_id'] == account_id]
                    
                    if not account_loans.empty:
                        # Convert loans to dict with native Python types
                        loan_list = []
                        for _, loan in account_loans.iterrows():
                            loan_list.append(json.loads(loan.to_json()))
                        account_data['loans'] = loan_list
                
                accounts_list.append(account_data)
            
            customer_data['accounts'] = accounts_list
        
        # Add net worth and total debt
        customer_data['net_worth'] = float(self.calculate_customer_net_worth(customer_id))
        customer_data['total_debt'] = float(self.calculate_total_debt(customer_id))
        
        # Add transaction summary
        transaction_summary = self.get_transaction_summary(customer_id)
        if not transaction_summary.empty:
            # Convert summary to dict with native Python types
            summary_list = []
            for _, summary in transaction_summary.iterrows():
                summary_list.append(json.loads(summary.to_json()))
            customer_data['transaction_summary'] = summary_list
        
        return customer_data

def process_customer(customer_id: str, time_period: str = None) -> Dict:
    """
    Process data for a single customer and return results
    
    Parameters:
    - customer_id: ID of the customer
    - time_period: Optional time period for filtering transactions (e.g., "1d", "7d", "30d")
    
    Returns:
    Dictionary with customer data and metrics
    """
    # Initialize the manager
    api_url = "http://api.nessieisreal.com"
    api_key = "9699a5b7260039b6a8fac75cf9dae5d0"
    
    bank_manager = BankDataManager(api_url, api_key)
    
    print(f"Processing data for customer ID: {customer_id}")
    if time_period:
        print(f"Using time filter: {time_period}")
    
    # Fetch data for just this customer
    data = bank_manager.fetch_customer_data(customer_id)
    
    # Filter transactions by time period if specified
    if time_period and data["transactions"] is not None and not data["transactions"].empty:
        # Convert transaction_date to datetime
        data["transactions"]['transaction_date'] = pd.to_datetime(
            data["transactions"]['transaction_date'], errors='coerce'
        )
        
        # Parse time period format (e.g., "30d" for 30 days)
        if time_period.endswith('d'):
            days = int(time_period[:-1])
            cutoff_date = datetime.now() - pd.Timedelta(days=days)
            data["transactions"] = data["transactions"][
                data["transactions"]['transaction_date'] >= cutoff_date
            ]
    
    # Calculate financial metrics with the same time filter
    net_worth = bank_manager.calculate_customer_net_worth(customer_id)
    total_debt = bank_manager.calculate_total_debt(customer_id)
    transaction_summary = bank_manager.get_transaction_summary(customer_id, time_period)
    
    # Format data for API
    api_data = bank_manager.to_dict_for_api(customer_id)
    
    # Return compiled results
    return {
        "data_tables": data,
        "financial_metrics": {
            "net_worth": net_worth,
            "total_debt": total_debt
        },
        "transaction_summary": transaction_summary,
        "api_data": api_data
    }

# Example usage:
if __name__ == "__main__":
    # Set the customer ID to process
    customer_id = "67cb640c9683f20dd518d16f"  # Replace with your target customer ID
    
    # Process the customer data with a time filter of 7 days
    time_period = "7d"  # Options: "1d", "7d", "30d", etc.
    
    # Process the customer data with the time filter
    result = process_customer(customer_id, time_period)
    
    # Print the data tables
    print("\nCUSTOMER INFO:")
    print(result["data_tables"]["customers"])
    
    print("\nACCOUNTS:")
    print(result["data_tables"]["accounts"])
    
    print("\nTRANSACTIONS:")
    if not result["data_tables"]["transactions"].empty:
        print(f"Found {len(result['data_tables']['transactions'])} transactions")
        print(f"These transactions are filtered for the last {time_period}")
        print(result["data_tables"]["transactions"].head())
    else:
        print(f"No transactions found in the last {time_period}")
    
    # Print financial metrics
    print(f"\nNet Worth: ${result['financial_metrics']['net_worth']:.2f}")
    print(f"Total Debt: ${result['financial_metrics']['total_debt']:.2f}")
    
    # Print transaction summary
    print("\nTransaction Summary:")
    print(result["transaction_summary"])
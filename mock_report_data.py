"""
Mock report_data module that provides sample data for testing the newsletter generator
"""

def get_report_data(customer_id, time_period):
    """
    Returns mock data for testing the newsletter generator
    """
    return {
        "name": "John Doe",
        "accounts_summary": "Your finances are looking strong this month, John. You've maintained steady spending while your investments have grown by 3.2%. Consider setting aside more for your emergency fund.",
        "net_worth": 124569.87,
        "money_spent": 3245.67,
        "money_added": 5678.90,
        "money_owed": 15432.10,
        "stocks": [
            {"ticker": "^GSPC", "name": "S&P 500", "price": 5123.45, "status": "Up"},
            {"ticker": "^DJI", "name": "Dow Jones", "price": 38765.32, "status": "Up"},
            {"ticker": "^IXIC", "name": "Nasdaq Composite", "price": 16432.10, "status": "Down"}
        ],
        "account_balances": {
            "Checking Account": 5678.90,
            "Savings Account": 28765.43,
            "Investment Account": 105557.64
        },
        "largest_transactions": [
            {"transaction_id": "tx123", "amount": -1234.56, "description": "Home Repair", "transaction_date": "2025-02-15"},
            {"transaction_id": "tx456", "amount": -876.54, "description": "Annual Insurance Premium", "transaction_date": "2025-02-10"},
            {"transaction_id": "tx789", "amount": -543.21, "description": "Electronics Purchase", "transaction_date": "2025-02-05"}
        ],
        "largest_deposits": [
            {"transaction_id": "dep123", "amount": 3456.78, "description": "Salary Deposit", "transaction_date": "2025-02-28"},
            {"transaction_id": "dep456", "amount": 1234.56, "description": "Tax Refund", "transaction_date": "2025-02-20"},
            {"transaction_id": "dep789", "amount": 567.89, "description": "Dividend Payment", "transaction_date": "2025-02-10"}
        ],
        "news_ai_summary": "Markets showed resilience this week despite inflation concerns. Tech stocks continued their rally while energy sectors saw moderate gains. Analysts remain cautiously optimistic about Q1 earnings season beginning next month.",
        "news_articles": [
            {
                "title": "Federal Reserve Signals Potential Rate Cut",
                "source": "Financial Times",
                "url": "https://example.com/news/1",
                "published_at": "2025-03-05T12:30:45Z"
            },
            {
                "title": "Tech Stocks Rally on AI Advancements",
                "source": "Wall Street Journal",
                "url": "https://example.com/news/2",
                "published_at": "2025-03-04T15:20:30Z"
            },
            {
                "title": "Housing Market Shows Signs of Cooling",
                "source": "Bloomberg",
                "url": "https://example.com/news/3",
                "published_at": "2025-03-03T09:15:22Z"
            },
            {
                "title": "Retail Sales Exceed Expectations in February",
                "source": "CNBC",
                "url": "https://example.com/news/4",
                "published_at": "2025-03-02T14:45:10Z"
            }
        ]
    }
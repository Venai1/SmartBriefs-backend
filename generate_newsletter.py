from datetime import datetime
import report_data
def generate_newsletter(data):
    """
    Generate an HTML financial newsletter from the provided data dictionary.
    
    Parameters:
    data (dict): Dictionary containing financial data with the same structure as customer_summary.json
    
    Returns:
    str: The generated HTML for the newsletter
    """
    # Format currency values
    def format_currency(amount):
        return f"${amount:,.2f}"

    # Generate HTML - using string concatenation instead of f-strings
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap" rel="stylesheet">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Newsletter - """ + data['name'] + """</title>
    <style>
        body {
            font-family: 'Merriweather', Georgia, serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }
        .header {
            text-align: center;
            padding: 30px 0;
            border-bottom: 1px solid #e0e0e0;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #2ca05a;
            margin-bottom: 5px;
            font-size: 36px;
        }
        .header p {
            color: #666;
            font-size: 18px;
            margin-top: 0;
        }
        .summary-box {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            font-size: 18px;
            margin-bottom: 30px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .summary-box h2 {
            margin-top: 0;
            color: #2ca05a;
        }
        .financial-overview {
            display: flex;
            flex-direction: column;
            margin-bottom: 30px;
        }
        .networth-card {
            padding: 25px;
            margin-bottom: 20px;
            width: 100%;
            text-align: center;
        }
        .networth-card h3 {
            margin-top: 0;
            color: #2ca05a;
            font-size: 20px;
        }
        .networth-card .amount {
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }
        .other-finances {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }
        .financial-card {
            padding: 20px;
            margin-bottom: 20px;
            flex: 1;
            min-width: 200px;
            margin-right: 15px;
            text-align: center;
        }
        .financial-card:last-child {
            margin-right: 0;
        }
        .financial-card h3 {
            margin-top: 0;
            color: #2ca05a;
            font-size: 18px;
        }
        .financial-card .amount {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            color: #2ca05a;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 10px;
        }
        .market-overview {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            margin-bottom: 30px;
        }
        .market-card {
            padding: 15px;
            margin-bottom: 15px;
            flex: 1;
            min-width: 200px;
            margin-right: 15px;
            text-align: center;
        }
        .market-card:last-child {
            margin-right: 0;
        }
        .market-card h3 {
            margin-top: 0;
            font-size: 16px;
        }
        .market-card .price {
            font-size: 20px;
            font-weight: bold;
        }
        .up {
            color: #28a745;
        }
        .down {
            color: #dc3545;
        }
        .accounts-table, .transactions-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        .accounts-table th, .accounts-table td,
        .transactions-table th, .transactions-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        .accounts-table th, .transactions-table th {
            background-color: #f5f5f5;
            font-weight: bold;
        }
        .accounts-table tr:last-child td,
        .transactions-table tr:last-child td {
            border-bottom: none;
        }
        .news-section {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .news-section h2 {
            color: #2ca05a;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 10px;
        }
        .news-summary {
            margin-bottom: 20px;
        }
        .news-articles {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .news-item {
            background-color: #f5f5f5;
            border-radius: 6px;
            padding: 10px;
            flex: 1 1 calc(50% - 15px);
            min-width: 250px;
        }
        .news-item h3 {
            margin-top: 0;
            margin-bottom: 5px;
            font-size: 16px;
        }
        .news-item p {
            margin: 5px 0;
            color: #666;
            font-size: 14px;
        }
        .news-item a {
            color: #2ca05a;
            text-decoration: none;
        }
        .news-item a:hover {
            text-decoration: underline;
        }
        .date {
            color: #888;
            font-size: 12px;
        }
        .footer {
            text-align: center;
            padding: 20px 0;
            margin-top: 30px;
            border-top: 1px solid #e0e0e0;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Financial Insights</h1>
        <p>Your personal financial newsletter - """ + datetime.now().strftime('%B %d, %Y') + """</p>
    </div>

    <div class="summary-box">
        <h2>Summary</h2>
        <p>""" + data['accounts_summary'] + """</p>
    </div>

    <div class="section">
        <h2>Financial Overview</h2>
        <div class="financial-overview">
            <div class="networth-card">
                <h3>Net Worth</h3>
                <div class="amount">""" + format_currency(data['net_worth']) + """</div>
            </div>
            <div class="other-finances">
                <div class="financial-card">
                    <h3>Money Spent</h3>
                    <div class="amount">""" + format_currency(data['money_spent']) + """</div>
                </div>
                <div class="financial-card">
                    <h3>Money Added</h3>
                    <div class="amount">""" + format_currency(data['money_added']) + """</div>
                </div>
                <div class="financial-card">
                    <h3>Money Owed</h3>
                    <div class="amount">""" + format_currency(data['money_owed']) + """</div>
                </div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>The Market</h2>
        <div class="market-overview">"""

    # Add stock market cards
    for stock in data['stocks']:
        price_color = "up" if stock['status'] == "Up" else "down"
        # Use stock name instead of ticker
        stock_name = stock.get('name', stock['ticker'])
        if stock_name == "^GSPC":
            stock_name = "S&P 500"
        elif stock_name == "^DJI":
            stock_name = "Dow Jones"
        elif stock_name == "^IXIC":
            stock_name = "Nasdaq Composite"
        html += """
            <div class="market-card">
                <h3>""" + stock_name + """</h3>
                <div class="price """ + price_color + """">""" + format_currency(stock['price']) + """</div>
            </div>
        """

    html += """
        </div>
    </div>

    <div class="section">
        <h2>Account Balances</h2>
        <table class="accounts-table">
            <thead>
                <tr>
                    <th>Account</th>
                    <th>Balance</th>
                </tr>
            </thead>
            <tbody>"""

    # Add account balances
    for account, balance in data['account_balances'].items():
        html += """
                <tr>
                    <td>""" + account + """</td>
                    <td>""" + format_currency(balance) + """</td>
                </tr>
        """

    html += """
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>Largest Transactions</h2>
        <table class="transactions-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Date</th>
                    <th>Description</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>"""

    # Add largest transactions with numbering
    for i, transaction in enumerate(data['largest_transactions'], 1):
        html += """
                <tr>
                    <td>""" + str(i) + """</td>
                    <td>""" + transaction['transaction_date'] + """</td>
                    <td>""" + transaction['description'] + """</td>
                    <td>""" + format_currency(transaction['amount']) + """</td>
                </tr>
        """

    html += """
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>Largest Deposits</h2>
        <table class="transactions-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Date</th>
                    <th>Description</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>"""

    # Add largest deposits with numbering
    for i, deposit in enumerate(data['largest_deposits'], 1):
        html += """
                <tr>
                    <td>""" + str(i) + """</td>
                    <td>""" + deposit['transaction_date'] + """</td>
                    <td>""" + deposit['description'] + """</td>
                    <td>""" + format_currency(deposit['amount']) + """</td>
                </tr>
        """

    html += """
            </tbody>
        </table>
    </div>

    <div class="news-section">
        <h2>Financial News</h2>
        <div class="news-summary">
            <p>""" + data['news_ai_summary'] + """</p>
        </div>
        <div class="news-articles">"""

    # Add news articles
    for article in data['news_articles']:
        published_date = datetime.strptime(article['published_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y")
        html += """
            <div class="news-item">
                <h3><a href=\"""" + article['url'] + """\" target="_blank">""" + article['title'] + """</a></h3>
                <p class="date">""" + article['source'] + """ · """ + published_date + """</p>
            </div>
        """

    html += """
        </div>
    </div>

    <div class="footer">
        <p>© 2025 Financial Insights Newsletter. All rights reserved.</p>
    </div>
</body>
</html>
    """
    
    return html


if __name__ == "__main__":
    # Example usage:
    import json
    
    # Load the JSON data (for demonstration purposes)
    customer_id = "67cbd8d99683f20dd518d75e"
    customer_data = report_data.get_report_data(customer_id, "30d")
    
    # Generate newsletter
    newsletter_html = generate_newsletter(customer_data)
    
    # Save the HTML to a file
    with open('financial_newsletter.html', 'w') as file:
        file.write(newsletter_html)
    
    print("Newsletter generated successfully! Open 'financial_newsletter.html' in your browser to view it.")
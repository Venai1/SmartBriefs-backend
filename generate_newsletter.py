from datetime import datetime

# Try to import the real module, fall back to mock if not available
try:
    import report_data
    print("Using real report_data module")
except ImportError:
    print("Real report_data module not found, using mock_report_data instead")
    import mock_report_data as report_data

def generate_newsletter(data):
    """
    Generate an email-friendly HTML financial newsletter from the provided data dictionary.
    
    Parameters:
    data (dict): Dictionary containing financial data with the same structure as customer_summary.json
    
    Returns:
    str: The generated HTML for the newsletter
    """
    # Format currency values
    def format_currency(amount):
        return f"${amount:,.2f}"

    # Generate HTML - using string concatenation for consistency with original code
    # Email-optimized version with inline styles and table-based layout
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="format-detection" content="telephone=no">
    <title>Penny - """ + data['name'] + """</title>
    <!--[if mso]>
    <style type="text/css">
        body, table, td {font-family: Arial, Helvetica, sans-serif !important;}
    </style>
    <![endif]-->
</head>
<body style="margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; line-height: 1.4; color: #f9f9f9; background-color: #0f1419;">
    <!-- Wrapper table for entire email - MSO conditional ensures Outlook compatibility -->
    <!--[if mso]>
    <table align="center" border="0" cellspacing="0" cellpadding="0" width="600">
    <tr>
    <td>
    <![endif]-->
    
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin: 0 auto; background-color: #0f1419;" role="presentation">
        <tr>
            <td align="center" style="padding: 20px;">
                <!-- Header -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #1a1f27; border-radius: 8px; margin-bottom: 20px;">
                    <tr>
                        <td align="center" style="padding: 30px 20px; border-bottom: 1px solid #2c3038;">
                            <table cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 10px;">
                                <tr>
                                    <td>
                                        <h1 style="color: #2ca05a; margin: 0; font-size: 38px; font-weight: bold;">Penny</h1>
                                    </td>
                                </tr>
                            </table>
                            <p style="color: #aaaaaa; font-size: 16px; margin-top: 5px;">Your personal finance assistant - """ + datetime.now().strftime('%B %d, %Y') + """</p>
                        </td>
                    </tr>
                </table>

                <!-- Summary Box -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #1a1f27; border-radius: 8px; margin-bottom: 20px;">
                    <tr>
                        <td style="padding: 20px;">
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px;">Summary</h2>
                            <p style="margin-top: 0; margin-bottom: 0; color: #f9f9f9; font-size: 18px;">""" + data['accounts_summary'] + """</p>
                        </td>
                    </tr>
                </table>

                <!-- Financial Overview -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                    <tr>
                        <td>
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px; border-bottom: 1px solid #2c3038; padding-bottom: 10px;">Financial Overview</h2>
                        </td>
                    </tr>
                    <!-- Net Worth -->
                    <tr>
                        <td>
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #1a1f27; border-radius: 8px; margin-bottom: 15px;">
                                <tr>
                                    <td align="center" style="padding: 20px;">
                                        <h3 style="color: #2ca05a; margin-top: 0; margin-bottom: 10px; font-size: 18px;">Net Worth</h3>
                                        <div style="font-size: 24px; font-weight: bold; color: #f9f9f9;">""" + format_currency(data['net_worth']) + """</div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Other Financial Cards -->
                    <tr>
                        <td>
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td width="33%" valign="top">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #1a1f27; border-radius: 8px; margin-right: 10px; margin-bottom: 15px;">
                                            <tr>
                                                <td align="center" style="padding: 15px;">
                                                    <h3 style="color: #2ca05a; margin-top: 0; margin-bottom: 10px; font-size: 16px;">Money Spent</h3>
                                                    <div style="font-size: 18px; font-weight: bold; color: #f9f9f9;">""" + format_currency(data['money_spent']) + """</div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                    <td width="33%" valign="top">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #1a1f27; border-radius: 8px; margin-right: 5px; margin-left: 5px; margin-bottom: 15px;">
                                            <tr>
                                                <td align="center" style="padding: 15px;">
                                                    <h3 style="color: #2ca05a; margin-top: 0; margin-bottom: 10px; font-size: 16px;">Money Added</h3>
                                                    <div style="font-size: 18px; font-weight: bold; color: #f9f9f9;">""" + format_currency(data['money_added']) + """</div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                    <td width="33%" valign="top">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #1a1f27; border-radius: 8px; margin-left: 10px; margin-bottom: 15px;">
                                            <tr>
                                                <td align="center" style="padding: 15px;">
                                                    <h3 style="color: #2ca05a; margin-top: 0; margin-bottom: 10px; font-size: 16px;">Money Owed</h3>
                                                    <div style="font-size: 18px; font-weight: bold; color: #f9f9f9;">""" + format_currency(data['money_owed']) + """</div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>

                <!-- Market Section -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                    <tr>
                        <td>
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px; border-bottom: 1px solid #2c3038; padding-bottom: 10px;">The Market</h2>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">
                                <tr>"""

    # Add stock market cards - using simpler layout for better email compatibility
    # Instead of trying to put all stocks in one row (which can cause layout issues),
    # we'll create a 2-column layout regardless of how many stocks there are
    
    # Start with an empty row
    html += """
                                </tr>
                            </table>
                            
                            <!-- Stock cards in a more email-friendly layout -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">"""
    
    # Create stock cards in rows of 2 columns
    stocks = data['stocks']
    for i in range(0, len(stocks), 2):
        html += """
                                <tr>"""
        
        # First column
        stock = stocks[i]
        price_color = "#28a745" if stock['status'] == "Up" else "#dc3545"
        stock_name = stock.get('name', stock['ticker'])
        if stock_name == "^GSPC":
            stock_name = "S&P 500"
        elif stock_name == "^DJI":
            stock_name = "Dow Jones"
        elif stock_name == "^IXIC":
            stock_name = "Nasdaq Composite"
            
        html += """
                                    <td width="50%" valign="top">
                                        <table width="95%" cellpadding="0" cellspacing="0" border="0" style="background-color: #1a1f27; border-radius: 8px; margin-right: 10px; margin-bottom: 15px;" role="presentation">
                                            <tr>
                                                <td align="center" style="padding: 15px;">
                                                    <h3 style="margin-top: 0; margin-bottom: 10px; font-size: 14px; color: #f9f9f9;">""" + stock_name + """</h3>
                                                    <div style="font-size: 16px; font-weight: bold; color: """ + price_color + """;">""" + format_currency(stock['price']) + """</div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>"""
        
        # Second column (if available)
        if i + 1 < len(stocks):
            stock = stocks[i + 1]
            price_color = "#28a745" if stock['status'] == "Up" else "#dc3545"
            stock_name = stock.get('name', stock['ticker'])
            if stock_name == "^GSPC":
                stock_name = "S&P 500"
            elif stock_name == "^DJI":
                stock_name = "Dow Jones"
            elif stock_name == "^IXIC":
                stock_name = "Nasdaq Composite"
                
            html += """
                                    <td width="50%" valign="top">
                                        <table width="95%" cellpadding="0" cellspacing="0" border="0" style="background-color: #1a1f27; border-radius: 8px; margin-left: 10px; margin-bottom: 15px;" role="presentation">
                                            <tr>
                                                <td align="center" style="padding: 15px;">
                                                    <h3 style="margin-top: 0; margin-bottom: 10px; font-size: 14px; color: #f9f9f9;">""" + stock_name + """</h3>
                                                    <div style="font-size: 16px; font-weight: bold; color: """ + price_color + """;">""" + format_currency(stock['price']) + """</div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>"""
        else:
            # Empty cell to maintain table structure
            html += """
                                    <td width="50%">&nbsp;</td>"""
        
        html += """
                                </tr>"""
    
    html += """
                            </table>
                        </td>
                    </tr>
                </table>"""

    html += """
                <!-- Account Balances Section -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                    <tr>
                        <td>
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px; border-bottom: 1px solid #2c3038; padding-bottom: 10px;">Account Balances</h2>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #1a1f27; border-radius: 8px;">
                                <tr style="background-color: #232830;">
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #2c3038; font-weight: bold; color: #f9f9f9;">Account</th>
                                    <th align="right" style="padding: 10px; border-bottom: 1px solid #2c3038; font-weight: bold; color: #f9f9f9;">Balance</th>
                                </tr>"""

    # Add account balances
    for account, balance in data['account_balances'].items():
        html += """
                                <tr>
                                    <td style="padding: 10px; border-bottom: 1px solid #2c3038; color: #f9f9f9;">""" + account + """</td>
                                    <td align="right" style="padding: 10px; border-bottom: 1px solid #2c3038; color: #f9f9f9;">""" + format_currency(balance) + """</td>
                                </tr>"""

    html += """
                            </table>
                        </td>
                    </tr>
                </table>

                <!-- Largest Transactions Section -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                    <tr>
                        <td>
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px; border-bottom: 1px solid #2c3038; padding-bottom: 10px;">Largest Transactions</h2>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #1a1f27; border-radius: 8px;">
                                <tr style="background-color: #232830;">
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #2c3038; font-weight: bold; color: #f9f9f9;">#</th>
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #2c3038; font-weight: bold; color: #f9f9f9;">Date</th>
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #2c3038; font-weight: bold; color: #f9f9f9;">Description</th>
                                    <th align="right" style="padding: 10px; border-bottom: 1px solid #2c3038; font-weight: bold; color: #f9f9f9;">Amount</th>
                                </tr>"""

    # Add largest transactions
    for i, transaction in enumerate(data['largest_transactions'], 1):
        html += """
                                <tr>
                                    <td style="padding: 10px; border-bottom: 1px solid #2c3038; color: #f9f9f9;">""" + str(i) + """</td>
                                    <td style="padding: 10px; border-bottom: 1px solid #2c3038; color: #f9f9f9;">""" + transaction['transaction_date'] + """</td>
                                    <td style="padding: 10px; border-bottom: 1px solid #2c3038; color: #f9f9f9;">""" + transaction['description'] + """</td>
                                    <td align="right" style="padding: 10px; border-bottom: 1px solid #2c3038; color: #f9f9f9;">""" + format_currency(transaction['amount']) + """</td>
                                </tr>"""

    html += """
                            </table>
                        </td>
                    </tr>
                </table>

                <!-- Largest Deposits Section -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                    <tr>
                        <td>
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px; border-bottom: 1px solid #2c3038; padding-bottom: 10px;">Largest Deposits</h2>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #1a1f27; border-radius: 8px;">
                                <tr style="background-color: #232830;">
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #2c3038; font-weight: bold; color: #f9f9f9;">#</th>
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #2c3038; font-weight: bold; color: #f9f9f9;">Date</th>
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #2c3038; font-weight: bold; color: #f9f9f9;">Description</th>
                                    <th align="right" style="padding: 10px; border-bottom: 1px solid #2c3038; font-weight: bold; color: #f9f9f9;">Amount</th>
                                </tr>"""

    # Add largest deposits
    for i, deposit in enumerate(data['largest_deposits'], 1):
        html += """
                                <tr>
                                    <td style="padding: 10px; border-bottom: 1px solid #2c3038; color: #f9f9f9;">""" + str(i) + """</td>
                                    <td style="padding: 10px; border-bottom: 1px solid #2c3038; color: #f9f9f9;">""" + deposit['transaction_date'] + """</td>
                                    <td style="padding: 10px; border-bottom: 1px solid #2c3038; color: #f9f9f9;">""" + deposit['description'] + """</td>
                                    <td align="right" style="padding: 10px; border-bottom: 1px solid #2c3038; color: #f9f9f9;">""" + format_currency(deposit['amount']) + """</td>
                                </tr>"""

    html += """
                            </table>
                        </td>
                    </tr>
                </table>

                <!-- Financial News Section -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #1a1f27; border-radius: 8px; margin-bottom: 20px;" role="presentation">
                    <tr>
                        <td style="padding: 20px;">
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px; border-bottom: 1px solid #2c3038; padding-bottom: 10px;">Financial News</h2>
                            <p style="margin-top: 0; margin-bottom: 15px; color: #f9f9f9;">""" + data['news_ai_summary'] + """</p>
                            
                            <!-- News Articles -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">"""

    # Add news articles - using simpler approach for better email compatibility
    # Limit to top 3-4 articles to avoid email clipping in Gmail and other clients
    max_articles = min(4, len(data['news_articles']))
    for article in data['news_articles'][:max_articles]:
        published_date = datetime.strptime(article['published_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y")
        html += """
                                <tr>
                                    <td style="padding: 10px; background-color: #232830; border-bottom: 1px solid #2c3038;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">
                                            <tr>
                                                <td>
                                                    <p style="margin-top: 0; margin-bottom: 5px; font-size: 16px; font-weight: bold;"><a href=\"""" + article['url'] + """\" target="_blank" style="color: #2ca05a; text-decoration: none;">""" + article['title'] + """</a></p>
                                                    <p style="margin: 5px 0; color: #aaaaaa; font-size: 12px;">""" + article['source'] + """ · """ + published_date + """</p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>"""

    html += """
                            </table>
                        </td>
                    </tr>
                </table>

                <!-- Footer -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                    <tr>
                        <td align="center" style="padding: 20px; color: #aaaaaa; font-size: 12px; border-top: 1px solid #2c3038;">
                            <div style="text-align: center; margin-bottom: 10px;">
                                <span style="color: #2ca05a; font-size: 20px; font-weight: bold;">Penny</span>
                            </div>
                            <p>© 2025 Penny Newsletter. All rights reserved.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
    
    <!--[if mso]>
    </td>
    </tr>
    </table>
    <![endif]-->
</body>
</html>
    """
    
    return html


if __name__ == "__main__":
    import sys
    import os
    
    # Get customer ID from command line argument or use a default
    customer_id = "67cd1c779683f20dd518f115"
    
    print(f"Generating newsletter for customer ID: {customer_id}")
    
    try:
        # Get customer data from report_data module
        customer_data = report_data.get_report_data(customer_id, "7d")
        
        # Generate the newsletter HTML
        newsletter_html = generate_newsletter(customer_data)
        
        # Create output directory if it doesn't exist
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Write the HTML to a file
        output_file = os.path.join(output_dir, f"{customer_id}_newsletter.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(newsletter_html)
        
        print(f"Newsletter generated successfully and saved to: {output_file}")
        
    except Exception as e:
        print(f"Error generating newsletter: {str(e)}")
        sys.exit(1)
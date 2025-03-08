from datetime import datetime
import report_data

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
    # Avoiding any collapsing sections that might be interpreted as accordions
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="format-detection" content="telephone=no">
    <title>Financial Newsletter - """ + data['name'] + """</title>
    <!--[if mso]>
    <style type="text/css">
        body, table, td {font-family: Arial, Helvetica, sans-serif !important;}
    </style>
    <![endif]-->
</head>
<body style="margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; line-height: 1.4; color: #333333; background-color: #f9f9f9;">
    <!-- Wrapper table for entire email - MSO conditional ensures Outlook compatibility -->
    <!--[if mso]>
    <table align="center" border="0" cellspacing="0" cellpadding="0" width="600">
    <tr>
    <td>
    <![endif]-->
    
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin: 0 auto; background-color: #f9f9f9;" role="presentation">
        <tr>
            <td align="center" style="padding: 20px;">
                <!-- Header -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 5px; margin-bottom: 20px;">
                    <tr>
                        <td align="center" style="padding: 30px 20px; border-bottom: 1px solid #e0e0e0;">
                            <h1 style="color: #2ca05a; margin-bottom: 5px; font-size: 28px;">Financial Insights</h1>
                            <p style="color: #666666; font-size: 16px; margin-top: 5px;">Your personal financial newsletter - """ + datetime.now().strftime('%B %d, %Y') + """</p>
                        </td>
                    </tr>
                </table>

                <!-- Summary Box -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 5px; margin-bottom: 20px;">
                    <tr>
                        <td style="padding: 20px;">
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px;">Summary</h2>
                            <p style="margin-top: 0; margin-bottom: 0;">""" + data['accounts_summary'] + """</p>
                        </td>
                    </tr>
                </table>

                <!-- Financial Overview -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                    <tr>
                        <td>
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px; border-bottom: 1px solid #e0e0e0; padding-bottom: 10px;">Financial Overview</h2>
                        </td>
                    </tr>
                    <!-- Net Worth -->
                    <tr>
                        <td>
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 5px; margin-bottom: 15px;">
                                <tr>
                                    <td align="center" style="padding: 20px;">
                                        <h3 style="color: #2ca05a; margin-top: 0; margin-bottom: 10px; font-size: 18px;">Net Worth</h3>
                                        <div style="font-size: 24px; font-weight: bold; color: #333333;">""" + format_currency(data['net_worth']) + """</div>
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
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 5px; margin-right: 10px; margin-bottom: 15px;">
                                            <tr>
                                                <td align="center" style="padding: 15px;">
                                                    <h3 style="color: #2ca05a; margin-top: 0; margin-bottom: 10px; font-size: 16px;">Money Spent</h3>
                                                    <div style="font-size: 18px; font-weight: bold; color: #333333;">""" + format_currency(data['money_spent']) + """</div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                    <td width="33%" valign="top">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 5px; margin-right: 5px; margin-left: 5px; margin-bottom: 15px;">
                                            <tr>
                                                <td align="center" style="padding: 15px;">
                                                    <h3 style="color: #2ca05a; margin-top: 0; margin-bottom: 10px; font-size: 16px;">Money Added</h3>
                                                    <div style="font-size: 18px; font-weight: bold; color: #333333;">""" + format_currency(data['money_added']) + """</div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                    <td width="33%" valign="top">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 5px; margin-left: 10px; margin-bottom: 15px;">
                                            <tr>
                                                <td align="center" style="padding: 15px;">
                                                    <h3 style="color: #2ca05a; margin-top: 0; margin-bottom: 10px; font-size: 16px;">Money Owed</h3>
                                                    <div style="font-size: 18px; font-weight: bold; color: #333333;">""" + format_currency(data['money_owed']) + """</div>
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
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px; border-bottom: 1px solid #e0e0e0; padding-bottom: 10px;">The Market</h2>
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
                                        <table width="95%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 5px; margin-right: 10px; margin-bottom: 15px;" role="presentation">
                                            <tr>
                                                <td align="center" style="padding: 15px;">
                                                    <h3 style="margin-top: 0; margin-bottom: 10px; font-size: 14px;">""" + stock_name + """</h3>
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
                                        <table width="95%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 5px; margin-left: 10px; margin-bottom: 15px;" role="presentation">
                                            <tr>
                                                <td align="center" style="padding: 15px;">
                                                    <h3 style="margin-top: 0; margin-bottom: 10px; font-size: 14px;">""" + stock_name + """</h3>
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
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>

                <!-- Account Balances Section -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                    <tr>
                        <td>
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px; border-bottom: 1px solid #e0e0e0; padding-bottom: 10px;">Account Balances</h2>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 5px;">
                                <tr style="background-color: #f5f5f5;">
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Account</th>
                                    <th align="right" style="padding: 10px; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Balance</th>
                                </tr>"""

    # Add account balances
    for account, balance in data['account_balances'].items():
        html += """
                                <tr>
                                    <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">""" + account + """</td>
                                    <td align="right" style="padding: 10px; border-bottom: 1px solid #e0e0e0;">""" + format_currency(balance) + """</td>
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
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px; border-bottom: 1px solid #e0e0e0; padding-bottom: 10px;">Largest Transactions</h2>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 5px;">
                                <tr style="background-color: #f5f5f5;">
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #e0e0e0; font-weight: bold;">#</th>
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Date</th>
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Description</th>
                                    <th align="right" style="padding: 10px; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Amount</th>
                                </tr>"""

    # Add largest transactions
    for i, transaction in enumerate(data['largest_transactions'], 1):
        html += """
                                <tr>
                                    <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">""" + str(i) + """</td>
                                    <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">""" + transaction['transaction_date'] + """</td>
                                    <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">""" + transaction['description'] + """</td>
                                    <td align="right" style="padding: 10px; border-bottom: 1px solid #e0e0e0;">""" + format_currency(transaction['amount']) + """</td>
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
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px; border-bottom: 1px solid #e0e0e0; padding-bottom: 10px;">Largest Deposits</h2>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 5px;">
                                <tr style="background-color: #f5f5f5;">
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #e0e0e0; font-weight: bold;">#</th>
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Date</th>
                                    <th align="left" style="padding: 10px; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Description</th>
                                    <th align="right" style="padding: 10px; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Amount</th>
                                </tr>"""

    # Add largest deposits
    for i, deposit in enumerate(data['largest_deposits'], 1):
        html += """
                                <tr>
                                    <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">""" + str(i) + """</td>
                                    <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">""" + deposit['transaction_date'] + """</td>
                                    <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">""" + deposit['description'] + """</td>
                                    <td align="right" style="padding: 10px; border-bottom: 1px solid #e0e0e0;">""" + format_currency(deposit['amount']) + """</td>
                                </tr>"""

    html += """
                            </table>
                        </td>
                    </tr>
                </table>

                <!-- Financial News Section -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 5px; margin-bottom: 20px;" role="presentation">
                    <tr>
                        <td style="padding: 20px;">
                            <h2 style="color: #2ca05a; margin-top: 0; margin-bottom: 15px; font-size: 20px; border-bottom: 1px solid #e0e0e0; padding-bottom: 10px;">Financial News</h2>
                            <p style="margin-top: 0; margin-bottom: 15px;">""" + data['news_ai_summary'] + """</p>
                            
                            <!-- News Articles -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">"""

    # Add news articles - using simpler approach for better email compatibility
    # Limit to top 3-4 articles to avoid email clipping in Gmail and other clients
    max_articles = min(4, len(data['news_articles']))
    for article in data['news_articles'][:max_articles]:
        published_date = datetime.strptime(article['published_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y")
        html += """
                                <tr>
                                    <td style="padding: 10px; background-color: #f5f5f5; border-bottom: 1px solid #e0e0e0;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">
                                            <tr>
                                                <td>
                                                    <p style="margin-top: 0; margin-bottom: 5px; font-size: 16px; font-weight: bold;"><a href=\"""" + article['url'] + """\" target="_blank" style="color: #2ca05a; text-decoration: none;">""" + article['title'] + """</a></p>
                                                    <p style="margin: 5px 0; color: #888888; font-size: 12px;">""" + article['source'] + """ · """ + published_date + """</p>
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
                        <td align="center" style="padding: 20px; color: #888888; font-size: 12px; border-top: 1px solid #e0e0e0;">
                            <p>© 2025 Financial Insights Newsletter. All rights reserved.</p>
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
    # Example usage:
    import json
    
    # Load the JSON data (for demonstration purposes)
    customer_id = "67cbd8d99683f20dd518d75e"
    customer_data = report_data.get_report_data(customer_id, "30d")
    
    # Generate newsletter
    newsletter_html = generate_newsletter(customer_data)
    
    # Save the HTML to a file
    with open('financial_newsletter_email.html', 'w') as file:
        file.write(newsletter_html)
    
    print("Email-friendly newsletter generated successfully! Open 'financial_newsletter_email.html' in your browser to view it.")
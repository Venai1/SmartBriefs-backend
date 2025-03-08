"""
Email sender module for financial newsletters
"""
import os
import resend
from datetime import datetime
import report_data
from generate_newsletter import generate_newsletter

# Get API key from environment or set directly
#RESEND_API_KEY = os.environ["RESEND_API_KEY"]
RESEND_API_KEY = "re_7ZbDEmYy_Dizg5KJPsMc76zxfGegSBGrs"
def send_financial_newsletter(customer_id, date_range, recipient_email):
    """
    Generate and send a financial newsletter email to a customer.
    
    Parameters:
    customer_id (str): The ID of the customer to generate the newsletter for
    date_range (str): The date range for the report (e.g., "30d", "60d", "90d")
    recipient_email (str): Email address to send the newsletter to (required)
    
    Returns:
    dict: The email response from the Resend API
    """
    # Set Resend API key
    resend.api_key = RESEND_API_KEY
    
    # Get customer data from report_data module
    customer_data = report_data.get_report_data(customer_id, date_range)
    
    # Generate HTML newsletter content
    newsletter_html = generate_newsletter(customer_data)

    # Get customer name for email subject
    full_name = customer_data.get('name', f"{customer_data.get('first_name', '')} {customer_data.get('last_name', '')}")
    
    # Format today's date for the email subject
    today_date = datetime.now().strftime('%b %d, %Y')
    
    # Construct email subject
    subject = f"Financial Insights Newsletter for {full_name} - {today_date}"

    params: resend.Emails.SendParams = {
        "from": "SmartBriefs <smartbriefs@newsletter.venai.dev>",
        "to": [recipient_email],
        "subject": subject,
        "html": newsletter_html
    }

    # Send the email
    try:
        email_response = resend.Emails.send(params)
        print(f"Email sent successfully to {recipient_email}")
        return email_response
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise
    

def send_newsletter_to_multiple_customers(customer_ids, date_range, email_mapping=None):
    """
    Send financial newsletters to multiple customers.
    
    Parameters:
    customer_ids (list): List of customer IDs
    date_range (str): The date range for the report (e.g., "30d", "60d", "90d")
    email_mapping (dict, optional): Dictionary mapping customer IDs to email addresses.
                                    If not provided, must be specified in each call.
    
    Returns:
    dict: Mapping of customer IDs to email send results
    """
    results = {}
    
    for customer_id in customer_ids:
        try:
            # Get the email address from the mapping or use a default pattern
            email = None
            if email_mapping and customer_id in email_mapping:
                email = email_mapping[customer_id]
                
            if not email:
                raise ValueError(f"No email address found for customer ID: {customer_id}")
                
            # Send the newsletter
            result = send_financial_newsletter(customer_id, date_range, email)
            results[customer_id] = {"success": True, "result": result}
            
        except Exception as e:
            results[customer_id] = {"success": False, "error": str(e)}
            print(f"Failed to send newsletter to customer {customer_id}: {str(e)}")
    
    return results


if __name__ == "__main__":
    # Example usage
    customer_id = "67cc82d19683f20dd518da03"  # Example customer ID
    date_range = "30d"  # Last 30 days
    test_email = "venai.seepersaud@gmail.com"  # Test email address
    
    # Send newsletter to a single customer
    print("Sending newsletter to a single customer...")
    result = send_financial_newsletter(customer_id, date_range, test_email)
    print(f"Email result: {result}")
    
    '''
    # Example of sending to multiple customers
    print("\nSending newsletters to multiple customers...")
    customer_ids = ["67cbd8d99683f20dd518d75e", "67cbd8d99683f20dd518d76f"]
    email_mapping = {
        "67cbd8d99683f20dd518d75e": "customer1@example.com",
        "67cbd8d99683f20dd518d76f": "customer2@example.com"
    }
    
    results = send_newsletter_to_multiple_customers(customer_ids, date_range, email_mapping)
    print("Multiple send results:")
    for cid, res in results.items():
        print(f"Customer {cid}: {'Success' if res['success'] else 'Failed - ' + res['error']}")
    '''
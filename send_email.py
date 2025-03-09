"""
Email sender module for financial newsletters with Firebase integration
"""
import os
import resend
from dotenv import load_dotenv
from datetime import datetime
import report_data
from generate_newsletter import generate_newsletter
from firebase_admin import firestore
import numpy as np


load_dotenv()
RESEND_API_KEY = os.environ["RESEND_API_KEY"]

def convert_numpy_types(obj):
    """Convert numpy types to Python native types recursively in dictionaries and lists."""
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

def get_firestore_db():
    """
    Get the Firestore database client.
    This avoids circular imports by getting the client at runtime.
    """
    try:
        # Get the existing client that was initialized in main.py
        return firestore.client()
    except Exception as e:
        print(f"Warning: Could not get Firestore client: {e}")
        return None

def send_financial_newsletter(customer_id, date_range, recipient_email):
    """
    Generate and send a financial newsletter email to a customer.
    The generated report data is also stored in Firebase under 'last_newsletter_data'.
    
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

    # Store the report data in Firebase
    try:
        # Get Firestore client at runtime instead of import time
        db = get_firestore_db()
        
        if db is not None:
            # In Firestore, the document ID is the email address as seen in the screenshot
            # So we can directly access the user document if we have the email
            user_doc_ref = db.collection("users").document(recipient_email)
            user_doc = user_doc_ref.get()
            
            if user_doc.exists:
                # Convert NumPy types to native Python types before storing in Firestore
                converted_data = convert_numpy_types(customer_data)
                
                # Update the user document with the newsletter data
                user_doc_ref.update({
                    "last_newsletter_data": {
                        "data": converted_data,
                        "date": datetime.now().isoformat(),
                        "date_range": date_range
                    }
                })
                print(f"Updated user {recipient_email} with the latest newsletter data")
            else:
                # If we don't have the email directly, try to find the user by customer_id
                users_ref = db.collection("users")
                query = users_ref.where("customer_id", "==", customer_id).limit(1)
                user_docs = query.get()
                
                user_found = False
                for doc in user_docs:
                    user_found = True
                    # Convert NumPy types to native Python types before storing in Firestore
                    converted_data = convert_numpy_types(customer_data)
                    
                    doc.reference.update({
                        "last_newsletter_data": {
                            "data": converted_data,
                            "date": datetime.now().isoformat(),
                            "date_range": date_range
                        }
                    })
                    print(f"Updated user {doc.id} with the latest newsletter data")
                
                if not user_found:
                    print(f"Warning: Could not find user for customer_id {customer_id} or email {recipient_email}")
        else:
            print("Warning: Firebase db not initialized, skipping database update")
    except Exception as e:
        print(f"Error storing report data in Firebase: {str(e)}")
        # Continue with email sending even if database update fails

    params: resend.Emails.SendParams = {
        "from": "Penny <penny@newsletter.venai.dev>",
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

if __name__ == "__main__":

    ## CALLING THIS ONLY HELPS WITH TESTING EMAIL DOES NOT UPDATE DATABASe
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
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

def initialize_firebase():
    """
    Initialize Firebase with credentials from environment variables
    This works both locally (with a service account file) and in Vercel/Railway (with env variables)
    """
    try:
        # First, try to use environment variable (preferred for production)
        if os.environ.get("FIREBASE_SERVICE_ACCOUNT"):
            try:
                service_account_info = json.loads(os.environ.get("FIREBASE_SERVICE_ACCOUNT"))
                cred = credentials.Certificate(service_account_info)
                firebase_admin.initialize_app(cred)
                print("Firebase initialized using FIREBASE_SERVICE_ACCOUNT environment variable")
                return firestore.client()
            except Exception as env_error:
                print(f"Error initializing Firebase with environment variable: {str(env_error)}")
                # Continue to try the file method

        
        # If we got here, no credentials were available
        print("No Firebase credentials found. Database functionality will be unavailable.")
        return None
            
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        return None
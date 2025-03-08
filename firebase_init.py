import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

def initialize_firebase():
    """
    Initialize Firebase with credentials from environment variables
    This works both locally (with a service account file) and in Vercel (with env variables)
    """
    try:
        # First, try to use a service account file if it exists (local development)
        if os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
            return firestore.client()
        
        # If no file, try to use environment variables (Vercel deployment)
        elif os.environ.get("FIREBASE_SERVICE_ACCOUNT"):
            service_account_info = json.loads(os.environ.get("FIREBASE_SERVICE_ACCOUNT"))
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred)
            return firestore.client()
        
        else:
            print("No Firebase credentials found. Database functionality will be unavailable.")
            return None
            
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        return None
    
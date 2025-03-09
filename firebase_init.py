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
        
        # If no file, try to use environment variables (Vercel deployment)
        os.environ.get("FIREBASE_SERVICE_ACCOUNT"):
            try:
                # Make sure we're getting valid JSON from the environment variable
                service_account_info = json.loads(os.environ.get("FIREBASE_SERVICE_ACCOUNT"))
                cred = credentials.Certificate(service_account_info)
                app = firebase_admin.initialize_app(cred)
                return firestore.client()
            except json.JSONDecodeError as e:
                print(f"Error parsing Firebase service account JSON: {str(e)}")
                print("Please check the format of your FIREBASE_SERVICE_ACCOUNT environment variable")
                
                # As a fallback, try to handle the case where the JSON might be escaped or formatted incorrectly
                try:
                    # Sometimes environment variables have escaped quotes or other issues
                    raw_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
                    # Replace any potential escaped quotes
                    clean_json = raw_json.replace('\\"', '"').replace('\\\\', '\\')
                    # Try to parse again after cleaning
                    service_account_info = json.loads(clean_json)
                    cred = credentials.Certificate(service_account_info)
                    app = firebase_admin.initialize_app(cred)
                    return firestore.client()
                except Exception as e2:
                    print(f"Failed to parse Firebase service account JSON after cleaning: {str(e2)}")
                    return None
        
        else:
            print("No Firebase credentials found. Database functionality will be unavailable.")
            return None
            
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        return None
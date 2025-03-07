from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
import requests
import json
import firebase_admin
from firebase_admin import credentials, firestore
import fillAccounts
import random

# Firebase setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

API_URL = "http://api.nessieisreal.com"
API_KEY = "9699a5b7260039b6a8fac75cf9dae5d0"


app = FastAPI()

class Address(BaseModel):
    street_number: str
    street_name: str
    city: str
    state: str
    zip: str

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    address: Address
    email: str
    frequency: str
    
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/register")
def register_user(request: RegisterRequest):
    # First, check if the user already exists in the database
    user_ref = db.collection("users").document(request.email)
    user_doc = user_ref.get()
    
    # If user exists, return the user information in the same format as new users
    if user_doc.exists:
        user_data = user_doc.to_dict()
        # Check if we have address data stored
        address = {
            "street_number": "",
            "street_name": "",
            "city": "",
            "state": "",
            "zip": ""
        }
        
        # If address exists in the stored user data, use it
        if "address" in user_data:
            address = {
                "street_number": user_data["address"].get("street_number", ""),
                "street_name": user_data["address"].get("street_name", ""),
                "city": user_data["address"].get("city", ""),
                "state": user_data["address"].get("state", ""),
                "zip": user_data["address"].get("zip", "")
            }
        
        return {
            "status": "success",
            "message": "Customer created and data saved to database",
            "capital_one_response": {
                "code": 201,
                "message": "Customer created",
                "objectCreated": {
                    "first_name": user_data.get("first_name"),
                    "last_name": user_data.get("last_name"),
                    "address": address,
                    "_id": user_data.get("customer_id")
                }
            },
            "database_data": user_data
        }
    
    # If user doesn't exist, proceed with registration
    # Prepare the data for Nessie API
    capital_one_data = {
        "first_name": request.first_name,
        "last_name": request.last_name,
        "address": {
            "street_number": request.address.street_number,
            "street_name": request.address.street_name,
            "city": request.address.city,
            "state": request.address.state,
            "zip": request.address.zip
        }
    }
    
    # Set up headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        # Make request to Capital One Nessie API
        url = f"{API_URL}/customers?key={API_KEY}"
        response = requests.post(
            url,
            data=json.dumps(capital_one_data),
            headers=headers
        )
        
        # Check if request was successful
        response.raise_for_status()
        capital_one_response = response.json()
        
        # Get the customer ID from the response
        customer_id = capital_one_response.get('objectCreated', {}).get('_id')
        
        if customer_id:
            # Save to Firestore
            user_data = {
                "customer_id": customer_id,
                "email": request.email,
                "frequency": request.frequency,
                "first_name": request.first_name,
                "last_name": request.last_name,
                "address": {
                    "street_number": request.address.street_number,
                    "street_name": request.address.street_name,
                    "city": request.address.city,
                    "state": request.address.state,
                    "zip": request.address.zip
                }
            }
            
            db.collection("users").document(request.email).set(user_data)
            fillAccounts.fill_accounts_with_data(customer_id)
            
            return {
                "status": "success",
                "message": "Customer created and data saved to database",
                "capital_one_response": capital_one_response,
                "database_data": user_data
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to get customer ID from API response")
    
    except requests.exceptions.RequestException as e:
        # Handle API errors
        raise HTTPException(status_code=500, detail=f"Error calling Capital One API: {str(e)}")
    except Exception as e:
        # Handle general errors including Firestore errors
        raise HTTPException(status_code=500, detail=f"Error saving to database: {str(e)}")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
import requests
import json

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
    topic: List[str]

# The correct API endpoint from your CURL request
API_URL = "http://api.nessieisreal.com/customers"
API_KEY = "9699a5b7260039b6a8fac75cf9dae5d0"

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/register")
def register_user(request: RegisterRequest):
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
    
    # Set up headers exactly like in your CURL request
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        # Make request to Capital One Nessie API
        url = f"{API_URL}?key={API_KEY}"
        
        response = requests.post(
            url,
            data=json.dumps(capital_one_data),
            headers=headers
        )
        
        # Check if request was successful
        response.raise_for_status()
        capital_one_response = response.json()
        
        # Return combined response
        return {
            "status": "success",
            "capital_one_response": capital_one_response,
            "registration_data": {
                "email": request.email,
                "frequency": request.frequency,
                "topic": request.topic
            }
        }
    
    except requests.exceptions.RequestException as e:
        # Handle API errors
        raise HTTPException(status_code=500, detail=f"Error calling Capital One API: {str(e)}")
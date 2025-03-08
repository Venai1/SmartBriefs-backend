from fastapi import APIRouter, HTTPException
import os
import requests
import json
import time
from datetime import datetime
import socket
from dotenv import load_dotenv
import traceback

# Try importing OpenAI
try:
    from openai import OpenAI
    has_openai = True
except ImportError:
    has_openai = False

# Try importing yfinance
try:
    import yfinance as yf
    has_yfinance = True
except ImportError:
    has_yfinance = False

# Try importing Firebase
try:
    import firebase_admin
    from firebase_admin import firestore
    has_firebase = True
except ImportError:
    has_firebase = False

# Try importing Resend
try:
    import resend
    has_resend = True
except ImportError:
    has_resend = False

# Create router
router = APIRouter(prefix="/diagnostic", tags=["diagnostic"])

load_dotenv()

# Basic network connectivity test
@router.get("/network-test")
async def test_network():
    """
    Test basic network connectivity to various services.
    """
    results = {}
    
    # Test common websites
    websites = [
        {"name": "Google", "url": "https://www.google.com"},
        {"name": "Amazon", "url": "https://www.amazon.com"},
        {"name": "CloudFlare DNS", "url": "https://1.1.1.1"},
        {"name": "OpenAI", "url": "https://api.openai.com"}
    ]
    
    for site in websites:
        try:
            start_time = time.time()
            response = requests.get(site["url"], timeout=5)
            elapsed = time.time() - start_time
            results[site["name"]] = {
                "status": response.status_code,
                "success": response.status_code == 200,
                "time_ms": round(elapsed * 1000, 2)
            }
        except Exception as e:
            results[site["name"]] = {
                "success": False,
                "error": str(e)
            }
    
    # Test socket connections
    services = [
        {"name": "Google DNS", "host": "8.8.8.8", "port": 53},
        {"name": "OpenAI API", "host": "api.openai.com", "port": 443},
        {"name": "Yahoo Finance", "host": "query1.finance.yahoo.com", "port": 443}
    ]
    
    for service in services:
        try:
            start_time = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            result = s.connect_ex((service["host"], service["port"]))
            s.close()
            elapsed = time.time() - start_time
            results[f"Socket {service['name']}"] = {
                "success": result == 0,
                "error_code": result,
                "time_ms": round(elapsed * 1000, 2)
            }
        except Exception as e:
            results[f"Socket {service['name']}"] = {
                "success": False,
                "error": str(e)
            }
    
    # Test DNS resolution
    domains = ["api.openai.com", "query1.finance.yahoo.com", "api.resend.com", "firestore.googleapis.com"]
    for domain in domains:
        try:
            start_time = time.time()
            ip = socket.gethostbyname(domain)
            elapsed = time.time() - start_time
            results[f"DNS {domain}"] = {
                "success": True,
                "ip": ip,
                "time_ms": round(elapsed * 1000, 2)
            }
        except Exception as e:
            results[f"DNS {domain}"] = {
                "success": False,
                "error": str(e)
            }
    
    # Summary
    successful = sum(1 for r in results.values() if r.get("success", False))
    total = len(results)
    
    return {
        "summary": {
            "success_rate": f"{successful}/{total} ({round(successful/total*100, 1)}%)",
            "timestamp": datetime.now().isoformat()
        },
        "tests": results
    }

# Test OpenAI API
@router.get("/test-openai")
async def test_openai_api():
    """
    Test the OpenAI API connection.
    """
    if not has_openai:
        return {"status": "error", "message": "OpenAI library not installed"}
    
    api_key = os.getenv("OPEN_AI_API_KEY")
    if not api_key:
        return {"status": "error", "message": "OPEN_AI_API_KEY environment variable not set"}
    
    results = {
        "api_key_configured": bool(api_key),
        "api_key_masked": f"{api_key[:5]}...{api_key[-4:]}" if api_key else None
    }
    
    try:
        client = OpenAI(api_key=api_key)
        
        start_time = time.time()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello in one word."}
            ],
            max_tokens=10
        )
        elapsed = time.time() - start_time
        
        results["api_call"] = {
            "success": True,
            "response": response.choices[0].message.content.strip(),
            "time_ms": round(elapsed * 1000, 2),
            "model": "gpt-3.5-turbo"
        }
        
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        error_details = traceback.format_exc()
        return {
            "status": "error",
            "message": str(e),
            "traceback": error_details,
            "results": results
        }

# Test Yahoo Finance API
@router.get("/test-yahoo-finance")
async def test_yahoo_finance():
    """
    Test the Yahoo Finance API.
    """
    if not has_yfinance:
        return {"status": "error", "message": "yfinance library not installed"}
    
    results = {}
    tickers = ["AAPL", "MSFT", "^GSPC", "^DJI"]
    
    for ticker in tickers:
        try:
            start_time = time.time()
            stock = yf.Ticker(ticker)
            
            # Test history
            hist = stock.history(period="1d")
            
            # Test info
            info = stock.info
            
            elapsed = time.time() - start_time
            
            results[ticker] = {
                "success": True,
                "has_history": not hist.empty,
                "history_rows": len(hist) if not hist.empty else 0,
                "has_info": bool(info),
                "time_ms": round(elapsed * 1000, 2)
            }
            
            if not hist.empty:
                results[ticker]["latest_close"] = hist["Close"].iloc[-1] if not hist.empty else None
            
        except Exception as e:
            error_details = traceback.format_exc()
            results[ticker] = {
                "success": False,
                "error": str(e),
                "traceback": error_details
            }
    
    # Overall success
    successes = sum(1 for r in results.values() if r.get("success", False))
    
    return {
        "status": "success" if successes > 0 else "error",
        "success_rate": f"{successes}/{len(tickers)}",
        "results": results
    }

# Test Firebase
@router.get("/test-firebase")
async def test_firebase():
    """
    Test Firebase Firestore connection.
    """
    if not has_firebase:
        return {"status": "error", "message": "Firebase library not installed"}
    
    # Check for service account key file
    service_account_path = "serviceAccountKey.json"
    service_account_exists = os.path.exists(service_account_path)
    
    # Check environment variables
    firebase_env_var = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    
    results = {
        "service_account_file_exists": service_account_exists,
        "firebase_service_account_env": bool(firebase_env_var)
    }
    
    try:
        # Try to get the existing client
        db = firestore.client()
        
        # Test a simple operation
        start_time = time.time()
        # Use a safe collection name for testing
        test_collection = db.collection("_diagnostic_tests")
        test_doc_ref = test_collection.document("test_connection")
        test_doc_ref.set({
            "timestamp": datetime.now().isoformat(),
            "test": "connection"
        })
        test_doc = test_doc_ref.get()
        test_doc_ref.delete()  # Clean up after ourselves
        elapsed = time.time() - start_time
        
        results["operations"] = {
            "success": True,
            "write_success": True,
            "read_success": test_doc.exists,
            "time_ms": round(elapsed * 1000, 2)
        }
        
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        error_details = traceback.format_exc()
        return {
            "status": "error",
            "message": str(e),
            "traceback": error_details,
            "results": results
        }

# Test Resend Email API
@router.get("/test-resend")
async def test_resend():
    """
    Test Resend email API configuration (does not send actual emails).
    """
    if not has_resend:
        return {"status": "error", "message": "Resend library not installed"}
    
    api_key = os.getenv("RESEND_API_KEY")
    
    results = {
        "api_key_configured": bool(api_key),
        "api_key_masked": f"{api_key[:5]}...{api_key[-4:]}" if api_key and len(api_key) > 10 else None
    }
    
    if not api_key:
        return {
            "status": "error",
            "message": "RESEND_API_KEY environment variable not set",
            "results": results
        }
    
    try:
        # Just set the API key but don't send an email
        resend.api_key = api_key
        
        return {
            "status": "configured",
            "message": "Resend API key is configured correctly. No email sent.",
            "results": results
        }
    except Exception as e:
        error_details = traceback.format_exc()
        return {
            "status": "error",
            "message": str(e),
            "traceback": error_details,
            "results": results
        }

# Test actual email sending (use with caution)
@router.get("/test-send-email")
async def test_send_email(to_email: str = None):
    """
    Test sending an actual email with Resend.
    Requires a to_email query parameter.
    """
    if not has_resend:
        return {"status": "error", "message": "Resend library not installed"}
    
    if not to_email:
        return {"status": "error", "message": "to_email query parameter is required"}
    
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        return {"status": "error", "message": "RESEND_API_KEY environment variable not set"}
    
    try:
        resend.api_key = api_key
        
        start_time = time.time()
        response = resend.Emails.send({
            "from": "SmartBriefs <smartbriefs@newsletter.venai.dev>",
            "to": [to_email],
            "subject": "Test Email from Financial Newsletter API",
            "html": """
                <div style="font-family: Arial, sans-serif; padding: 20px;">
                    <h1>Test Email</h1>
                    <p>This is a test email from your Financial Newsletter API diagnostic tool.</p>
                    <p>If you received this, your email sending is working correctly!</p>
                    <p>Time sent: {}</p>
                </div>
            """.format(datetime.now().isoformat())
        })
        elapsed = time.time() - start_time
        
        return {
            "status": "success",
            "time_ms": round(elapsed * 1000, 2),
            "response": response,
            "recipient": to_email
        }
    except Exception as e:
        error_details = traceback.format_exc()
        return {
            "status": "error",
            "message": str(e),
            "traceback": error_details
        }

# Test environment variables
@router.get("/env-vars")
async def test_env_vars():
    """
    Test if all required environment variables are set.
    Masks sensitive values for security.
    """
    env_vars = {
        "NESSIE_API_URL": os.getenv("NESSIE_API_URL"),
        "NESSIE_API_KEY": mask_value(os.getenv("NESSIE_API_KEY")),
        "OPEN_AI_API_KEY": mask_value(os.getenv("OPEN_AI_API_KEY")),
        "RESEND_API_KEY": mask_value(os.getenv("RESEND_API_KEY")),
        "NEWS_API_KEY": mask_value(os.getenv("NEWS_API_KEY")),
        "FIREBASE_SERVICE_ACCOUNT": "(Set)" if os.getenv("FIREBASE_SERVICE_ACCOUNT") else "(Not Set)"
    }
    
    # Count how many are set
    set_count = sum(1 for v in env_vars.values() if v)
    missing = [k for k, v in env_vars.items() if not v]
    
    return {
        "status": "success" if set_count == len(env_vars) else "warning",
        "set_count": f"{set_count}/{len(env_vars)}",
        "missing": missing,
        "environment_variables": env_vars
    }

# Test everything in one call
@router.get("/all")
async def test_all():
    """
    Run all diagnostic tests and compile results.
    """
    results = {}
    
    # Network connectivity
    try:
        results["network"] = await test_network()
    except Exception as e:
        results["network"] = {"status": "error", "message": str(e)}
    
    # OpenAI
    try:
        results["openai"] = await test_openai_api()
    except Exception as e:
        results["openai"] = {"status": "error", "message": str(e)}
    
    # Yahoo Finance
    try:
        results["yahoo_finance"] = await test_yahoo_finance()
    except Exception as e:
        results["yahoo_finance"] = {"status": "error", "message": str(e)}
    
    # Firebase
    try:
        results["firebase"] = await test_firebase()
    except Exception as e:
        results["firebase"] = {"status": "error", "message": str(e)}
    
    # Resend
    try:
        results["resend"] = await test_resend()
    except Exception as e:
        results["resend"] = {"status": "error", "message": str(e)}
    
    # Environment variables
    try:
        results["env_vars"] = await test_env_vars()
    except Exception as e:
        results["env_vars"] = {"status": "error", "message": str(e)}
    
    # Count successes
    success_count = sum(1 for r in results.values() if r.get("status") == "success")
    
    return {
        "status": "success" if success_count == len(results) else "partial_success" if success_count > 0 else "failure",
        "success_count": f"{success_count}/{len(results)}",
        "timestamp": datetime.now().isoformat(),
        "results": results
    }

# Helper function to mask sensitive values
def mask_value(value):
    if not value:
        return None
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}...{value[-4:]}"

# Function to integrate with FastAPI app
def add_diagnostic_routes(app):
    """
    Add diagnostic routes to the FastAPI app.
    Call this function in your main.py file.
    """
    app.include_router(router)
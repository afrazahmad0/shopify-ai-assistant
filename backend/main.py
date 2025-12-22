from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.get("/test-shopify")
def test_shopify_connection():
    # Get credentials from .env
    store_url = os.getenv("SHOPIFY_STORE_URL")
    access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")

    if not store_url or not access_token:
        return {"error": "Shopify credentials not found in .env file"}

    url = f"https://{store_url}/admin/api/2024-01/products.json"
    headers = {
        "X-Shopify-Access-Token": access_token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": "Failed to connect to Shopify",
            "status_code": response.status_code,
            "details": response.text
        }

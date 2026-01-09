from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from database import create_table, save_chat, get_chats
from dotenv import load_dotenv
from openai import OpenAI
import requests
import os

load_dotenv()

app = FastAPI()

create_table()

app.mount(
"/static",
StaticFiles(directory="Static"),
name="static"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


@app.get("/test-shopify")
def test_shopify_connection():
    store_url = os.getenv("SHOPIFY_STORE_URL")
    access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")

    if not store_url or not access_token:
        return {"error": "Shopify credentials not found"}

    url = f"https://{store_url}/admin/api/2024-01/products.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()

    return {"error": "Failed to connect to Shopify"}


@app.get("/products-clean")
def get_clean_products():
    store_url = os.getenv("SHOPIFY_STORE_URL")
    access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")

    url = f"https://{store_url}/admin/api/2024-01/products.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.get(url, headers=headers)
    products = response.json().get("products", [])

    clean_products = []

    for p in products:
        clean_products.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "price": p.get("variants", [{}])[0].get("price"),
            "image": p.get("image", {}).get("src")
        })

    return {"products": clean_products}


from database import get_chats

@app.get("/assistant")
def assistant(question: str):
    store_url = os.getenv("SHOPIFY_STORE_URL")
    access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")

    url = f"https://{store_url}/admin/api/2024-01/products.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.get(url, headers=headers)
    products = response.json().get("products", [])

    product_text = ""
    for p in products:
        product_text += f"""
        Product: {p.get('title')}
        Price: {p.get('variants', [{}])[0].get('price')}
        Description: {p.get('body_html')}
        """

    previous_chats = get_chats()

    chat_context = ""
    for q, a, _ in previous_chats:
        chat_context += f"""
        User: {q}
        Assistant: {a}
        """

    prompt = f"""
You are a Shopify store assistant.

Store products:
{product_text}

Previous conversation:
{chat_context}

Now answer the new question clearly.

Customer question:
{question}
"""

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = ai_response.choices[0].message.content

    save_chat(question, answer)

    return {"answer": answer}


@app.get("/generate-description")
def generate_description(product_info: str):
    prompt = f"""
Generate a professional Shopify product title and description.

Product info:
{product_info}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    generated_text = response.choices[0].message.content

    save_chat(product_info, generated_text)

    return {"generated_text": generated_text}
from database import get_chats

@app.get("/chat-history")
def chat_history():
    rows = get_chats()
    history = []
    for q, a, t in rows:
        history.append({
            "question": q,
            "answer": a,
            "time": t
        })
    return {"history": history}

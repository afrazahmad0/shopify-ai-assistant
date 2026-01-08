import sqlite3

DB_NAME = "assistant.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT,
        ai_reply TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_chat(user_message, ai_reply):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats (user_message, ai_reply) VALUES (?, ?)",
        (user_message, ai_reply)
    )

    conn.commit()
    conn.close()

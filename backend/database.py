import sqlite3

DB_NAME = "chats.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_chat(question, answer):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats (question, answer) VALUES (?, ?)",
        (question, answer)
    )

    conn.commit()
    conn.close()


def get_chats(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT question, answer, created_at FROM chats ORDER BY id DESC LIMIT ?",
        (limit,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows[::-1]

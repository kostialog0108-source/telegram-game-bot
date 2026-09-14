import sqlite3

DB_NAME = "game.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance INTEGER DEFAULT 1000,
            level INTEGER DEFAULT 1,
            experience INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def create_player(user_id, username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO players
        (user_id, username, balance, level, experience)
        VALUES (?, ?, 1000, 1, 0)
    """, (user_id, username))

    conn.commit()
    conn.close()


def get_player(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, balance, level, experience
        FROM players
        WHERE user_id = ?
    """, (user_id,))

    player = cursor.fetchone()

    conn.close()

    return player

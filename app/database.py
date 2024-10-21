
import psycopg2
from app.config import DATABASE_URL

conn = psycopg2.connect(DATABASE_URL)

def execute_query(query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params)
        
        res = cur.fetchall()
        conn.commit()
        return res

def execute_non_query(query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()

def create_tables():
    """Create users and saved_articles tables if they do not exist."""
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_articles (
            id UUID PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            link TEXT,
            content TEXT,
            tags TEXT[],
            user_id UUID REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        conn.commit()

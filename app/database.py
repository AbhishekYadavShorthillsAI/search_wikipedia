
import psycopg2
from app.config import DATABASE_URL

conn = psycopg2.connect(DATABASE_URL)

def execute_query(query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params)

        try:
            res = cur.fetchall()
            conn.commit()
            return res
        except:
            return

def execute_non_query(query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()

def create_tables():
    """Create users and saved_articles tables if they do not exist."""
    execute_query("""
    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL
    );
    """)
    
    execute_query("""
    CREATE TABLE IF NOT EXISTS saved_articles (
        id UUID PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT,
        tags TEXT[],
        user_id UUID REFERENCES users(id) ON DELETE CASCADE
    );
    """)

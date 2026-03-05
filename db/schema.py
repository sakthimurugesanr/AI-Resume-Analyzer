import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import get_connection


async def create_tables():
    """Create all required tables if they don't already exist."""
    conn = await get_connection()
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id          SERIAL PRIMARY KEY,
                username    VARCHAR(100) NOT NULL,
                email       VARCHAR(255) NOT NULL UNIQUE,
                role        VARCHAR(50)  NOT NULL,
                phone       VARCHAR(20),
                image_url   TEXT,
                resume_url  TEXT,
                created_at  TIMESTAMP DEFAULT NOW()
            )
        """)
        print("Tables are ready.")
    finally:
        await conn.close()
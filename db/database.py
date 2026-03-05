import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


async def get_connection():
    """Create and return a new DB connection."""
    return await asyncpg.connect(DATABASE_URL)
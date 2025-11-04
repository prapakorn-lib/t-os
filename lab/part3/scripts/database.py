"""
Database Connection Module
This module handles PostgreSQL database connections
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """
    Create and return a database connection
    
    Returns:
        connection: PostgreSQL connection object
    """
    try:
        connection = psycopg2.connect(
            os.getenv('DATABASE_URL'),
            cursor_factory=RealDictCursor
        )
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def close_db_connection(connection):
    """
    Close database connection
    
    Args:
        connection: PostgreSQL connection object to close
    """
    if connection:
        connection.close()

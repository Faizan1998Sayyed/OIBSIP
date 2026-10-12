"""
Database Module for Smart BMI Calculator
Handles SQLite database creation, storage, retrieval, multi-user filtering, and error handling.
"""

import sqlite3
import os
from typing import List, Tuple, Dict, Any, Optional

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "bmi_records.db")

def get_connection(db_path: str = DEFAULT_DB_PATH):
    """
    Establishes and returns a database connection.
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to connect to SQLite database at {db_path}: {e}")


def init_db(db_path: str = DEFAULT_DB_PATH) -> Tuple[bool, str]:
    """
    Initializes the SQLite database table 'bmi_records' if it does not exist.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        weight REAL NOT NULL,
        height REAL NOT NULL,
        bmi REAL NOT NULL,
        category TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
        return True, "Database initialized successfully."
    except Exception as e:
        return False, f"Database initialization error: {str(e)}"


def save_record(user_name: str, weight: float, height: float, bmi: float, category: str, db_path: str = DEFAULT_DB_PATH) -> Tuple[bool, str]:
    """
    Saves a new BMI calculation record using parameterized SQL.
    """
    insert_sql = """
    INSERT INTO bmi_records (user_name, weight, height, bmi, category)
    VALUES (?, ?, ?, ?, ?);
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(insert_sql, (user_name, weight, height, bmi, category))
            conn.commit()
        return True, "BMI record saved successfully."
    except Exception as e:
        return False, f"Error saving record to database: {str(e)}"


def get_all_records(db_path: str = DEFAULT_DB_PATH) -> Tuple[bool, Any]:
    """
    Retrieves all records ordered by creation date descending.
    """
    select_sql = """
    SELECT id, created_at, user_name, weight, height, bmi, category
    FROM bmi_records
    ORDER BY created_at DESC, id DESC;
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(select_sql)
            rows = cursor.fetchall()
            records = [dict(row) for row in rows]
        return True, records
    except Exception as e:
        return False, f"Error fetching records: {str(e)}"


def get_user_records(user_name: str, db_path: str = DEFAULT_DB_PATH) -> Tuple[bool, Any]:
    """
    Retrieves records for a specific user ordered chronologically (created_at ASC) for trend plotting or history.
    """
    select_sql = """
    SELECT id, created_at, user_name, weight, height, bmi, category
    FROM bmi_records
    WHERE user_name = ?
    ORDER BY created_at ASC, id ASC;
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(select_sql, (user_name,))
            rows = cursor.fetchall()
            records = [dict(row) for row in rows]
        return True, records
    except Exception as e:
        return False, f"Error fetching user records: {str(e)}"


def get_unique_users(db_path: str = DEFAULT_DB_PATH) -> Tuple[bool, List[str]]:
    """
    Retrieves a sorted list of unique user names stored in the database.
    """
    select_sql = """
    SELECT DISTINCT user_name
    FROM bmi_records
    ORDER BY user_name ASC;
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(select_sql)
            rows = cursor.fetchall()
            users = [row['user_name'] for row in rows]
        return True, users
    except Exception as e:
        return False, []

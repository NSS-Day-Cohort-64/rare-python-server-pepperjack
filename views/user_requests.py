import sqlite3
import json
import bcrypt
from datetime import datetime
from models import User

def login_user(user):

    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Fetch the user's hashed password from the database
        db_cursor.execute("""
            select id, password
            from Users
            where username = ?
        """, (user['username'], ))

        user_from_db = db_cursor.fetchone()

        # If the user was found and the hashed passwords match
        if user_from_db is not None and bcrypt.checkpw(user['password'].encode('utf-8'), user_from_db['password'].encode('utf-8')):
            response = {
                'valid': True,
                'token': user_from_db['id']
            }
        else:
            response = {
                'valid': False
            }

        return json.dumps(response)

def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    # Hash the user's password using bcrypt
    hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())

    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            user['first_name'],
            user['last_name'],
            user['username'],
            user['email'],
            hashed_password.decode('utf-8'),  # Decode the hashed password bytes to store as text
            user['bio'],
            datetime.now()
        ))

        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })

def get_all_users():
    """
    Get all users
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT id, username, first_name, last_name, email, bio, profile_image_url
            FROM Users
            ORDER BY username
        """)

        dataset = db_cursor.fetchall()

        users = []
        for row in dataset:
            user = User(
                row['id'],
                row['username'],
                row['first_name'],
                row['last_name'],
                row['email'],
                row['bio'],
                row['profile_image_url'] if row['profile_image_url'] else None
            )
            users.append(user.__dict__)

        return users

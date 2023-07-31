import sqlite3
import json
from datetime import datetime
from models.post import Post

def get_single_post(user):
    """Gets a single post from the database"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM Posts p
        WHERE p.id = ?
        """, ( user, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'], data['publication_date'], data['image_url'], data['content'], data['approved'])

        return post.__dict__

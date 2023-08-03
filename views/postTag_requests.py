"""Module for generating postTag requests"""

import sqlite3
from models import Post_tag

def get_postTags_by_post_id(post_id):
    """Gets all postTags by post_id"""
    with sqlite3.connect("./db.sqlite3") as conn:
        
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pt.id,
            pt.post_id,
            pt.tag_id
        FROM PostTags pt
        WHERE pt.post_id = ?
        """, (post_id,))

        postTagsList = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            postTag = Post_tag(row['id'], row['post_id'], row['tag_id'])

            postTagsList.append(postTag.__dict__)

    return postTagsList

from models import Tag
import sqlite3


def get_all_tags_alphabetical():

    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label            
        FROM Tags t
        ORDER BY LOWER(label) ASC
        """)

        tagsList = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['label'])

            tagsList.append(tag.__dict__)

    return tagsList


def create_tag(new_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags
            (label)
        VALUES
            (?);
        """, (new_tag['label'],))

        id = db_cursor.lastrowid

        new_tag['id'] = id

    return new_tag

import sqlite3

def create_category(new_category):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories
            (label)
        VALUES
            (?);
        """, (new_category['label'],))

        category_id = db_cursor.lastrowid

        new_category['id'] = category_id

    return new_category

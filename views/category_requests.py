import sqlite3
from models import Category

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

def get_all_categories():
    """
    Get all categories from the Categories table.

    Returns:
        A list of dictionaries, each representing a category.
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT id, label
            FROM Categories
            ORDER BY label
        """)

        # Fetch all rows from the database as dictionaries
        rows = db_cursor.fetchall()

        # Convert rows to a list of dictionaries
        categories = []
        for row in rows:
            category = Category(row["id"], row["label"])
            categories.append(category.__dict__)

        return categories

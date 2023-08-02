import sqlite3
from datetime import datetime
from models import Post, User, Category


def get_all_posts_recent_first():

    with sqlite3.connect("./db.sqlite3") as conn:

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
            p.approved,
            u.id,
            u.first_name author_first_name,
            u.last_name author_last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active,
            c.id,
            c.label             
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        ORDER BY publication_date DESC
        
        """)

        postsList = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'], row['approved'])

            user = User(row['id'], row['author_first_name'], row['author_last_name'], row['email'], row['bio'],
                        row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])

            category = Category(row['id'], row['label'])

            post.author = user.__dict__
            post.category = category.__dict__

            postsList.append(post.__dict__)

    return postsList


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
            p.approved,
            u.id,
            u.first_name author_first_name,
            u.last_name author_last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active,
            c.id,
            c.label
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        WHERE p.id = ?
        """, (user, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'],
                    data['publication_date'], data['image_url'], data['content'], data['approved'])

        user = User(data['id'], data['author_first_name'], data['author_last_name'], data['email'], data['bio'],
                    data['username'], data['password'], data['profile_image_url'], data['created_on'], data['active'])

        category = Category(data['id'], data['label'])

        post.author = user.__dict__
        post.category = category.__dict__

        return post.__dict__


def get_posts_by_user_id(user_id):
    """Gets all posts from the database by a specific user"""
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
            p.approved,
            u.id user_id,
            c.id,
            c.label
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        WHERE u.id = ?
        """, (user_id, ))

        postsList = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'], row['approved'])

            category = Category(row['id'], row['label'])

            post.author = row['user_id']
            post.category = category.__dict__

            postsList.append(post.__dict__)

    return postsList


def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            (user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES
            (?, ?, ?, ?, ?, ?, ?);
        """, (new_post.user_id, new_post.category_id, new_post.title, new_post.publication_date,
              new_post.image_url, new_post.content, new_post.approved))

        post_id = db_cursor.lastrowid

        new_post.id = post_id

    return new_post

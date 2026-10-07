import sqlite3

import os

DATABASE_NAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "customer_persona.db"
)

def connect_db():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection

def create_tables():

    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history (
        prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        income REAL NOT NULL,
        spending_score REAL NOT NULL,
        cluster INTEGER NOT NULL,
        persona TEXT NOT NULL,
        recommendation TEXT NOT NULL,

        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
    )
""")

    connection.commit()
    connection.close()

def register_user(name, email, phone, username, password_hash):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users
        (name, email, phone, username, password_hash)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, phone, username, password_hash))

    connection.commit()
    connection.close()

    print("User registered successfully!")

def login_user(username, password_hash):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT user_id, name, email, phone, username, password_hash
        FROM users
        WHERE username = ? AND password_hash = ?
    """, (username, password_hash))

    user = cursor.fetchone()

    connection.close()

    return user

def save_prediction(user_id, age, gender, income, spending_score,
                    cluster, persona, recommendation):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO prediction_history
        (
            user_id,
            age,
            gender,
            income,
            spending_score,
            cluster,
            persona,
            recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        age,
        gender,
        income,
        spending_score,
        cluster,
        persona,
        recommendation
    ))

    connection.commit()
    connection.close()

    print("Prediction saved successfully!")

def get_prediction_history(user_id):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            prediction_id,
            age,
            gender,
            income,
            spending_score,
            cluster,
            persona,
            recommendation
        FROM prediction_history
        WHERE user_id = ?
        ORDER BY prediction_id DESC
    """, (user_id,))

    history = cursor.fetchall()

    connection.close()

    return history

def update_user(user_id, name, email, phone):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET name = ?, email = ?, phone = ?
        WHERE user_id = ?
    """, (name, email, phone, user_id))

    connection.commit()
    connection.close()

    print("User updated successfully!")
    
def delete_user(user_id):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE user_id = ?
    """, (user_id,))

    connection.commit()
    connection.close()

    print("User deleted successfully!")

if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")

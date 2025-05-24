import bcrypt
import mysql.connector
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CA_PATH = os.path.join(BASE_DIR, "ca.pem")


def get_db():
    return mysql.connector.connect(
        host="mysql-2e900226-ainulhasan1999-7428.l.aivencloud.com",
        port=15125,
        user="avnadmin",
        password="AVNS_jd6jADXVbRtsrci9dFh",
        database="defaultdb",
        ssl_ca=CA_PATH,
    )


def initialize_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def create_user(username: str, password: str):
    # Hash password with bcrypt directly
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed.decode("utf-8")),  # Store as string
    )
    conn.commit()
    conn.close()


def verify_user(username: str, password: str):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False

    # Convert stored hash string to bytes and verify password
    stored_hash = user["password"].encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash)

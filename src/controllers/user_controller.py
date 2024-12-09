# src/controllers/user_controller.py
from database.database import get_connection

class UserController:
    def login(self, username, password):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", 
                       (username, password))  # In real app, use proper password hashing
            user = cur.fetchone()
            return user is not None
        finally:
            conn.close()
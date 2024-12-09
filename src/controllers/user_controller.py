# src/controllers/user_controller.py

from database.database import get_connection

class UserController:
    def login(self, username_or_email, password):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username_or_email, password))
            user = cur.fetchone()
            if user:
                return user
            cur.execute("SELECT * FROM users WHERE email = ? AND password_hash = ?", (username_or_email, password))
            user = cur.fetchone()
            if user:
                return user
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cur.close()
            conn.close()
        return None
       
    def register(self, username, email, password):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cur.close()
            conn.close()
        return False

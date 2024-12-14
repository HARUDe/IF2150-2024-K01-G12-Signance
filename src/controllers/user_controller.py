# src/controllers/UserController.py

from models.user import User
from database.database import get_connection

class UserController:
    def __init__(self):
        self.logged_in_user = None

    def login(self, username_or_email, password):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", 
                      (username_or_email, password))
            user = cur.fetchone()
            if not user:
                cur.execute("SELECT * FROM users WHERE email = ? AND password_hash = ?", 
                          (username_or_email, password))
                user = cur.fetchone()
            
            if user:
                self.logged_in_user = User(
                    username=user[1],
                    email=user[2],
                    password_hash=user[3],
                    user_id=user[0]
                )
                return user
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cur.close()
            conn.close()
        return None

    def register(self, username, email, password):
        if self.is_username_taken(username):
            return False, "Username already taken"
        
        if self.is_email_registered(email):
            return False, "Email already registered"
        
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", 
                (username, email, password)
            )
            conn.commit()
            return True, "Registration successful"
        except Exception as e:
            print(f"An error occurred: {e}")
            return False, "Registration failed"
        finally:
            cur.close()
            conn.close()

    def is_username_taken(self, username):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            count = cur.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"Error checking username: {str(e)}")
            return False
        finally:
            cur.close()
            conn.close()

    def is_email_registered(self, email):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM users WHERE email = ?", (email,))
            count = cur.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"Error checking email: {str(e)}")
            return False
        finally:
            cur.close()
            conn.close()

    def logout_user(self):
        self.logged_in_user = None

    def get_logged_in_user(self):
        return self.logged_in_user

    def get_user_by_username_or_email(self, username_or_email):
        """Fetch user by username or email."""
        conn = get_connection()  # Assuming you have a database connection function
        cur = conn.cursor()
        try:
            # Try to get user by username
            cur.execute("SELECT * FROM users WHERE username = ?", (username_or_email,))
            user = cur.fetchone()
            
            # If no user is found by username, try with email
            if not user:
                cur.execute("SELECT * FROM users WHERE email = ?", (username_or_email,))
                user = cur.fetchone()

            return user  # Return user details (user_id, username, email, etc.)
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            cur.close()
            conn.close()
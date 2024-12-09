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

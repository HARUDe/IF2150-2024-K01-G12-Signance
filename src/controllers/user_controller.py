# src/controllers/UserController.py
from models.user import User

class UserController:
    def __init__(self):
        self.users = []
        self.logged_in_user = None

    def register_user(self, username, email, password_hash):
        user_id = self.users[-1].user_id + 1 if self.users else 1
        user = User(username=username, email=email, password_hash=password_hash, user_id=user_id)
        self.users.append(user)
        return user

    def login_user(self, email, password_hash):
        for user in self.users:
            if user.email == email and user.password_hash == password_hash:
                self.logged_in_user = user
                return True
        return False

    def logout_user(self):
        self.logged_in_user = None

    def get_logged_in_user(self):
        return self.logged_in_user

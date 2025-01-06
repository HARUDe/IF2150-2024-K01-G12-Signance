#src/utils/helpers.py
import bcrypt
import re

def format_currency(amount: float) -> str:
    return f'${amount:,.2f}'

def validate_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def hash_password(password: str) -> str:
    print(f"Hashing password: {password}")

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def decrypt_password(password_input: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password_input.encode(), password_hash.encode())

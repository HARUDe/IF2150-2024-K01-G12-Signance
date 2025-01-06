#src/utils/helpers.py
import bcrypt
import re

def format_currency(amount: float) -> str:
    return f'${amount:,.2f}'

def validate_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

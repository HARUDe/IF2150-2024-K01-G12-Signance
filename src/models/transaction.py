# src/models/transaction.py

from datetime import datetime
from decimal import Decimal
from enum import Enum

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Category(Enum):
    FOODS = "foods"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    EDUCATION = "education"
    OTHER = "other"

class Transaction:
    def __init__(self, user_id: int, amount: Decimal, category: str, 
                 transaction_type: TransactionType, description: str = None,
                 transaction_id: int = None, date: datetime = None):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.description = description
        self.date = date

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'amount': str(self.amount),
            'category': self.category,
            'transaction_type': self.transaction_type.value,
            'description': self.description,
            'date': self.date
        }
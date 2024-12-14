# src/models/budget.py
from datetime import datetime
from decimal import Decimal
from enum import Enum

class Category(Enum):
    FOODS = "foods"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    EDUCATION = "education"
    OTHER = "other"

class Budget:
    def __init__(self, user_id: int, category: str, amount: Decimal,
                 start_date: datetime, end_date: datetime, budget_id: int = None):
        self.budget_id = budget_id
        self.user_id = user_id
        self.category = category
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date
        self.current_amount = Decimal('0')

    def add_expense(self, amount: Decimal):
        self.current_amount += amount

    def get_remaining(self) -> Decimal:
        return self.amount - self.current_amount

    def get_percentage_used(self) -> float:
        return float(self.current_amount / self.amount * 100)

    def to_dict(self):
        return {
            'budget_id': self.budget_id,
            'user_id': self.user_id,
            'category': self.category,
            'amount': str(self.amount),
            'current_amount': str(self.current_amount),
            'start_date': self.start_date,
            'end_date': self.end_date
        }
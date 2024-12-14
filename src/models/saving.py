# src/models/saving.py
from datetime import datetime
from decimal import Decimal

class SavingGoal:
    def __init__(self, saving_id, user_id, name, target_amount, current_amount, deadline, created_at):
        self.saving_id = saving_id
        self.user_id = user_id
        self.name = name
        self.target_amount = target_amount
        self.current_amount = current_amount
        self.deadline = deadline
        self.created_at = created_at

    def add_saving(self, amount: Decimal):
        self.current_amount += amount

    def get_progress_percentage(self) -> float:
        return float(self.current_amount / self.target_amount * 100)

    def is_goal_reached(self) -> bool:
        return self.current_amount >= self.target_amount

    def to_dict(self):
        return {
            'saving_id': self.saving_id,
            'user_id': self.user_id,
            'name': self.name,
            'target_amount': str(self.target_amount),
            'current_amount': str(self.current_amount),
            'deadline': self.deadline,
            'created_at': self.created_at
        }
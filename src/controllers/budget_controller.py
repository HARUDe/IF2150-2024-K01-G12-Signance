from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from models.budget import Budget


class BudgetController:
    def __init__(self):
        self.budgets = []

    # CRUD operations
    def create_budget(self, user_id, category, amount, start_date, end_date):
        budget = Budget(user_id, category, amount, start_date, end_date,
                        budget_id=self.budgets[-1].budget_id + 1 if self.budgets else 1)
        self.budgets.append(budget)

    def update_budget(self, budget_id, category=None, amount=None, start_date=None, end_date=None):
        budget = self.get_budget_by_id(budget_id)
        if budget:
            if category:
                budget.category = category
            if amount:
                budget.amount = amount
            if start_date:
                budget.start_date = start_date
            if end_date:
                budget.end_date = end_date
            return budget
        return None

    def delete_budget(self, budget_id):
        budget = self.get_budget_by_id(budget_id)
        if budget:
            self.budgets.remove(budget)

    def get_budget_by_id(self, budget_id):
        for budget in self.budgets:
            if budget.budget_id == budget_id:
                return budget
        return None

    def get_all_budgets(self):
        return self.budgets

from datetime import datetime
from decimal import Decimal
from models.saving import SavingGoal

class SavingsController:
    def __init__(self):
        self.savings = []
        self.next_id = 1

    def create_saving(self, user_id, name, target_amount, deadline):
        saving = SavingGoal(user_id, name, target_amount, deadline, saving_id=self.next_id)
        self.savings.append(saving)
        self.next_id += 1
        return saving

    def update_saving(self, saving_id, name=None, target_amount=None, deadline=None):
        saving = self.get_saving_by_id(saving_id)
        if saving:
            if name:
                saving.name = name
            if target_amount:
                saving.target_amount = target_amount
            if deadline:
                saving.deadline = deadline
            return saving
        return None

    def delete_saving(self, saving_id):
        saving = self.get_saving_by_id(saving_id)
        if saving:
            self.savings.remove(saving)

    def get_saving_by_id(self, saving_id):
        for saving in self.savings:
            if saving.saving_id == saving_id:
                return saving
        return None

    def get_all_savings(self):
        return self.savings
# src/controllers/TransactionController.py
from models.transaction import Transaction, TransactionType
from decimal import Decimal
from datetime import datetime

class TransactionController:
    def __init__(self):
        self.transactions = []

    def create_transaction(self, user_id, amount, category, transaction_type, description=None):
        transaction_id = self.transactions[-1].transaction_id + 1 if self.transactions else 1
        transaction = Transaction(
            user_id=user_id,
            amount=Decimal(amount),
            category=category,
            transaction_type=TransactionType(transaction_type),
            description=description,
            transaction_id=transaction_id
        )
        self.transactions.append(transaction)

    def update_transaction(self, transaction_id, amount, category, transaction_type, description=None):
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                transaction.amount = Decimal(amount)
                transaction.category = category
                transaction.transaction_type = TransactionType(transaction_type)
                transaction.description = description
                return True
        return False

    def delete_transaction(self, transaction_id):
        self.transactions = [t for t in self.transactions if t.transaction_id != transaction_id]

    def get_all_transactions(self):
        return self.transactions

    def get_transaction_by_id(self, transaction_id):
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                return transaction
        return None

    def calculate_monthly_spending(self, user_id):
        """Calculate total spending for the current month."""
        if not user_id:
            return 0
        transactions = self.transactions
        current_month = datetime.now().month
        current_year = datetime.now().year
        total_spending = sum(
            Decimal(transaction.amount)
            for transaction in transactions
            if transaction.date.month == current_month and transaction.date.year == current_year and transaction.transaction_type.value == "expense"
        )

        return total_spending

from models.transaction import Transaction, TransactionType
from decimal import Decimal
from datetime import datetime
from database.database import get_connection

class TransactionController:
    def __init__(self):
        # Initialize the connection to the database
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def create_transaction(self, user_id, amount, category, transaction_type, description=None):
        """Insert a new transaction into the database."""
        try:
            query = """
            INSERT INTO transactions (user_id, amount, category, transaction_type, description, date)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Convert Decimal to float
            self.cursor.execute(query, (user_id, float(Decimal(amount)), category, transaction_type, description, current_date))
            self.conn.commit()
        except Exception as e:
            print(f"Error creating transaction: {e}")

    def update_transaction(self, transaction_id, amount, category, transaction_type, description=None):
        """Update an existing transaction."""
        try:
            query = """
            UPDATE transactions
            SET amount = ?, category = ?, transaction_type = ?, description = ?
            WHERE transaction_id = ?
            """
            # Convert Decimal to float
            self.cursor.execute(query, (float(Decimal(amount)), category, transaction_type, description, transaction_id))
            self.conn.commit()
        except Exception as e:
            print(f"Error updating transaction: {e}")

    def delete_transaction(self, transaction_id):
        """Delete a transaction by its ID."""
        try:
            query = "DELETE FROM transactions WHERE transaction_id = ?"
            self.cursor.execute(query, (transaction_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting transaction: {e}")

    def get_all_transactions(self):
        """Fetch all transactions from the database."""
        try:
            query = "SELECT * FROM transactions"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            transactions = []
            for row in rows:
                transaction = Transaction(
                    user_id=row[1],
                    amount=row[2],
                    category=row[3],
                    transaction_type=TransactionType(row[4]),
                    description=row[5],
                    transaction_id=row[0],
                    date=row[6]
                )
                transactions.append(transaction)
            return transactions
        except Exception as e:
            print(f"Error fetching all transactions: {e}")
            return []

    def get_transaction_by_id(self, transaction_id):
        """Fetch a transaction by its ID."""
        try:
            query = "SELECT * FROM transactions WHERE transaction_id = ?"
            self.cursor.execute(query, (transaction_id,))
            row = self.cursor.fetchone()
            if row:
                return Transaction(
                    user_id=row[1],
                    amount=row[2],
                    category=row[3],
                    transaction_type=TransactionType(row[4]),
                    description=row[5],
                    transaction_id=row[0],
                    date=row[6]
                )
            return None
        except Exception as e:
            print(f"Error fetching transaction by ID: {e}")
            return None

    def calculate_monthly_spending(self, user_id):
        """Calculate total spending for the current month."""
        if not user_id:
            return Decimal(0)
        
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year
            query = """
            SELECT amount
            FROM transactions
            WHERE user_id = ? AND transaction_type = ? AND 
                  strftime('%m', date) = ? AND strftime('%Y', date) = ?
            """
            self.cursor.execute(query, (user_id, "expense", f"{current_month:02d}", str(current_year)))
            rows = self.cursor.fetchall()
            
            total_spending = sum(Decimal(row[0]) for row in rows)
            return total_spending
        except Exception as e:
            print(f"Error calculating monthly spending: {e}")
            return Decimal(0)

    def calculate_monthly_category_spending(self, user_id):
        """Calculate total spending for the current month in each category."""
        if not user_id:
            return [0] * 5  # If no user ID is provided, return 0 for all categories
        
        # Categories for spending
        categories = ["food", "transport", "entertainment", "education", "other"]
        category_spending = {category: Decimal(0) for category in categories}
        
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year

            # Loop through categories and calculate total spending for each
            for category in categories:
                query = """
                SELECT amount
                FROM transactions
                WHERE user_id = ? AND category = ? AND transaction_type = ? AND 
                      strftime('%m', date) = ? AND strftime('%Y', date) = ?
                """
                self.cursor.execute(query, (user_id, category, "expense", f"{current_month:02d}", str(current_year)))
                rows = self.cursor.fetchall()
                
                total_category_spending = sum(Decimal(row[0]) for row in rows)
                category_spending[category] = total_category_spending

            # Return the category spending as a list of integers
            return [int(category_spending[category]) for category in categories]
        
        except Exception as e:
            print(f"Error calculating monthly category spending: {e}")
            return [0] * 5  # Return 0 for all categories if an error occurs

    def close(self):
        """Close the database connection and cursor when done."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

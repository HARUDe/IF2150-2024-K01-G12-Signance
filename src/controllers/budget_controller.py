# src/controllers/budget_controller.py

from decimal import Decimal
from datetime import datetime
from models.budget import Budget, Category
from database.database import get_connection

class BudgetController:
    def update_budget(self, budget_id, amount=None, start_date=None, end_date=None):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM budgets WHERE budget_id = ?", (budget_id,))
            current = cur.fetchone()
            if not current:
                return False, "Budget not found"

            new_amount = float(amount) if amount is not None else current[3]
            new_start_date = start_date if start_date is not None else current[4]
            new_end_date = end_date if end_date is not None else current[5]

            cur.execute(
                """UPDATE budgets 
                   SET amount = ?, start_date = ?, end_date = ?
                   WHERE budget_id = ?""",
                (new_amount, new_start_date, new_end_date, budget_id)
            )
            conn.commit()
            return True, "Budget updated successfully"
        except Exception as e:
            print(f"Error updating budget: {e}")
            return False, "Failed to update budget"
        finally:
            cur.close()
            conn.close()

    def get_budget_by_id(self, budget_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM budgets WHERE budget_id = ?", (budget_id,))
            row = cur.fetchone()
            if row:
                return Budget(
                    user_id=row[1],
                    category=Category(row[2]),
                    amount=Decimal(str(row[3])),
                    start_date=row[4],
                    end_date=row[5],
                    budget_id=row[0]
                )
            return None
        except Exception as e:
            print(f"Error fetching budget: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    def get_all_budgets(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT * FROM budgets 
                WHERE user_id = ? 
                ORDER BY category""", 
                (user_id,)
            )
            rows = cur.fetchall()
            budgets = [Budget(
                user_id=row[1],
                category=Category(row[2]),
                amount=Decimal(str(row[3])),
                start_date=row[4],
                end_date=row[5],
                budget_id=row[0]
            ) for row in rows]
            return budgets
        except Exception as e:
            print(f"Error fetching budgets: {e}")
            return []
        finally:
            cur.close()
            conn.close()

    def get_active_budgets(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            cur.execute("""
                SELECT * FROM budgets 
                WHERE user_id = ? 
                AND start_date <= ? 
                AND end_date >= ?
                ORDER BY category
            """, (user_id, current_date, current_date))
            
            rows = cur.fetchall()
            return [Budget(
                user_id=row[1],
                category=Category(row[2]),
                amount=Decimal(str(row[3])),
                start_date=row[4],
                end_date=row[5],
                budget_id=row[0]
            ) for row in rows]
        except Exception as e:
            print(f"Error fetching active budgets: {e}")
            return []
        finally:
            cur.close()
            conn.close()
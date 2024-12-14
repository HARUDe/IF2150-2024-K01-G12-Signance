from datetime import datetime
from decimal import Decimal
from models.saving import SavingGoal
from database.database import get_connection

class SavingsController:
    def __init__(self):
        pass  # Initialization no longer pre-fetches data

    def create_saving(self, user_id, name, target_amount, deadline):
        conn = get_connection()
        cur = conn.cursor()
        try:
            # langsung masukin ke database
            cur.execute(
                """
                INSERT INTO savings (user_id, name, target_amount, current_amount, deadline, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                RETURNING saving_id
                """,
                (user_id, name, str(target_amount), "0", deadline, datetime.now())
            )
            saving_id = cur.fetchone()[0]
            conn.commit()
            return SavingGoal(saving_id, user_id, name, target_amount, 0, deadline, datetime.now())
        except Exception as e:
            print(f"Error creating saving: {str(e)}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def update_saving(self, saving_id, name=None, target_amount=None, deadline=None):
        """Update a saving goal in the database."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            updates = []
            params = []
            if name:
                updates.append("name = ?")
                params.append(name)
            if target_amount:
                updates.append("target_amount = ?")
                params.append(str(target_amount))
            if deadline:
                updates.append("deadline = ?")
                params.append(deadline)
            if not updates:
                return None  # no updates

            params.append(saving_id)
            query = f"UPDATE savings SET {', '.join(updates)} WHERE saving_id = ?"
            cur.execute(query, tuple(params))
            conn.commit()
            # Fetch the updated saving
            return self.get_saving_by_id(saving_id)
        except Exception as e:
            print(f"Error updating saving: {str(e)}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def delete_saving(self, saving_id):
        """Delete a saving goal from the database."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM savings WHERE saving_id = ?", (saving_id,))
            conn.commit()
        except Exception as e:
            print(f"Error deleting saving: {str(e)}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def get_saving_by_id(self, saving_id):
        """Fetch a single saving goal by its ID."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT saving_id, user_id, name, target_amount, current_amount, deadline, created_at
                FROM savings
                WHERE saving_id = ?
                """,
                (saving_id,)
            )
            row = cur.fetchone()
            if row:
                return SavingGoal(
                    saving_id=row[0],
                    user_id=row[1],
                    name=row[2],
                    target_amount=Decimal(row[3]),
                    current_amount=Decimal(row[4]),
                    deadline=row[5],
                    created_at=row[6]
                )
            return None
        except Exception as e:
            print(f"Error fetching saving by ID: {str(e)}")
        finally:
            cur.close()
            conn.close()

    def update_current_amount(self, saving_id, current_amount):
        """Update the current amount of a specific savings goal."""
        try:
            current_amount = str(current_amount)
            # Update the current amount in the database
            query = """
                UPDATE savings
                SET current_amount = ?
                WHERE saving_id = ?
            """
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (current_amount, saving_id))
            conn.commit()

            print(f"Current amount for savings goal {saving_id} updated to {current_amount}.")
        except Exception as e:
            print(f"Error updating current amount: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def get_all_savings(self, user_id):
        """Fetch all savings for a specific user."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT saving_id, user_id, name, target_amount, current_amount, deadline, created_at
                FROM savings
                WHERE user_id = ?
                """,
                (user_id,)
            )
            rows = cur.fetchall()
            return [
                SavingGoal(
                    saving_id=row[0],
                    user_id=row[1],
                    name=row[2],
                    target_amount=Decimal(row[3]),
                    current_amount=Decimal(row[4]),
                    deadline=row[5],
                    created_at=row[6]
                )
                for row in rows
            ]
        except Exception as e:
            print(f"Error fetching all savings: {str(e)}")
        finally:
            cur.close()
            conn.close()

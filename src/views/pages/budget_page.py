from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QDialog, QLabel, 
    QFormLayout, QLineEdit, QDateEdit, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from decimal import Decimal
from datetime import datetime

class BudgetPage(QWidget):
    def __init__(self, user_id, controller, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.controller = controller

        # Layout for the page
        self.layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        # Floating button
        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(50, 50)
        self.add_button.setIcon(QIcon("path/to/plus_icon.png"))  # Optional
        self.add_button.setStyleSheet("""
            QPushButton {
                border-radius: 25px;
                background-color: #2196F3;
                color: white;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.add_button.clicked.connect(self.show_create_budget_dialog)

        # Floating button container
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_button)
        button_layout.setContentsMargins(0, 0, 10, 10)
        self.layout.addLayout(button_layout)

        # Connect list item click to the detail dialog
        self.list_widget.itemClicked.connect(self.show_budget_detail)

        # Load budgets
        self.refresh_budget_list()

    def refresh_budget_list(self):
        self.list_widget.clear()
        budgets = self.controller.get_all_budgets()
        for budget in budgets:
            self.list_widget.addItem(f"{budget.category} - {budget.current_amount}/{budget.amount}")

    def show_create_budget_dialog(self):
        dialog = BudgetForm(user_id=self.user_id, controller=self.controller, parent=self)
        if dialog.exec_():  # If the dialog is accepted
            self.refresh_budget_list()

    def show_budget_detail(self, item):
        budget_id = self.get_selected_budget_id()
        selected_budget = self.controller.get_budget_by_id(budget_id)
        if selected_budget:
            dialog = BudgetDetailDialog(budget=selected_budget, controller=self.controller, parent=self)
            if dialog.exec_():  # If any updates or deletions are made
                self.refresh_budget_list()

    def get_selected_budget_id(self):
        current_row = self.list_widget.currentRow()
        if current_row != -1:
            return self.controller.get_all_budgets()[current_row].budget_id
        return None


class BudgetForm(QDialog):
    def __init__(self, user_id, controller, budget=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.controller = controller
        self.budget = budget

        self.setWindowTitle("Add Budget" if not budget else "Edit Budget")
        self.setMinimumSize(300, 200)

        self.layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.category_input = QLineEdit(budget.category if budget else "")
        self.amount_input = QLineEdit(str(budget.amount) if budget else "")
        self.start_date_input = QDateEdit(budget.start_date if budget else QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        self.end_date_input = QDateEdit(budget.end_date if budget else QDate.currentDate())
        self.end_date_input.setCalendarPopup(True)

        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Amount:", self.amount_input)
        form_layout.addRow("Start Date:", self.start_date_input)
        form_layout.addRow("End Date:", self.end_date_input)
        self.layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_budget)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        self.layout.addLayout(button_layout)

    def save_budget(self):
        category = self.category_input.text()
        try:
            amount = Decimal(self.amount_input.text())
        except:
            QMessageBox.warning(self, "Error", "Amount must be a valid number.")
            return
        start_date = self.start_date_input.date().toPyDate()
        end_date = self.end_date_input.date().toPyDate()

        if category and amount > 0 and start_date < end_date:
            if self.budget:  # Update existing budget
                self.controller.update_budget(self.budget.budget_id, category, amount, start_date, end_date)
            else:  # Create a new budget
                self.controller.create_budget(self.user_id, category, amount, start_date, end_date)

            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Please provide valid inputs.")


class BudgetDetailDialog(QDialog):
    def __init__(self, budget, controller, parent=None):
        super().__init__(parent)
        self.budget = budget
        self.controller = controller

        self.setWindowTitle("Budget Details")
        self.setMinimumSize(300, 200)

        self.layout = QVBoxLayout(self)

        # Details
        self.layout.addWidget(QLabel(f"Category: {budget.category}"))
        self.layout.addWidget(QLabel(f"Total Amount: {budget.amount}"))
        self.layout.addWidget(QLabel(f"Current Amount: {budget.current_amount}"))
        self.layout.addWidget(QLabel(f"Start Date: {budget.start_date}"))
        self.layout.addWidget(QLabel(f"End Date: {budget.end_date}"))
        self.layout.addWidget(QLabel(f"Remaining: {budget.get_remaining()}"))
        self.layout.addWidget(QLabel(f"Progress: {budget.get_percentage_used():.2f}%"))

        # Buttons
        button_layout = QHBoxLayout()
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_budget)
        button_layout.addWidget(update_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_budget)
        button_layout.addWidget(delete_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)

        self.layout.addLayout(button_layout)

    def update_budget(self):
        dialog = BudgetForm(user_id=self.budget.user_id, controller=self.controller, budget=self.budget, parent=self)
        if dialog.exec_():  # If the dialog is accepted
            self.accept()  # Close the details dialog

    def delete_budget(self):
        confirm = QMessageBox.question(
            self, "Confirm Deletion", "Are you sure you want to delete this budget?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.controller.delete_budget(self.budget.budget_id)
            self.accept()

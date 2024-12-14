from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QDialog, QLabel, 
    QFormLayout, QLineEdit, QDateEdit, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from decimal import Decimal
from datetime import datetime

class SavingsPage(QWidget):
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
        self.add_button.clicked.connect(self.show_create_savings_dialog)

        # Floating button container
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_button)
        button_layout.setContentsMargins(0, 0, 10, 10)
        self.layout.addLayout(button_layout)

        # Connect list item click to the detail dialog
        self.list_widget.itemClicked.connect(self.show_savings_detail)

        # Load savings goals
        self.refresh_savings_list()

    def refresh_savings_list(self):
        self.list_widget.clear()
        savings_goals = self.controller.get_all_savings(self.user_id)
        for goal in savings_goals:
            self.list_widget.addItem(f"{goal.name} - {goal.current_amount}/{goal.target_amount}")

    def show_create_savings_dialog(self):
        dialog = SavingsForm(user_id=self.user_id, controller=self.controller, parent=self)
        if dialog.exec_():  # If the dialog is accepted
            self.refresh_savings_list()

    def show_savings_detail(self, savings):
        savings_id = self.get_selected_savings_id()
        selected_goal = self.controller.get_saving_by_id(savings_id)
        if selected_goal:
            dialog = SavingsDetailDialog(goal=selected_goal, controller=self.controller, parent=self)
            if dialog.exec_():  # If any updates or deletions are made
                self.refresh_savings_list()

    def get_selected_savings_id(self):
        current_row = self.list_widget.currentRow()
        if current_row != -1:
            return self.controller.get_all_savings(self.user_id)[current_row].saving_id
        return None
        


class SavingsForm(QDialog):
    def __init__(self, user_id, controller, goal=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.controller = controller
        self.goal = goal

        self.setWindowTitle("Add Savings Goal" if not goal else "Edit Savings Goal")
        self.setMinimumSize(300, 200)

        self.layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.name_input = QLineEdit(goal.name if goal else "")
        self.target_input = QLineEdit(str(goal.target_amount) if goal else "")
        self.deadline_input = QDateEdit(
            QDate(*map(int, goal.deadline.split('-'))) if goal else QDate.currentDate()
        )
        self.deadline_input.setCalendarPopup(True)

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Target Amount:", self.target_input)
        form_layout.addRow("Deadline:", self.deadline_input)
        self.layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_savings)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        self.layout.addLayout(button_layout)

    def save_savings(self):
        name = self.name_input.text()
        try:
            target_amount = Decimal(self.target_input.text())
        except:
            QMessageBox.warning(self, "Error", "Target amount must be a valid number.")
            return
        deadline = self.deadline_input.date().toPyDate()

        if name and target_amount > 0:
            if self.goal:  # Update existing goal
                self.controller.update_saving(self.goal.saving_id, name, target_amount, deadline)
            else:  # Create a new goal
                self.controller.create_saving(self.user_id, name, target_amount, deadline)

            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Please provide valid inputs.")

class SavingsDetailDialog(QDialog):
    def __init__(self, goal, controller, parent=None):
        super().__init__(parent)
        self.goal = goal
        self.controller = controller

        self.setWindowTitle("Savings Goal Details")
        self.setMinimumSize(300, 250)

        self.layout = QVBoxLayout(self)

        # Details
        self.layout.addWidget(QLabel(f"Name: {goal.name}"))
        self.layout.addWidget(QLabel(f"Target Amount: {goal.target_amount}"))
        
        # Current Amount with editable field
        self.current_amount_label = QLabel(f"Current Amount: {goal.current_amount}")
        self.layout.addWidget(self.current_amount_label)
        self.current_amount_input = QLineEdit(str(goal.current_amount))  # Input for current amount
        self.layout.addWidget(self.current_amount_input)

        self.layout.addWidget(QLabel(f"Deadline: {goal.deadline}"))
        self.layout.addWidget(QLabel(f"Progress: {goal.get_progress_percentage():.2f}%"))

        # Buttons
        button_layout = QHBoxLayout()

        update_goal_button = QPushButton("Update Goal")
        update_goal_button.clicked.connect(self.update_savings)
        button_layout.addWidget(update_goal_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_savings)
        button_layout.addWidget(delete_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)

        self.layout.addLayout(button_layout)

    def update_savings(self):
        # First update the current amount (if changed)
        try:
            new_current_amount = Decimal(self.current_amount_input.text())
        except:
            QMessageBox.warning(self, "Error", "Current amount must be a valid number.")
            return
        
        # Ensure the current amount is not negative
        if new_current_amount >= 0:
            # Update current amount via the controller
            self.controller.update_current_amount(self.goal.saving_id, new_current_amount)
            # Update the local object and the label
            self.goal.current_amount = new_current_amount
            self.current_amount_label.setText(f"Current Amount: {new_current_amount}")
        else:
            QMessageBox.warning(self, "Error", "Current amount must be a positive number.")
            return

        # Now update the rest of the goal if needed
        dialog = SavingsForm(user_id=self.goal.user_id, controller=self.controller, goal=self.goal, parent=self)
        if dialog.exec_():  # If the dialog is accepted
            self.accept()  # Close the details dialog

    def delete_savings(self):
        confirm = QMessageBox.question(
            self, "Confirm Deletion", "Are you sure you want to delete this savings goal?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.controller.delete_saving(self.goal.saving_id)
            self.accept()




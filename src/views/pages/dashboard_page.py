from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
from datetime import datetime
from decimal import Decimal


class DashboardPage(QWidget):
    def __init__(self, user_controller, transaction_controller, switch_to_savings_page, parent=None):
        super().__init__(parent)
        self.user_controller = user_controller
        self.transaction_controller = transaction_controller
        self.switch_to_savings_page = switch_to_savings_page

        # Layout setup
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        # Placeholder widgets
        self.welcome_label = QLabel()
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.welcome_label, alignment=Qt.AlignCenter)

        self.spending_label = QLabel()
        self.spending_label.setStyleSheet("font-size: 18px; color: #555;")
        self.layout.addWidget(self.spending_label, alignment=Qt.AlignCenter)

        # Big button for savings
        self.savings_button = QPushButton("Check Your Savings")
        self.savings_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 15px;
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.savings_button.clicked.connect(self.switch_to_savings_page)
        self.layout.addWidget(self.savings_button, alignment=Qt.AlignCenter)


    def update_dashboard(self):
        """Update the dashboard with the latest user info and monthly spending."""
        logged_in_user = self.user_controller.get_logged_in_user()
        if logged_in_user:
            self.welcome_label.setText(f"Welcome, {logged_in_user.username}!")
        else:
            self.welcome_label.setText("Welcome!")

        total_spending = self.transaction_controller.calculate_monthly_spending(logged_in_user.user_id if logged_in_user else 1)
        self.spending_label.setText(f"Total Spending This Month: ${total_spending:.2f}")
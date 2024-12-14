from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from datetime import datetime
from decimal import Decimal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import datetime

# Line Chart for Monthly Spending
class LineChart(QWidget):
    def __init__(self, user_id, transaction_controller, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.transaction_controller = transaction_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.canvas)

        self.monthly_spending_data = self.get_monthly_spending_data()  # Fetch the data
        self.plot_line_chart()

        self.setLayout(layout)

    def get_monthly_spending_data(self):
        """Fetch monthly spending data for the user"""
        # Placeholder data for the last 6 months
        data = {
            'January': 1200,
            'February': 1500,
            'March': 1000,
            'April': 900,
            'May': 1100,
            'June': 1300
        }
        return data

    def plot_line_chart(self):
        """Plot the line chart"""
        data = self.monthly_spending_data
        months = list(data.keys())
        spending = list(data.values())

        fig, ax = plt.subplots()
        ax.plot(months, spending, marker='o')

        ax.set_title('Monthly Spending')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount')
        self.canvas.draw()

# Budget Progress Bars for Categories
class BudgetProgress(QWidget):
    def __init__(self, user_id, budget_controller, transaction_controller, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.budget_controller = budget_controller
        self.transaction_controller = transaction_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.category_progress = self.get_category_progress()
        self.display_progress_bars(layout)

        self.setLayout(layout)

    def get_category_progress(self):
        """Fetch the user's budget and current spending for each category"""
        # Placeholder data for budget and spending
        budget_data = {
            'Food': 1000000,
            'Transportation': 500000,
            'Entertainment': 400000,
            'Education': 200000,
            'Others': 150000,
        }
        spending_data = {
            'Food': 512000,
            'Transportation': 350000,
            'Entertainment': 200000,
            'Education': 150000,
            'Others': 50000,
        }
        progress = {
            category: (spending_data[category] / budget_data[category]) * 100
            for category in budget_data
        }
        return progress, spending_data, budget_data

    def display_progress_bars(self, layout):
        """Create progress bars for each category"""
        progress, spending_data, budget_data = self.category_progress

        for category, progress_percentage in progress.items():
            progress_bar = QProgressBar()
            progress_bar.setValue(int(progress_percentage))  # Set percentage value
            progress_bar.setStyleSheet("QProgressBar::chunk {background-color: #4CAF50;}")

            # Display real spending and budget information
            progress_label = QLabel(
                f"{category}: {spending_data[category]:,.2f} / {budget_data[category]:,.2f} ({progress_percentage:.1f}%)"
            )

            layout.addWidget(progress_label)
            layout.addWidget(progress_bar)





class DashboardPage(QWidget):
    def __init__(self, user_id, user_controller, transaction_controller, budget_controller, switch_to_savings_page, parent=None):
        super().__init__(parent)
        self.user_controller = user_controller
        self.budget_controller = budget_controller
        self.transaction_controller = transaction_controller
        self.switch_to_savings_page = switch_to_savings_page
        self.user_id = user_id
        self.setWindowTitle("Dashboard")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        # Welcome Label
        self.welcome_label = QLabel("Welcome!")
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.welcome_label)

        # Spending Label
        self.spending_label = QLabel("Total Spending This Month: $0.00")
        self.spending_label.setStyleSheet("font-size: 18px; color: #555;")
        self.spending_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.spending_label)

        # Spacer between labels and charts
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add charts and progress bars
        chart_layout = QVBoxLayout()  # To hold the charts and progress bars separately

        # Create widgets for charts
        line_chart = LineChart(self.user_id, self.transaction_controller)
        chart_layout.addWidget(line_chart)

        # Add a spacer between the line chart and the progress bars
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        chart_layout.addItem(spacer)

        # Add budget progress widget
        budget_progress = BudgetProgress(self.user_id, self.budget_controller, self.transaction_controller)
        chart_layout.addWidget(budget_progress)

        # Add the chart layout to the main layout
        main_layout.addLayout(chart_layout)

        # Button for savings section
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
        main_layout.addWidget(self.savings_button)

    def update_dashboard(self):
        """Update the dashboard with the latest user info and monthly spending."""
        logged_in_user = self.user_controller.get_logged_in_user()
        if logged_in_user:
            self.welcome_label.setText(f"Welcome, {logged_in_user.username}!")
        else:
            self.welcome_label.setText("Welcome!")

        total_spending = self.transaction_controller.calculate_monthly_spending(logged_in_user.user_id if logged_in_user else 1)
        self.spending_label.setText(f"Total Spending This Month: ${total_spending:.2f}")
    

    def income_vs_outcome_chart(self):
        """Placeholder for the income vs outcome chart logic"""
        pass

    def monthly_income_outcome_chart(self):
        """Placeholder for monthly income vs outcome chart logic"""
        pass

    def current_vs_budget_chart(self):
        """Placeholder for current vs budget chart logic"""
        pass

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QSpacerItem, QSizePolicy, QHBoxLayout, QProgressBar
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import datetime
import colorsys

# Line Chart for Monthly Spending
class LineChart(QWidget):
    def __init__(self, user_id, transaction_controller, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.transaction_controller = transaction_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.canvas = FigureCanvas(plt.figure())  # Create a figure for the canvas
        layout.addWidget(self.canvas)

        self.monthly_spending_data = self.get_monthly_spending_data()  # Fetch the data
        self.plot_line_chart()

        self.setLayout(layout)

    def get_monthly_spending_data(self):
        """Fetch monthly spending data for the user"""
        # Replace this with actual data fetching logic
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

        # Clear the existing figure to avoid overlapping plots
        self.canvas.figure.clear()

        # Add a subplot to the existing figure
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(months, spending, marker='o', color='blue')

        ax.set_title('Monthly Spending')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.grid(True)

        # Render the plot on the canvas
        self.canvas.draw()

    def update_chart(self):
        """Update the line chart with new data"""
        self.monthly_spending_data = self.get_monthly_spending_data()
        self.plot_line_chart()

# Budget Progress Bars for Categories
class BudgetProgress(QWidget):
    def __init__(self, user_id, budget_controller, transaction_controller, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.budget_controller = budget_controller
        self.transaction_controller = transaction_controller
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.update_progress(self.user_id)

    def get_category_progress(self):
        """Fetch the user's budget and current spending for each category"""
        # Replace this with actual data fetching logic
        budget_data = {
            'Food': 1000000,
            'Transportation': 500000,
            'Entertainment': 400000,
            'Education': 200000,
            'Others': 150000,
        }
        spending_data = {
            'Food': 992000,
            'Transportation': 550000,
            'Entertainment': 200000,
            'Education': 150000,
            'Others': 50000,
        }
        progress = {
            category: (spending_data[category] / budget_data[category]) * 100
            for category in budget_data
        }
        return progress, spending_data, budget_data

    def hsl_to_rgb(self, h, s, l):
        r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
        return f"rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)})"

    def calculate_color(self, percentage):
        hue = 120 - (120 * (percentage / 100))  # Transition from 120° to 0° (Green to Red)
        saturation = 1  # Full saturation
        lightness = 0.4  # Set lightness to 40% for better visibility

        return self.hsl_to_rgb(hue, saturation, lightness)

    def display_progress_bars(self, layout):
        """Create progress bars for each category"""
        progress, spending_data, budget_data = self.category_progress

        for category, progress_percentage in progress.items():
            progress_bar = QProgressBar()
            progress_bar.setValue(min(100, int(progress_percentage)))  # Set percentage value

            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: #f0f0f0;  /* Light grey background */
                    border: 2px solid #5c5c5c;
                    border-radius: 5px;
                }}
                QProgressBar::chunk {{
                    background-color: {self.calculate_color(min(100, int(progress_percentage)))};  /* Color changes from green to red */
                }}
            """)


            # Display real spending and budget information
            progress_label = QLabel(
                f"{category}: Rp {spending_data[category]:,.2f} / Rp {budget_data[category]:,.2f} ({progress_percentage:.1f}%)"
            )

            layout.addWidget(progress_label)
            layout.addWidget(progress_bar)

    def update_progress(self, user_id):
        """Update the budget progress bars based on the new user_id."""
        self.user_id = user_id
        # Clear existing widgets
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        # Fetch progress data based on user_id
        self.category_progress = self.get_category_progress()
        # Create progress bars
        self.display_progress_bars(self.layout)

# Main DashboardPage
class DashboardPage(QWidget):
    def __init__(
        self, user_id, user_controller, transaction_controller,
        budget_controller, switch_to_savings_page, parent=None
    ):
        super().__init__(parent)
        print("dashboarid ID in as:", user_id)
        self.user_controller = user_controller
        self.budget_controller = budget_controller
        self.transaction_controller = transaction_controller
        self.switch_to_savings_page = switch_to_savings_page
        self.user_id = user_id
        self.setWindowTitle("Dashboard")
        self.init_ui()

    def init_ui(self):
        # Main vertical layout
        main_layout = QVBoxLayout()
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

        # Horizontal layout for charts and progress bars
        charts_layout = QHBoxLayout()

        # Line Chart
        self.line_chart = LineChart(self.user_id, self.transaction_controller)
        self.line_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        charts_layout.addWidget(self.line_chart)

        # Add a spacer between the line chart and the progress bars
        charts_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Budget Progress
        self.budget_progress = BudgetProgress(self.user_id, self.budget_controller, self.transaction_controller)
        self.budget_progress.setFixedWidth(350)  # Set a fixed width for progress bars
        charts_layout.addWidget(self.budget_progress)

        # Add the horizontal charts layout to the main layout
        main_layout.addLayout(charts_layout)

        # Spacer between charts and button
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

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
        main_layout.addWidget(self.savings_button, alignment=Qt.AlignCenter)

        # Set the main layout
        self.setLayout(main_layout)

    def update_dashboard(self):
        """Update the dashboard with the latest user info and monthly spending."""
        logged_in_user = None
        if logged_in_user:
            self.welcome_label.setText(f"Welcome!")
            self.user_id = logged_in_user.user_id
        else:
            self.welcome_label.setText("Welcome!")
            self.user_id = None

        print(f"User ID: {self.user_id}")
        total_spending = self.transaction_controller.calculate_monthly_spending(
            self.user_id
        )
        print(f"Total spending this month: {total_spending}")
        self.spending_label.setText(f"Total Spending This Month: Rp {total_spending:.2f}")

        # Update child widgets
        self.line_chart.update_chart()
        self.budget_progress.update_progress(self.user_id)
    
    def income_vs_outcome_chart(self):
        """Placeholder for the income vs outcome chart logic"""
        pass

    def monthly_income_outcome_chart(self):
        """Placeholder for monthly income vs outcome chart logic"""
        pass

    def current_vs_budget_chart(self):
        """Placeholder for current vs budget chart logic"""
        pass

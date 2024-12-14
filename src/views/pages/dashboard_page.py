from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QVBoxLayout, QWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import datetime


# Donut Chart for Outcome Categories
class DonutChart(QWidget):
    def __init__(self, user_id, transaction_controller, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.transaction_controller = transaction_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.canvas)

        self.category_data = self.get_category_data()  # Get the data for categories
        self.plot_donut_chart()

        self.setLayout(layout)

    def get_category_data(self):
        """Fetch current month's outcome for each category"""
        # Placeholder for actual logic to fetch data from the database
        current_month = datetime.datetime.now().month
        data = {
            'Food': 1200,
            'Transportation': 500,
            'Entertainment': 300,
            'Education': 200,
            'Others': 100,
        }
        return data

    def plot_donut_chart(self):
        """Plot the donut chart with the category data"""
        data = self.category_data
        labels = data.keys()
        sizes = data.values()
        explode = (0.1, 0, 0, 0, 0)  # "explode" the first slice (Food)

        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85)

        # Draw a white circle in the center to make it a donut chart
        centre_circle = plt.Circle((0, 0), 0.70, color='white')
        fig.gca().add_artist(centre_circle)

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        self.canvas.draw()

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


# Main DashboardPage
class DashboardPage(QWidget):
    def __init__(self, user_id, budget_controller, transaction_controller):
        super().__init__()
        self.user_id = user_id
        self.budget_controller = budget_controller
        self.transaction_controller = transaction_controller
        self.setWindowTitle("Dashboard")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create widgets for charts
        donut_chart = DonutChart(self.user_id, self.transaction_controller)
        line_chart = LineChart(self.user_id, self.transaction_controller)
        budget_progress = BudgetProgress(self.user_id, self.budget_controller, self.transaction_controller)

        layout.addWidget(donut_chart)
        layout.addWidget(line_chart)
        layout.addWidget(budget_progress)

        self.setLayout(layout)

    def update_dashboard(self):
        """Update dashboard with current data"""
        self.income_vs_outcome_chart()
        self.monthly_income_outcome_chart()
        self.current_vs_budget_chart()
        pass

    def income_vs_outcome_chart(self):
        """Placeholder for the income vs outcome chart logic"""
        pass

    def monthly_income_outcome_chart(self):
        """Placeholder for monthly income vs outcome chart logic"""
        pass

    def current_vs_budget_chart(self):
        """Placeholder for current vs budget chart logic"""
        pass

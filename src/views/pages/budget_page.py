#src/views/pages/budget_page.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QDialog, QLabel, 
    QFormLayout, QTableWidget, QLineEdit, QDateEdit, QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView, QComboBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from decimal import Decimal
from datetime import datetime
from models.budget import Category

class BudgetPage(QWidget):
    def __init__(self, user_id, controller, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        
        # Create table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels([
            'Category', 'Amount', 'Start Date', 'End Date'
        ])
        
        # Set table properties
        header = self.table_widget.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
            
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f7f7f7;
                border: 1px solid #ddd;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 6px;
                border: none;
                border-bottom: 1px solid #ddd;
            }
        """)
        
        self.layout.addWidget(self.table_widget)

        # Connect table item double click
        self.table_widget.itemDoubleClicked.connect(self.show_budget_detail)
        
        # Initial refresh to load data
        self.refresh_budget_list()

    def refresh_budget_list(self):
        self.table_widget.setRowCount(0)
        budgets = self.controller.get_all_budgets(self.user_id)
        
        for row, budget in enumerate(budgets):
            self.table_widget.insertRow(row)
            try:
                # Category
                category_item = QTableWidgetItem(budget.category.value)
                self.table_widget.setItem(row, 0, category_item)
                
                # Amount
                amount_str = f"Rp {int(budget.amount):,}"
                amount_item = QTableWidgetItem(amount_str)
                self.table_widget.setItem(row, 1, amount_item)
                
                # Start Date
                start_date = datetime.strptime(budget.start_date, "%Y-%m-%d %H:%M:%S.%f")
                start_date_str = start_date.strftime("%d %b %Y")
                start_date_item = QTableWidgetItem(start_date_str)
                self.table_widget.setItem(row, 2, start_date_item)
                
                # End Date
                end_date = datetime.strptime(budget.end_date, "%Y-%m-%d %H:%M:%S.%f")
                end_date_str = end_date.strftime("%d %b %Y")
                end_date_item = QTableWidgetItem(end_date_str)
                self.table_widget.setItem(row, 3, end_date_item)
            except Exception as e:
                print(f"Error processing budget: {e}")

    def show_budget_detail(self, item):
        row = item.row()
        budgets = self.controller.get_all_budgets(self.user_id)
        if row < len(budgets):
            budget = budgets[row]
            dialog = BudgetForm(
                user_id=self.user_id,
                controller=self.controller,
                budget=budget,
                parent=self
            )
            if dialog.exec_():
                self.refresh_budget_list()

class BudgetForm(QDialog):
    def __init__(self, user_id, controller, budget=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.controller = controller
        self.budget = budget

        self.setWindowTitle("Edit Budget")
        self.setMinimumSize(300, 200)

        self.layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        
        # Category should be display-only since it can't be changed
        self.category_label = QLabel(budget.category.value.title() if budget else "")
        self.amount_input = QLineEdit(str(budget.amount) if budget else "")
        self.start_date_input = QDateEdit()
        self.end_date_input = QDateEdit()
        
        # Convert string dates to QDate
        if budget:
            # Try multiple date parsing formats
            start_date = self._parse_date(budget.start_date)
            end_date = self._parse_date(budget.end_date)
            
            self.start_date_input.setDate(QDate(start_date.year, start_date.month, start_date.day))
            self.end_date_input.setDate(QDate(end_date.year, end_date.month, end_date.day))
        else:
            self.start_date_input.setDate(QDate.currentDate())
            self.end_date_input.setDate(QDate.currentDate())

        self.start_date_input.setCalendarPopup(True)
        self.end_date_input.setCalendarPopup(True)

        form_layout.addRow("Category:", self.category_label)
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

    def _parse_date(self, date_str):
        """
        Try multiple date parsing formats
        """
        date_formats = [
            "%Y-%m-%d %H:%M:%S.%f",  # Full timestamp with microseconds
            "%Y-%m-%d %H:%M:%S",     # Timestamp without microseconds
            "%Y-%m-%d",              # Date only
        ]

        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_str}")

    def save_budget(self):
        try:
            amount = Decimal(self.amount_input.text())
        except:
            QMessageBox.warning(self, "Error", "Amount must be a valid number.")
            return

        start_date = self.start_date_input.date().toPyDate()
        end_date = self.end_date_input.date().toPyDate()

        if amount > 0 and start_date < end_date:
            # Only update allowed
            success, message = self.controller.update_budget(
                self.budget.budget_id, amount=amount, 
                start_date=start_date, end_date=end_date
            )

            if success:
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)
        else:
            QMessageBox.warning(self, "Error", "Please provide valid inputs.")
   

class BudgetDetailDialog(QDialog):
    def __init__(self, budget, controller, parent=None):
        super().__init__(parent)
        self.budget = budget
        self.controller = controller

        self.setWindowTitle("Budget Details")
        self.setMinimumSize(400, 300)

        self.layout = QVBoxLayout(self)

        # Details form layout
        details_layout = QFormLayout()
        details_layout.addRow("Category:", QLabel(budget.category.value))

        # Amount details
        self.total_amount_label = QLabel(f"Rp {int(budget.amount):,}")
        details_layout.addRow("Total Amount:", self.total_amount_label)

        self.current_amount_label = QLabel(f"Rp {int(budget.current_amount):,}")
        details_layout.addRow("Current Amount:", self.current_amount_label)

        # Editable dates
        self.start_date_input = QDateEdit()
        self.end_date_input = QDateEdit()
        
        # Convert string dates to QDate
        start_date = datetime.strptime(budget.start_date, "%Y-%m-%d %H:%M:%S.%f")
        end_date = datetime.strptime(budget.end_date, "%Y-%m-%d %H:%M:%S.%f")
        
        self.start_date_input.setDate(QDate(start_date.year, start_date.month, start_date.day))
        self.end_date_input.setDate(QDate(end_date.year, end_date.month, end_date.day))

        self.start_date_input.setCalendarPopup(True)
        self.end_date_input.setCalendarPopup(True)

        details_layout.addRow("Start Date:", self.start_date_input)
        details_layout.addRow("End Date:", self.end_date_input)

        # Additional details
        remaining_label = QLabel(f"Rp {int(budget.get_remaining()):,}")
        details_layout.addRow("Remaining:", remaining_label)

        progress_label = QLabel(f"{budget.get_percentage_used():.2f}%")
        details_layout.addRow("Progress:", progress_label)

        self.layout.addLayout(details_layout)

        # Buttons
        button_layout = QHBoxLayout()
        
        update_dates_button = QPushButton("Update Dates")
        update_dates_button.clicked.connect(self.update_budget_dates)
        button_layout.addWidget(update_dates_button)

        update_button = QPushButton("Update Budget")
        update_button.clicked.connect(self.update_budget)
        button_layout.addWidget(update_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)

        self.layout.addLayout(button_layout)

    def update_budget_dates(self):
        start_date = self.start_date_input.date().toPyDate()
        end_date = self.end_date_input.date().toPyDate()

        if start_date < end_date:
            success, message = self.controller.update_budget(
                self.budget.budget_id, 
                start_date=start_date, 
                end_date=end_date
            )

            if success:
                QMessageBox.information(self, "Success", "Budget dates updated successfully.")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)
        else:
            QMessageBox.warning(self, "Error", "Start date must be before end date.")

    def update_budget(self):
        dialog = BudgetForm(
            user_id=self.budget.user_id, 
            controller=self.controller, 
            budget=self.budget, 
            parent=self
        )
        if dialog.exec_():  
            self.accept()  # Close the details dialog
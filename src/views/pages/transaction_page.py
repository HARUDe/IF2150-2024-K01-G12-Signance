#src/views/pages/transaction_page.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea,
    QFormLayout, QLineEdit, QComboBox, QHBoxLayout, QMessageBox,
    QDialog, QFrame
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QFont, QColor
from decimal import Decimal
from models.transaction import TransactionType
from models.budget import Category
from datetime import datetime

class TransactionWidget(QFrame):
    def __init__(self, transaction, parent=None):
        super().__init__(parent)
        self.transaction = transaction
        self.setObjectName("transactionWidget")
        self.setStyleSheet("""
            #transactionWidget {
                background-color: white;
                border-radius: 8px;
                margin: 4px;
                padding: 12px;
            }
            #transactionWidget:hover {
                background-color: #f5f5f5;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Left side - Date and Description
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(4)
        
        # Convert string date to datetime if needed
        if isinstance(transaction.date, str):
            try:
                # Assuming the date string is in ISO format (YYYY-MM-DD)
                date_obj = datetime.strptime(transaction.date, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d %b")
            except ValueError:
                # Fallback if date string is in unexpected format
                formatted_date = transaction.date
        else:
            # If it's already a datetime object
            formatted_date = transaction.date.strftime("%d %b")
            
        date = QLabel(formatted_date)
        date.setStyleSheet("color: #666; font-size: 13px;")
        description = QLabel(transaction.description)
        description.setStyleSheet("font-size: 15px; font-weight: bold;")
        category = QLabel(transaction.category)
        category.setStyleSheet("color: #666; font-size: 13px;")
        
        left_layout.addWidget(date)
        left_layout.addWidget(description)
        left_layout.addWidget(category)
        
        # Right side - Amount
        amount_str = f"{'+' if transaction.transaction_type == TransactionType.INCOME else '-'} Rp.{abs(transaction.amount):.2f}"
        amount = QLabel(amount_str)
        amount.setStyleSheet(
            f"font-size: 15px; font-weight: bold; color: {'#2ecc71' if transaction.transaction_type == TransactionType.INCOME else '#e74c3c'};"
        )
        amount.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        layout.addWidget(left_widget, stretch=1)
        layout.addWidget(amount)

class TransactionPage(QWidget):
    def __init__(self, user_id, controller, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.controller = controller
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
            }
            QPushButton#addButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 25px;
                font-size: 24px;
                font-weight: bold;
                border: none;
                padding: 10px;
            }
            QPushButton#addButton:hover {
                background-color: #27ae60;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(16)

        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Transactions")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        date_range = QLabel(QDate.currentDate().toString("MM/dd/yyyy"))
        date_range.setStyleSheet("color: #666;")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(date_range)
        
        self.layout.addWidget(header)

        # Scroll area for transactions
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        self.transactions_layout = QVBoxLayout(scroll_content)
        self.transactions_layout.setSpacing(8)
        scroll.setWidget(scroll_content)
        
        self.layout.addWidget(scroll)

        # Floating add button
        self.add_button = QPushButton("+")
        self.add_button.setObjectName("addButton")
        self.add_button.setFixedSize(50, 50)
        self.add_button.clicked.connect(self.show_create_transaction_dialog)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_button)
        self.layout.addLayout(button_layout)

        # Load transactions
        self.refresh_transaction_list()

    def refresh_transaction_list(self):
        # Clear existing transactions
        while self.transactions_layout.count():
            child = self.transactions_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add new transactions
        transactions = self.controller.get_transactions_by_user_id(self.user_id)
        for transaction in transactions:
            widget = TransactionWidget(transaction)
            widget.mousePressEvent = lambda _, t=transaction: self.show_transaction_detail(t)
            self.transactions_layout.addWidget(widget)
        
        # Add stretch at the end
        self.transactions_layout.addStretch()

    def show_create_transaction_dialog(self):
        dialog = TransactionForm(user_id=self.user_id, controller=self.controller, parent=self)
        if dialog.exec_():
            self.refresh_transaction_list()

    def show_transaction_detail(self, transaction):
        dialog = TransactionDetailDialog(transaction=transaction, controller=self.controller, parent=self)
        if dialog.exec_():
            self.refresh_transaction_list()

class TransactionForm(QDialog):
    def __init__(self, user_id, controller, transaction=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.controller = controller
        self.transaction = transaction
        
        self.setWindowTitle("Add Transaction" if not transaction else "Edit Transaction")
        self.setMinimumSize(400, 250)
        
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                min-width: 200px;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                border: none;
                color: white;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton#saveButton {
                background-color: #2ecc71;
            }
            QPushButton#saveButton:hover {
                background-color: #27ae60;
            }
            QPushButton#cancelButton {
                background-color: #95a5a6;
            }
            QPushButton#cancelButton:hover {
                background-color: #7f8c8d;
            }
        """)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)

        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # Amount input
        self.amount_input = QLineEdit(str(transaction.amount) if transaction else "")
        self.amount_input.setPlaceholderText("Enter amount")
        
        # Category dropdown
        self.category_input = QComboBox()
        self.category_input.addItems([e.value for e in Category])
        if transaction:
            self.category_input.setCurrentText(transaction.category)
        
        # Transaction type dropdown
        self.type_input = QComboBox()
        self.type_input.addItems([e.value for e in TransactionType])
        if transaction:
            self.type_input.setCurrentText(transaction.transaction_type.value)
        
        # Description input
        self.description_input = QLineEdit(transaction.description if transaction else "")
        self.description_input.setPlaceholderText("Enter description")

        # Add form fields
        form_layout.addRow("Amount:", self.amount_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Type:", self.type_input)
        form_layout.addRow("Description:", self.description_input)
        
        self.layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        save_button = QPushButton("Save")
        save_button.setObjectName("saveButton")
        save_button.clicked.connect(self.save_transaction)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        self.layout.addSpacing(8)
        self.layout.addLayout(button_layout)

    def save_transaction(self):
        try:
            amount = Decimal(self.amount_input.text())
        except:
            QMessageBox.warning(self, "Error", "Amount must be a valid number.")
            return
        
        amount = int(amount * 100) // 100  # Round to 2 decimal places
        
        category = self.category_input.currentText()
        transaction_type = self.type_input.currentText()
        description = self.description_input.text()

        if category and amount > 0:
            # Show a confirmation dialog before saving the transaction
            confirm = QMessageBox.question(
                self, "Confirm Transaction", 
                f"Are you sure you want to create a transaction of Rp.{amount} in category '{category}'?", 
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                if self.transaction:  # Update existing transaction
                    self.controller.update_transaction(
                        self.transaction.transaction_id, amount, category, transaction_type, description
                    )
                else:  # Create new transaction
                    self.controller.create_transaction(self.user_id, amount, category, transaction_type, description)

                self.accept()
            else:
                self.reject()  # Reject the dialog if user clicks 'No'
        else:
            QMessageBox.warning(self, "Error", "Please provide valid inputs.")

class TransactionDetailDialog(QDialog):
    def __init__(self, transaction, controller, parent=None):
        super().__init__(parent)
        self.transaction = transaction
        self.controller = controller

        self.setWindowTitle("Transaction Details")
        self.setMinimumSize(400, 300)
        
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 14px;
                padding: 4px 0;
            }
            QLabel.title {
                font-size: 18px;
                font-weight: bold;
                padding: 8px 0;
            }
            QLabel.value {
                color: #333;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                border: none;
                color: white;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton#updateButton {
                background-color: #3498db;
            }
            QPushButton#updateButton:hover {
                background-color: #2980b9;
            }
            QPushButton#deleteButton {
                background-color: #e74c3c;
            }
            QPushButton#deleteButton:hover {
                background-color: #c0392b;
            }
            QPushButton#closeButton {
                background-color: #95a5a6;
            }
            QPushButton#closeButton:hover {
                background-color: #7f8c8d;
            }
        """)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)

        # Title
        title = QLabel("Transaction Details")
        title.setProperty("class", "title")
        self.layout.addWidget(title)

        # Details grid
        details_layout = QFormLayout()
        details_layout.setSpacing(12)

        # Format date the same way as in TransactionWidget
        if isinstance(transaction.date, str):
            try:
                date_obj = datetime.strptime(transaction.date, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d %b %Y")
            except ValueError:
                formatted_date = transaction.date
        else:
            formatted_date = transaction.date.strftime("%d %b %Y")

        # Add details with consistent styling
        details = [
            ("Category:", transaction.category),
            ("Amount:", f"Rp.{transaction.amount:.2f}"),
            ("Type:", transaction.transaction_type.value),
            ("Description:", transaction.description),
            ("Date:", formatted_date)
        ]

        for label_text, value in details:
            label = QLabel(label_text)
            value_label = QLabel(str(value))
            value_label.setProperty("class", "value")
            details_layout.addRow(label, value_label)

        self.layout.addLayout(details_layout)
        self.layout.addSpacing(16)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        update_button = QPushButton("Update")
        update_button.setObjectName("updateButton")
        update_button.clicked.connect(self.update_transaction)

        delete_button = QPushButton("Delete")
        delete_button.setObjectName("deleteButton")
        delete_button.clicked.connect(self.delete_transaction)

        close_button = QPushButton("Close")
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(close_button)

        self.layout.addLayout(button_layout)

    def update_transaction(self):
        dialog = TransactionForm(
            user_id=self.transaction.user_id, 
            controller=self.controller,
            transaction=self.transaction, 
            parent=self
        )
        if dialog.exec_():  # If the dialog is accepted
            self.accept()  # Close the details dialog

    def delete_transaction(self):
        confirm = QMessageBox.question(
            self, 
            "Confirm Deletion", 
            "Are you sure you want to delete this transaction?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.controller.delete_transaction(self.transaction.transaction_id)
            self.accept()
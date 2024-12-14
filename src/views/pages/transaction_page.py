from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QDialog, QLabel,
    QFormLayout, QLineEdit, QComboBox, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from decimal import Decimal
from models.transaction import TransactionType
from models.budget import Category

class TransactionPage(QWidget):
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
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.add_button.clicked.connect(self.show_create_transaction_dialog)

        # Floating button container
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_button)
        button_layout.setContentsMargins(0, 0, 10, 10)
        self.layout.addLayout(button_layout)

        # Connect list item click to the detail dialog
        self.list_widget.itemClicked.connect(self.show_transaction_detail)

        # Load transactions
        self.refresh_transaction_list()

    def refresh_transaction_list(self):
        self.list_widget.clear()
        transactions = self.controller.get_transactions_by_user_id(self.user_id)
        for transaction in transactions:
            self.list_widget.addItem(f"{transaction.category} - {transaction.amount} ({transaction.transaction_type.value})")

    def show_create_transaction_dialog(self):
        dialog = TransactionForm(user_id=self.user_id, controller=self.controller, parent=self)
        if dialog.exec_():  # If the dialog is accepted
            self.refresh_transaction_list()

    def show_transaction_detail(self, item):
        transaction_id = self.get_selected_transaction_id()
        selected_transaction = self.controller.get_transaction_by_id(transaction_id)
        if selected_transaction:
            dialog = TransactionDetailDialog(transaction=selected_transaction, controller=self.controller, parent=self)
            if dialog.exec_():  # If any updates or deletions are made
                self.refresh_transaction_list()
    
    def get_selected_transaction_id(self):
        current_row = self.list_widget.currentRow()
        if current_row != -1:
            return self.controller.get_all_transactions()[current_row].transaction_id
        return None


class TransactionForm(QDialog):
    def __init__(self, user_id, controller, transaction=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.controller = controller
        self.transaction = transaction

        self.setWindowTitle("Add Transaction" if not transaction else "Edit Transaction")
        self.setMinimumSize(300, 200)

        self.layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.amount_input = QLineEdit(str(transaction.amount) if transaction else "")

        self.category_input = QComboBox()
        self.category_input.addItems([e.value for e in Category])
        self.category_input.setCurrentText(transaction.category if transaction else "")

        self.type_input = QComboBox()
        self.type_input.addItems([e.value for e in TransactionType])
        self.type_input.setCurrentText(transaction.transaction_type.value if transaction else "")
        self.description_input = QLineEdit(transaction.description if transaction else "")

        form_layout.addRow("Amount:", self.amount_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Type:", self.type_input)
        form_layout.addRow("Description:", self.description_input)
        self.layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_transaction)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

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
                f"Are you sure you want to create a transaction of Rp {amount} in category '{category}'?", 
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
        self.setMinimumSize(300, 200)

        self.layout = QVBoxLayout(self)

        # Details
        self.layout.addWidget(QLabel(f"Category    :    {transaction.category}"))
        self.layout.addWidget(QLabel(f"Amount      : Rp {transaction.amount}"))
        self.layout.addWidget(QLabel(f"Type        :    {transaction.transaction_type.value}"))
        self.layout.addWidget(QLabel(f"Description :    {transaction.description}"))
        self.layout.addWidget(QLabel(f"Date        : {transaction.date}"))

        # Buttons
        button_layout = QHBoxLayout()
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_transaction)
        button_layout.addWidget(update_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_transaction)
        button_layout.addWidget(delete_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)

        self.layout.addLayout(button_layout)

    def update_transaction(self):
        dialog = TransactionForm(user_id=self.transaction.user_id, controller=self.controller,
                                 transaction=self.transaction, parent=self)
        if dialog.exec_():  # If the dialog is accepted
            self.accept()  # Close the details dialog

    def delete_transaction(self):
        confirm = QMessageBox.question(
            self, "Confirm Deletion", "Are you sure you want to delete this transaction?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.controller.delete_transaction(self.transaction.transaction_id)
            self.accept()

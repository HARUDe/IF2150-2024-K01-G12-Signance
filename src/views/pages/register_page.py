# src/views/pages/register_page.py

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from controllers.user_controller import UserController

class RegisterPage(QWidget):

    def __init__(self, main_window=None):
        super().__init__()
        self.setWindowTitle("Register")
        self.main_window = main_window
        self.user_controller = UserController()
        self.init_ui()
    
    def init_ui(self):
        # Create main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Add title
        title = QLabel("Register")
        title.setStyleSheet("font-size: 24px; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Create form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 8px;")
        form_layout.addWidget(self.username_input)
        
        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet("padding: 8px;")
        form_layout.addWidget(self.email_input)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 8px;")
        form_layout.addWidget(self.password_input)
        
        # Register button
        register_button = QPushButton("Register")
        register_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        register_button.clicked.connect(self.handle_register)
        
        # Add form layout to main layout
        layout.addLayout(form_layout)
        layout.addWidget(register_button)
        
        self.setLayout(layout)

    def handle_register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        
        if not username or not email or not password:
            QMessageBox.critical(self, "Error", "Please fill in all fields.")
            return
        
        user = self.user_controller.register(username, email, password)
        
        if user:
            QMessageBox.information(self, "Success", "User registered successfully.")
            self.main_window.switch_page("Login")
        else:
            QMessageBox.critical(self, "Error", "Failed to register user.")
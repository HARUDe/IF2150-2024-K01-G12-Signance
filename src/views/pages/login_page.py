# src/views/pages/login_page.py

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from controllers.user_controller import UserController

class LoginPage(QWidget):
    # Signal emitted when login is successful
    login_successful = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.user_controller = UserController()
        self.init_ui()
        
    def init_ui(self):
        # Create main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Add title
        title = QLabel("Welcome to Signance")
        title.setStyleSheet("font-size: 24px; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Create form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        # Username input
        self.username_or_email_input = QLineEdit()
        self.username_or_email_input.setPlaceholderText("Username/Email")
        self.username_or_email_input.setStyleSheet("padding: 8px;")
        form_layout.addWidget(self.username_or_email_input)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 8px;")
        form_layout.addWidget(self.password_input)
        
        # Login button
        login_button = QPushButton("Login")
        login_button.setStyleSheet("""
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
        login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(login_button)
        
        # Add form to main layout
        layout.addLayout(form_layout)
        self.setLayout(layout)
    
    def handle_login(self):
        username_email = self.username_or_email_input.text()
        password = self.password_input.text()
        
        if self.user_controller.login(username_email, password):
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, "Error", "Invalid username_email or password")
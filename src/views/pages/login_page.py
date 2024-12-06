# src/views/pages/login_page.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt

class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 8px;")
        form_layout.addWidget(self.username_input)
        
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
        
        # Register link
        register_button = QPushButton("Don't have an account? Register")
        register_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: blue;
                text-align: center;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        register_button.clicked.connect(self.show_register)
        form_layout.addWidget(register_button)
        
        # Add form to main layout
        layout.addLayout(form_layout)
        self.setLayout(layout)
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Kalau sudah ada database, bisa cek username dan password di sini
        if username and password:
            self.main_window.show_dashboard()
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
    
    def show_register(self):
        # Kalau sudah ada register page, bisa dipanggil di sini
        QMessageBox.information(self, "Register", "Registration page coming soon!")
# src/views/pages/register_page.py

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from controllers.user_controller import UserController

class RegisterPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.user_controller = UserController()
        self.error_labels = {}
        self.init_ui()
        
    def init_ui(self):
        # Membuat layout utama
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # Membuat widget dan layout kiri
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        left_layout.setContentsMargins(40, 40, 40, 40)
        
        # Menambahkan logo dan nama brand
        brand_layout = QHBoxLayout()
        logo_label = QLabel("Σ")
        logo_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-right: 10px;
        """)
        brand_name = QLabel("Signance")
        brand_name.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)
        brand_layout.addWidget(logo_label)
        brand_layout.addWidget(brand_name)
        brand_layout.addStretch()
        left_layout.addLayout(brand_layout)
        
        left_layout.addSpacing(40)
        
        # Menambahkan judul halaman
        title = QLabel("Sign up")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        """)
        left_layout.addWidget(title)
        
        # Menambahkan subjudul halaman
        subtitle = QLabel("Sign up to enjoy the feature of Signance")
        subtitle.setStyleSheet("color: #666; margin-bottom: 20px;")
        left_layout.addWidget(subtitle)
        
        # Menambahkan label dan input untuk username
        name_label = QLabel("Username")
        name_label.setStyleSheet("color: #666; margin-bottom: 5px;")
        left_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
                margin-bottom: 15px;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)
        self.name_input.setPlaceholderText("Enter your username")
        left_layout.addWidget(self.name_input)
        
        # Menambahkan label dan input untuk email
        email_label = QLabel("Email")
        email_label.setStyleSheet("color: #666; margin-bottom: 5px;")
        left_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
                margin-bottom: 15px;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)
        self.email_input.setPlaceholderText("Enter your email")
        left_layout.addWidget(self.email_input)
        
        # Menambahkan label dan input untuk password
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #666; margin-bottom: 5px;")
        left_layout.addWidget(password_label)
        
        password_container = QHBoxLayout()
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)
        self.password_input.setPlaceholderText("Enter your password")
        
        # Menambahkan tombol untuk toggle visibility password
        self.toggle_password_button = QPushButton("👁")
        self.toggle_password_button.setFixedSize(30, 30)
        self.toggle_password_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
        """)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)
        
        password_container.addWidget(self.password_input)
        password_container.addWidget(self.toggle_password_button)
        left_layout.addLayout(password_container)
        left_layout.addSpacing(15) 
        
        # Menambahkan tombol untuk register
        self.register_button = QPushButton("Sign up")
        self.register_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #244F24;
            }
        """)
        self.register_button.clicked.connect(self.handle_register)
        left_layout.addWidget(self.register_button)
        
        # Menambahkan separator
        separator_layout = QHBoxLayout()
        separator_label = QLabel("or")
        separator_label.setStyleSheet("color: #666;")
        separator_label.setAlignment(Qt.AlignCenter)
        separator_layout.addWidget(separator_label)
        left_layout.addLayout(separator_layout)
        
        # Menambahkan layout untuk login
        login_layout = QHBoxLayout()
        login_layout.setAlignment(Qt.AlignCenter)

        container = QWidget() 
        container_layout = QHBoxLayout()  
        container.setLayout(container_layout)

        login_label = QLabel("Already have an account?")
        login_label.setStyleSheet("color: #666;")

        login_button = QPushButton("Sign in")
        login_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: #2196F3;
                font-weight: bold;
                text-decoration: none;
                background: transparent;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        login_button.clicked.connect(lambda: self.main_window.switch_page("Login"))

        container_layout.addWidget(login_label)
        container_layout.addWidget(login_button)
        container_layout.setContentsMargins(0, 0, 0, 0)

        login_layout.addWidget(container)
        left_layout.addLayout(login_layout)
        
        left_layout.addStretch()
        
        # Membuat widget dan layout kanan
        right_widget = QWidget()
        right_widget.setStyleSheet("""
            background-color: #2c2c2c;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            background: qlineargradient(
                spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #2c2c2c, stop: 0.5 #3a3a3a, stop: 1 #1a1a1a
            );
        """)
        
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        
        main_layout.setStretch(0, 1) 
        main_layout.setStretch(1, 1)  

    def show_error(self, input_field, message):
        # Menampilkan pesan error pada input field
        input_field.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #FF3B30;
                border-radius: 4px;
                background: white;
                margin-bottom: 0px;
            }
            QLineEdit:focus {
                border: 1px solid #FF3B30;
            }
        """)
        
        if input_field not in self.error_labels:
            error_label = QLabel(message)
            error_label.setStyleSheet("""
                color: #FF3B30; 
                font-size: 12px;
                padding: 0px;
                margin-top: 4px;
                margin-bottom: 8px;
            """)
            
            parent_layout = input_field.parent().layout()
            if isinstance(parent_layout, QHBoxLayout):
                # Untuk field password dalam layout horizontal
                parent_widget = input_field.parent()
                main_layout = parent_widget.parent().layout()
                index = main_layout.indexOf(parent_widget)
                main_layout.insertWidget(index + 1, error_label)
            else:
                # Untuk field input lainnya
                index = parent_layout.indexOf(input_field)
                parent_layout.insertWidget(index + 1, error_label)
            
            self.error_labels[input_field] = error_label
        else:
            self.error_labels[input_field].setText(message)
            self.error_labels[input_field].show()

    def clear_error(self, input_field):
        # Menghapus pesan error pada input field
        normal_style = """
            QLineEdit {
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
                margin-bottom: 15px;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """
        input_field.setStyleSheet(normal_style)
        
        if input_field in self.error_labels:
            self.error_labels[input_field].hide()

    def toggle_password_visibility(self):
        # Mengubah visibility password
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_button.setText("🔒")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_button.setText("👁")

    def validate_input(self):
        # Validasi input dari user
        is_valid = True
        
        if not self.name_input.text():
            self.show_error(self.name_input, "Username is required")
            is_valid = False
        
        if not self.email_input.text():
            self.show_error(self.email_input, "Email is required")
            is_valid = False
        
        if not self.password_input.text():
            self.show_error(self.password_input, "Password is required")
            is_valid = False
            
        return is_valid

    def handle_register(self):
        # Menghapus pesan error sebelumnya
        self.clear_error(self.name_input)
        self.clear_error(self.email_input)
        self.clear_error(self.password_input)
         
        # Validasi input
        if not self.validate_input():
            return
            
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        
        # Mencoba melakukan registrasi user
        success, message = self.user_controller.register(name, email, password)
        if success:
            QMessageBox.information(self, "Success", message)
            self.main_window.switch_page("Login")
        else:
            if "username" in message.lower():
                self.show_error(self.name_input, message)
            elif "email" in message.lower():
                self.show_error(self.email_input, message)
            else:
                QMessageBox.critical(self, "Error", message)
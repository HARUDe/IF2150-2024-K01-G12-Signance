# src/views/pages/login_page.py

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from controllers.user_controller import UserController


class LoginPage(QWidget):
    login_successful = pyqtSignal(str)

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.user_controller = UserController()
        self.error_labels = {}
        self.init_ui()
        
    def init_ui(self):
        # Layout utama horizontal
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # Bagian kiri untuk form login
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        left_layout.setContentsMargins(40, 40, 40, 40)
        
        # Bagian logo/brand
        brand_layout = QHBoxLayout()
        logo_label = QLabel()
        pixmap = QPixmap("img/no_text.png")  
        logo_label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)) 
        logo_label.setAlignment(Qt.AlignCenter) 
        brand_name = QLabel("Signance")
        brand_name.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)
        brand_layout.addWidget(logo_label)
        brand_layout.addWidget(brand_name)
        brand_layout.addStretch()
        left_layout.addLayout(brand_layout)
        
        # Tambahkan spasi
        left_layout.addSpacing(40)
        
        # Bagian judul
        title = QLabel("Sign in")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        """)
        left_layout.addWidget(title)
        
        subtitle = QLabel("Please login to continue to your account.")
        subtitle.setStyleSheet("color: #666; margin-bottom: 20px;")
        left_layout.addWidget(subtitle)
        
        # Bagian form
        email_label = QLabel("Email/Username")
        email_label.setStyleSheet("color: #666; margin-bottom: 5px;")
        left_layout.addWidget(email_label)
        
        self.email_or_username_input = QLineEdit()
        self.email_or_username_input.setStyleSheet("""
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
        self.email_or_username_input.setPlaceholderText("Enter your email/username")
        self.email_or_username_input.textChanged.connect(
            lambda: self.clear_error(self.email_or_username_input))
        left_layout.addWidget(self.email_or_username_input)
        
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #666; margin-bottom: 5px;")
        left_layout.addWidget(password_label)
        
        # Input password dengan tombol show/hide
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
        self.password_input.textChanged.connect(
            lambda: self.clear_error(self.password_input))
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
        left_layout.addSpacing(15)  # Tambahkan spasi setelah field password
        
        # Tombol sign in
        self.login_button = QPushButton("Sign in")
        self.login_button.setStyleSheet("""
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
        self.login_button.clicked.connect(self.handle_login)
        left_layout.addWidget(self.login_button)
        
        # Separator
        separator_layout = QHBoxLayout()
        separator_label = QLabel("or")
        separator_label.setStyleSheet("color: #666;")
        separator_label.setAlignment(Qt.AlignCenter)
        separator_layout.addWidget(separator_label)
        left_layout.addLayout(separator_layout)
        
        # Link register
        register_layout = QHBoxLayout()
        register_layout.setAlignment(Qt.AlignCenter)  

        container = QWidget()  # Buat widget container untuk label
        container_layout = QHBoxLayout()  # Buat layout untuk container
        container.setLayout(container_layout)

        register_label = QLabel("Need an account?")
        register_label.setStyleSheet("color: #666;")

        register_button = QPushButton("Create one")
        register_button.setStyleSheet("""
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
        register_button.clicked.connect(lambda: self.main_window.switch_page("Register"))

        container_layout.addWidget(register_label)
        container_layout.addWidget(register_button)
        container_layout.setContentsMargins(0, 0, 0, 0)  # Hapus margin container

        register_layout.addWidget(container)  # Tambahkan container ke layout utama
        left_layout.addLayout(register_layout)  # Tambahkan layout utama ke layout kiri
            
        # Tambahkan stretch untuk mendorong semuanya ke atas
        left_layout.addStretch()
        
        # Bagian kanan (latar belakang gelap)
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

        # Create a QLabel for the image and add it to the right widget
        image_label = QLabel()
        pixmap = QPixmap("img/white_text.png")  # Path to the image
        image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Adjust size as needed
        image_label.setAlignment(Qt.AlignCenter)

        right_layout = QVBoxLayout()
        right_layout.addWidget(image_label)
        right_widget.setLayout(right_layout)
        
        # Tambahkan kedua bagian ke layout utama
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        
        # Atur rasio ukuran antara bagian kiri dan kanan (1:1)
        main_layout.setStretch(0, 1)  # Bagian kiri
        main_layout.setStretch(1, 1)  # Bagian kanan
    
    def show_error(self, input_field, message):
        # Terapkan styling error ke input field dengan margin yang dikoreksi
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
        
        # Buat atau perbarui label error dengan spasi yang tepat
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
        # Reset styling input dengan margin yang tepat
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
        # Fungsi untuk toggle visibilitas password
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_button.setText("🔒")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_button.setText("👁")
            
    def validate_input(self):
        # Fungsi untuk validasi input
        is_valid = True
        
        # Validasi email/username
        if not self.email_or_username_input.text():
            self.show_error(self.email_or_username_input, "Email/username is required")
            is_valid = False
        
        # Validasi password
        if not self.password_input.text():
            self.show_error(self.password_input, "Password is required")
            is_valid = False
            
        return is_valid
        
    def handle_login(self):
        # Fungsi untuk menangani login
        email_or_username = self.email_or_username_input.text()
        password = self.password_input.text()
        
        self.clear_error(self.email_or_username_input)
        self.clear_error(self.password_input)
        
        if not self.validate_input():
            return
            
        email_or_username = self.email_or_username_input.text()
        password = self.password_input.text()

        if self.user_controller.login(email_or_username, password):
            self.login_successful.emit(email_or_username)
        else:
            self.show_error(self.email_or_username_input, "Invalid email/username or password")
            self.show_error(self.password_input, "")

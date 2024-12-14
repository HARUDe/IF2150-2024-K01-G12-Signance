from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QSizePolicy, QLabel
)
from .pages import LoginPage, DashboardPage, TransactionPage, BudgetPage, SavingsPage, RegisterPage
from controllers import BudgetController, UserController, TransactionController, SavingsController

budget_controller = BudgetController()
transaction_controller = TransactionController()
saving_controller = SavingsController() 
user_controller = UserController()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signance - Financial Manager")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon("img/no_text.png"))
        self.logged_in = False
        self.user_id = None
        self.user_name = ""  # This will store the logged-in user's name

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Sidebar
        self.sidebar = QVBoxLayout()
        self.sidebar.setContentsMargins(0, 0, 0, 0)
        self.sidebar.setSpacing(10)

        # Pages
        self.pages = {
            "Transactions": None,  # Initially set to None, will be updated after login
            "Dashboard": None,  # Initially set to None, will be updated after login
            "Savings": None,  # Initially set to None, will be updated after login
            "Budget": None,  # Initially set to None, will be updated after login
            "Login": LoginPage(self),
            "Register": RegisterPage(self)
        }

        # Connect LoginPage signal
        login_page = self.pages["Login"]
        login_page.login_successful.connect(self.on_login_successful)

        # Content area
        self.content_area = QStackedWidget()

        # Add all pages to the content area initially
        for page_widget in self.pages.values():
            if page_widget:
                self.content_area.addWidget(page_widget)

        # Add sidebar and content area to the main layout
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setLayout(self.sidebar)
        self.sidebar_widget.setFixedWidth(200)

        main_layout.addWidget(self.sidebar_widget)
        main_layout.addWidget(self.content_area)

        # Set the initial page
        self.update_sidebar()
        self.switch_page("Login")

        # Make content area expand to fill available space
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def update_sidebar(self):
        """Update sidebar buttons based on login state."""
        # Clear the existing sidebar
        while self.sidebar.count():
            item = self.sidebar.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Greeting message for logged-in users
        if self.logged_in:
            greeting_label = QLabel(f"Welcome, {self.user_name}")
            self.sidebar.addWidget(greeting_label)

        # Choose pages based on login state
        pages = (
            ["Dashboard", "Transactions", "Savings", "Budget"]
            if self.logged_in
            else []
        )

        # Create buttons for each page
        for page_name in pages:
            btn = QPushButton(page_name)
            btn.clicked.connect(lambda checked, name=page_name: self.switch_page(name))
            self.sidebar.addWidget(btn)

        self.sidebar.addStretch()

        # Add logout button for logged-in state
        if self.logged_in:
            self.sidebar.addStretch()
            logout_btn = QPushButton("Logout")
            logout_btn.clicked.connect(self.logout)
            self.sidebar.addWidget(logout_btn)

    def switch_page(self, page_name):
        page_widget = self.pages[page_name]
        
        if page_name == "Dashboard":
            page_widget.update_dashboard()

        self.content_area.setCurrentWidget(page_widget)
        # Show or hide the sidebar based on the current page
        if page_name in ["Login", "Register"]:
            self.sidebar_widget.hide()
        else:
            self.sidebar_widget.show()

    def logout(self):
        """Handle logout action."""
        self.logged_in = False
        self.user_name = ""  # Clear user name on logout
        self.update_sidebar()
        self.switch_page("Login")

    def on_login_successful(self, username_or_email):
        """Handle successful login."""
        user_controller = UserController()
        user = user_controller.get_user_by_username_or_email(username_or_email)
        self.logged_in = True
        self.user_id = user[0]
        self.user_name = user[1]  # Update the user name
        self.update_sidebar()

        # Now initialize the pages with the correct user_id and other controllers
        self.pages["Transactions"] = TransactionPage(self.user_id, transaction_controller)
        self.pages["Dashboard"] = DashboardPage(self.user_id, user_controller, transaction_controller, budget_controller, lambda: self.switch_page("Savings"))
        self.pages["Savings"] = SavingsPage(self.user_id, saving_controller)
        self.pages["Budget"] = BudgetPage(self.user_id, budget_controller)

        # Add the pages to the content area
        for page_widget in self.pages.values():
            if page_widget:
                self.content_area.addWidget(page_widget)

        # Switch to the Dashboard page after login
        self.switch_page("Dashboard")
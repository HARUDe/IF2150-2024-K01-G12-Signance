# src/views/main_window.py

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QSizePolicy
)
from .pages import LoginPage, DashboardPage, TransactionPage, BudgetPage, SavingsPage, RegisterPage
from controllers import BudgetController, UserController, TransactionController, SavingsController

budget_controller = BudgetController()
saving_controller = SavingsController() 
transaction_controller = TransactionController() 
user_controller = UserController()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signance - Financial Manager")
        self.setGeometry(100, 100, 1200, 800)
        self.logged_in = False
        self.user_id = None
        
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
            "Dashboard": DashboardPage(user_controller, transaction_controller, lambda: self.switch_page("Savings")),
            "Transactions": TransactionPage(self.user_id, transaction_controller),
            "Savings": SavingsPage(self.user_id, saving_controller),
            "Budget": BudgetPage(self.user_id, budget_controller),
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
        self.update_sidebar()
        self.switch_page("Login")

    def on_login_successful(self):
        """Handle successful login."""
        self.logged_in = True
        self.user_id = 1
        self.update_sidebar()
        self.switch_page("Dashboard")  # Go to the dashboard page
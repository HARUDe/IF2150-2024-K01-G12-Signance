# src/views/main_window.py
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from .pages.login_page import LoginPage
from .pages.dashboard_page import DashboardPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signance - Financial Manager")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create stacked widget for multiple pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize pages
        self.login_page = LoginPage(self)
        self.dashboard_page = DashboardPage(self)
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.dashboard_page)
        
        # Start with login page
        self.show_login_page()
    
    def show_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)
    
    def show_dashboard(self):
        self.stacked_widget.setCurrentWidget(self.dashboard_page)
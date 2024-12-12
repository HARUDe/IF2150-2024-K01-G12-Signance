from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dashboard Coming Soon"))
        self.setLayout(layout)

    def update_dashboard(self):
        # This method is called when switching to the dashboard
        # For now it does nothing, but you can add updates here later
        pass
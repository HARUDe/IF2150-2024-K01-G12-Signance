from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dashboard Coming Soon"))
        self.setLayout(layout)
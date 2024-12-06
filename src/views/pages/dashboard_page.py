from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class DashboardPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dashboard Coming Soon"))
        self.setLayout(layout)
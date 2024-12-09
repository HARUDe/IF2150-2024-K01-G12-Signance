from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class SavingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Savings")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Savings Coming Soon"))
        self.setLayout(layout)
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class BudgetPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Budget Coming Soon"))
        self.setLayout(layout)
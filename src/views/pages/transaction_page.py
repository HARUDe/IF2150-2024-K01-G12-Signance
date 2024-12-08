from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class TransactionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaction")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Transaction Coming Soon"))
        self.setLayout(layout)
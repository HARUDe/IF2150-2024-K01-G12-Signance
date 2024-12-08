from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Register Coming Soon"))
        self.setLayout(layout)
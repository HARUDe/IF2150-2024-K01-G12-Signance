import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow
from database.database import initialize_database

def main():
    # Initialize database
    initialize_database()
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
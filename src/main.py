import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow
#from database.database import initialize_database (kalau udah bikin database, uncomment ini)

def main():
    # Initialize database
    #initialize_database() (kalau udah bikin database, uncomment ini)
    
    # Inisialisasi aplikasi
    app = QApplication(sys.argv)
    
    # Menginisialisasi dan menampilkan main window
    window = MainWindow()
    window.show()
    
    # Run 
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
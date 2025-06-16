from PyQt5.QtWidgets import QApplication
from start_menu import StartMenu

if __name__ == '__main__':
    app = QApplication([])
    window = StartMenu()
    window.show()
    app.exec_()
 

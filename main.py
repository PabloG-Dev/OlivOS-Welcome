import sys, os
from PySide6.QtWidgets import QApplication
from ui.welcome import MainPage

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    app = QApplication(sys.argv)
    win = MainPage()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

import sys
from PySide6.QtWidgets import QApplication
from ui.welcome import MainPage

def main():
    app = QApplication(sys.argv)
    win = MainPage()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
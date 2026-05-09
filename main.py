import sys, os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator, QLocale
from ui.welcome import MainPage

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    app = QApplication(sys.argv)

    # i18n SETUP
    translator = QTranslator()

    lang = QLocale.system().name()

    qm_path = f"i18n/{lang}.qm"

    if not translator.load(qm_path):
        print(f"[i18n] No se pudo cargar: {qm_path}")
    else:
        app.installTranslator(translator)
        print(f"[i18n] Cargado: {qm_path}")

    # UI
    win = MainPage()
    win.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
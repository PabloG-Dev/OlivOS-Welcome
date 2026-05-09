from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QTranslator
import subprocess
from utils.autostart_utils import Autostart
from pathlib import Path

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.autostart = Autostart()
        self.autostart.ensure_exists()
        self.setup_ui()
        self.auto_check.toggled.connect(self.on_autostart_changed)

    def setup_ui(self):
        self.resize(700, 475)
        self.setStyleSheet(self.global_style())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # HEADER
        header = QHBoxLayout()

        title_layout = QVBoxLayout()
        self.title = QLabel(self.tr("¡Bienvenido a OlivOS!"))
        self.subtitle = QLabel(self.tr("Tu sistema operativo amigable y ágil."))

        self.title.setObjectName("title")
        self.subtitle.setObjectName("subtitle")

        title_layout.addWidget(self.title)
        title_layout.addWidget(self.subtitle)

        header.addLayout(title_layout)
        header.addStretch()

        # Botón instalar
        if self.is_live_system():
            self.install_btn = QPushButton("Instalar OlivOS")
            self.install_btn.setObjectName("installButton")
            self.install_btn.setFixedSize(120, 50)
            header.addWidget(self.install_btn)

        main_layout.addLayout(header)
        main_layout.addStretch()

        # CONTENIDO CENTRAL
        content = QHBoxLayout()
        content.setSpacing(30)

        # COLUMNA IZQUIERDA
        left_col = QVBoxLayout()
        left_col.setSpacing(10)

        left_col.addWidget(self.create_card(self.tr("Página Oficial"), "images/web.png", self.open_website))
        left_col.addWidget(self.create_card(self.tr("Tienda de Aplicaciones"), "images/store.png", self.open_store))
        left_col.addWidget(self.create_card(self.tr("Información del Sistema"), "images/info.png", self.open_system_info))
        #left_col.addWidget(self.create_card("CuerdOS Noticias", "images/news.png", self.open_news))

        content.addLayout(left_col)

        # CENTRO (MASCOTA)
        center_col = QVBoxLayout()
        center_col.setAlignment(Qt.AlignCenter)

        mascot = QLabel()
        pix = QPixmap("images/olivos-logo.png")

        mascot.setPixmap(
            pix.scaled(170, 170, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        mascot.setAlignment(Qt.AlignCenter)

        center_col.addWidget(mascot)
        content.addLayout(center_col)

        # COLUMNA DERECHA
        right_col = QVBoxLayout()
        right_col.setSpacing(10)

        right_col.addWidget(self.create_card(self.tr("Actualizar Sistema"), "images/update.png", self.open_updater))
        right_col.addWidget(self.create_card(self.tr("Gestor de Recuperación"), "images/recovery.png", self.open_recovery))
        right_col.addWidget(self.create_card(self.tr("Wiki Oficial"), "images/wiki.png", self.open_wiki))
        # right_col.addWidget(self.create_card("Ver Novedades", "images/refresh.png", self.open_whats_new))

        content.addLayout(right_col)

        main_layout.addLayout(content)
        main_layout.addStretch()

        # FOOTER INFO
        self.footer_text = QLabel(self.tr("OlivOS está diseñado para ser rápido y eficiente."))
        self.footer_text.setAlignment(Qt.AlignCenter)
        self.footer_text.setObjectName("footer")

        main_layout.addWidget(self.footer_text)

        # BOTTOM BAR
        bottom = QHBoxLayout()

        self.auto_check = QCheckBox(self.tr("Iniciar automáticamente al acceder al escritorio"))
        self.auto_check.setChecked(self.autostart.is_enabled())
        bottom.addWidget(self.auto_check)

        bottom.addStretch()

        # Iconos pequeños
        bottom.addWidget(self.icon_label("images/terminal.png"))
        bottom.addWidget(self.icon_label("images/butterfly.png"))
        bottom.addWidget(self.icon_label("images/telegram.png"))

        # Botón cerrar
        self.close_btn = QPushButton(self.tr("Cerrar"))
        self.close_btn.setObjectName("closeButton")

        self.close_btn.clicked.connect(self.close)

        bottom.addWidget(self.close_btn)

        main_layout.addLayout(bottom)

    def is_live_system(self):
        return not Path("/etc/olivos-release").exists()

    def on_autostart_changed(self, enabled: bool):
        self.autostart.set_enabled(enabled)

    def create_card(self, text, icon_path, callback):
        btn = QPushButton(text)
        btn.setIcon(QIcon(icon_path))
        btn.setMinimumHeight(70)
        btn.setObjectName("cardButton")
        btn.setCursor(Qt.PointingHandCursor)

        btn.clicked.connect(callback)

        return btn

    # CALLBACKS
    def open_website(self):
        import webbrowser
        webbrowser.open("https://olivoslinux.com")

    def open_store(self):
        subprocess.Popen(["octoxbps"])

    def open_system_info(self):
        subprocess.Popen(["alacritty -e bash -c 'fastfetch; exec bash'"])

    def open_news(self):
        webbrowser.open("https://olivoslinux.com")

    def open_updater(self):
        subprocess.Popen(["alacritty -e bash -c 'xbps-install -Syu; exec bash'"])

    def open_recovery(self):
        subprocess.Popen(["timeshift-launcher"])

    def open_wiki(self):
        webbrowser.open("https://olivoslinux.com")

    def open_whats_new(self):
        subprocess.Popen(["https://olivoslinux.com"])

    def icon_label(self, path):
        lbl = QLabel()
        pix = QPixmap(path)
        lbl.setPixmap(pix.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        return lbl

    # ESTILOS
    def global_style(self):
        return """
        QWidget {
            background-color: #1f2421;
            color: #e6f1ea;
            font-family: "Noto Sans", sans-serif;
        }

        /* TITULOS */
        QLabel#title {
            font-size: 28px;
            font-weight: 600;
            color: #dff5e4;
        }

        QLabel#subtitle {
            font-size: 14px;
            color: #9fb7a7;
        }

        QLabel#footer {
            font-size: 13px;
            color: #7f9688;
        }

        /* BOTÓN INSTALAR */
        QPushButton#installButton {
            background-color: #6fa67a;
            border-radius: 8px;
            font-weight: 600;
            color: #ffffff;
            border: 1px solid #6fa67a;    
        }

        QPushButton#installButton:hover {
            background-color: #323b36;
            border: 1px solid #6fa67a;
        }

        /* TARJETAS */
        QPushButton#cardButton {
            background-color: #2a312d;
            border-radius: 10px;
            text-align: left;
            padding: 10px 14px;
            border: 1px solid transparent;
            color: #d7efe0;
        }

        QPushButton#cardButton:hover {
            background-color: #323b36;
            border: 1px solid #6fa67a;
        }

        QPushButton#cardButton:pressed {
            background-color: #26302a;
        }

        /* BOTÓN CERRAR */
        QPushButton#closeButton {
            background-color: #2c332f;
            padding: 6px 16px;
            border-radius: 8px;
            color: #d7efe0;
            border: 1px solid transparent;
        }

        QPushButton#closeButton:hover {
            background-color: #3e5f4a;
            border: 1px solid #7bcf93;
        }

        QPushButton#closeButton:pressed {
            background-color: #2b4a38;
        }

        /* CHECKBOX */
        QCheckBox {
            spacing: 6px;
            color: #b7d6c2;
        }

        QCheckBox::indicator {
            width: 14px;
            height: 14px;
            border-radius: 4px;
            border: 1px solid #6fa67a;
            background-color: #2a312d;
        }

        QCheckBox::indicator:checked {
            background-color: #6fa67a;
            border: 1px solid #6fa67a;
        }

        /* SCROLLBAR (por si luego añades) */
        QScrollBar:vertical {
            background: #1f2421;
            width: 10px;
        }

        QScrollBar::handle:vertical {
            background: #3a4a42;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical:hover {
            background: #4f6b5c;
        }
        """

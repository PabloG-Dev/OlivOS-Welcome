from pathlib import Path

AUTOSTART_PATH = Path.home() / ".config" / "autostart"
DESKTOP_FILE = AUTOSTART_PATH / "olivos-welcome.desktop"


class Autostart:
    def __init__(self):
        AUTOSTART_PATH.mkdir(parents=True, exist_ok=True)

    # ------------------------
    # PUBLIC API
    # ------------------------

    def ensure_exists(self):
        if not DESKTOP_FILE.exists():
            self._create_default()

    def is_enabled(self) -> bool:
        """
        Devuelve True si autostart está activado.
        """
        if not DESKTOP_FILE.exists():
            return False

        lines = DESKTOP_FILE.read_text().splitlines()

        for line in lines:
            line = line.strip()

            if line.startswith("Hidden="):
                value = line.split("=", 1)[1].lower()
                return value == "false"

        # Si no existe Hidden, asumimos activado
        return True

    def set_enabled(self, enabled: bool):
        """
        Activa o desactiva el autostart modificando Hidden=
        """
        self.ensure_exists()

        lines = DESKTOP_FILE.read_text().splitlines()
        new_lines = []

        hidden_written = False

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("Hidden="):
                # Reemplazamos SIEMPRE
                new_lines.append(f"Hidden={'false' if enabled else 'true'}")
                hidden_written = True
            else:
                new_lines.append(line)

        # Si no existía, lo añadimos
        if not hidden_written:
            new_lines.append(f"Hidden={'false' if enabled else 'true'}")

        # Escribimos limpio (sin duplicados)
        DESKTOP_FILE.write_text("\n".join(new_lines) + "\n")

    # ------------------------
    # INTERNAL
    # ------------------------

    def _create_default(self):
        DESKTOP_FILE.write_text(
            "[Desktop Entry]\n"
            "Type=Application\n"
            "Name=OlivOS Welcome\n"
            "Exec=olivos-welcome\n"
            "Hidden=false\n"
        )
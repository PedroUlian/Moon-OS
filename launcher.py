import subprocess
import sys
import os
import time

PYTHON = sys.executable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MOON = os.path.join(BASE_DIR, "moon.py")
LUNA = os.path.join(BASE_DIR, "luna.py")

def main():
    # abre o Moon OS (terminal real)
    moon_proc = subprocess.Popen(
        [PYTHON, MOON],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    time.sleep(0.5)

    # abre a LUNA (HUD)
    luna_proc = subprocess.Popen([PYTHON, LUNA])

    # 🔒 espera o Moon fechar
    moon_proc.wait()

    # ☠️ quando o Moon fechar, mata a LUNA
    luna_proc.terminate()

if __name__ == "__main__":
    main()

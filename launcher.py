import subprocess
import sys
import os
import time

PYTHON = sys.executable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MOON = os.path.join(BASE_DIR, "moon.py")
LUNA = os.path.join(BASE_DIR, "luna.py")

WINDOWS = os.name == "nt"

def main():
    # abre o Moon OS
    if WINDOWS:
        moon_proc = subprocess.Popen(
            [PYTHON, MOON],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        moon_proc = subprocess.Popen(
            [PYTHON, MOON]
        )

    time.sleep(0.5)

    # abre a LUNA (HUD)
    luna_proc = subprocess.Popen([PYTHON, LUNA])

    # espera o Moon fechar
    moon_proc.wait()

    # mata a LUNA quando Moon fechar
    luna_proc.terminate()

if __name__ == "__main__":
    main()

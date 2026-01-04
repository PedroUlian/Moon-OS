import msvcrt
import time
import sys
import os
import json
import subprocess

os.system('cls')

FS_ROOT = "moon_fs"
STATE_FILE = "state.json"
TEXT_EXTENSIONS = [".txt", ".log", ".md"]
CODE_EXTENSIONS = [".py", ".exe", ".bin"]

#############
# Functions #
#############

def read_text_file(real_path, name):
    type_out(f"--- READING {name} ---", delay=0.01)

    with open(real_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            type_out(line.rstrip(), delay=0.015)

    type_out("--- END OF FILE ---", delay=0.01)

def read_json_file(real_path, name):
    type_out(f"--- INSPECTING {name} ---", delay=0.01)

    try:
        with open(real_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        type_out("ERROR: corrupted or unreadable JSON")
        return

    def print_json(obj, indent=0):
        prefix = "  " * indent

        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    type_out(f"{prefix}{k}:")
                    print_json(v, indent + 1)
                else:
                    type_out(f"{prefix}{k}: {v}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                type_out(f"{prefix}- [{i}]")
                print_json(v, indent + 1)

    print_json(data)
    type_out("--- END OF DATA ---", delay=0.01)

def open_file(real_path, name):
    _, ext = os.path.splitext(real_path)
    type_out(f"Opening {name}...", delay=0.02)

    try:
        # SE FOR PY → executa via Python do venv em novo terminal
        if ext == ".py":
            venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
            if not os.path.exists(venv_python):
                type_out("ERROR: Python venv not found!")
                return

            # abre em nova janela de terminal
            subprocess.Popen(
                ["cmd", "/c", "start", "python", real_path],
                shell=True
            )
            type_out("Python script started in new terminal.")

        # WINDOWS outros arquivos
        elif os.name == "nt":
            os.startfile(real_path)
            type_out("Process started successfully.")

        # LINUX / MAC
        else:
            opener = "xdg-open"
            subprocess.Popen([opener, real_path])
            type_out("Process started successfully.")

    except Exception as e:
        type_out(f"ERROR: failed to open file ({e})")


def cmd_read(state, args):
    if not args:
        type_out("read: missing file operand")
        return

    path = resolve_path(state["cwd"], args[0])
    real = get_real_path(path)

    if not os.path.exists(real):
        type_out("read: file not found")
        return

    if os.path.isdir(real):
        type_out("read: cannot read a directory")
        return

    _, ext = os.path.splitext(real)

    # TXT / LOG / MD → leitura normal
    if ext in TEXT_EXTENSIONS:
        read_text_file(real, args[0])
        return

    # JSON → leitura estruturada
    if ext == ".json":
        read_json_file(real, args[0])
        return

    # PY / BIN / ETC → não pode ler
    if ext in CODE_EXTENSIONS:
        open_file(real, args[0])
        return

    # fallback
    type_out("read: unsupported file format")


def get_real_path(virtual_path):
    virtual_path = virtual_path.lstrip("/")
    return os.path.join(FS_ROOT, virtual_path)

def resolve_path(cwd, path):
    if path.startswith("/"):
        full = path
    else:
        full = os.path.join(cwd, path)

    normalized = os.path.normpath(full).replace("\\", "/")

    if not normalized.startswith("/"):
        normalized = "/" + normalized

    return normalized

def cmd_ls(state, args):
    cwd = state["cwd"]
    path = cwd if not args else resolve_path(cwd, args[0])

    real = get_real_path(path)

    if not os.path.exists(real):
        type_out("ls: no such directory")
        return

    if not os.path.isdir(real):
        type_out("ls: not a directory")
        return

    for item in os.listdir(real):
        type_out(item, delay=0)

def cmd_cd(state, args):
    if not args:
        state["cwd"] = "/"
        save_state(state)
        return

    target = resolve_path(state["cwd"], args[0])
    real = get_real_path(target)

    if not os.path.exists(real):
        type_out("cd: no such directory")
        return

    if not os.path.isdir(real):
        type_out("cd: not a directory")
        return

    state["cwd"] = target
    save_state(state)

def cmd_cat(state, args):
    if not args:
        type_out("cat: missing file operand")
        return

    path = resolve_path(state["cwd"], args[0])
    real = get_real_path(path)

    if not os.path.exists(real):
        type_out("cat: file not found")
        return

    if os.path.isdir(real):
        type_out("cat: is a directory")
        return

    with open(real, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            type_out(line.rstrip(), delay=0)




def load_state():
    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def type_out(text, delay=0.02):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def read_command(prompt="> "):
    print(prompt, end="", flush=True)
    cmd = ""

    while True:
        key = msvcrt.getch()

        if key == b'\r':  # ENTER
            print()
            return cmd

        elif key == b'\x08':  # BACKSPACE
            if len(cmd) > 0:
                cmd = cmd[:-1]
                print("\b \b", end="", flush=True)

        elif key >= b' ':
            char = key.decode(errors="ignore")
            cmd += char
            print(char, end="", flush=True)

def read_password(prompt="Password: "):
    print(prompt, end="", flush=True)
    passwd = ""

    while True:
        key = msvcrt.getch()

        if key == b'\r':  # ENTER
            print()
            return passwd

        elif key == b'\x08':  # BACKSPACE
            if len(passwd) > 0:
                passwd = passwd[:-1]
                print("\b \b", end="", flush=True)

        elif key >= b' ':
            char = key.decode(errors="ignore")
            passwd += char
            print("*", end="", flush=True)  # mostra '*' no lugar do caractere real

state = load_state()

#########
# Tasks #
#########

def task1():
    state = load_state()
    type_out(f"Hello {state["username"]}, I am LUN4")
    type_out(f"An Artificial Intelligence programmed to help you complete your tasks!")
    time.sleep(0.5)
    type_out("Would you like to know your next task? (Y/N) ")
    print("\033[1A\033[2K", end="")
    taskquestion = read_command("Would you like to know your next task? (Y/N) ")
    if taskquestion == "Y" or taskquestion == "y":
        state["ctask"] = "energize the spacecraft"
        save_state(state)
        os.system('cls')
        time.sleep(0.5)
        type_out("Very Well!")
        time.sleep(0.5)
        type_out("Your first task is to turn on the power to the spaceship.")
        time.sleep(5)
        os.system('cls')
        type_out("let's go!")
        time.sleep(3)
        os.system('cls')
    elif taskquestion == "N" or taskquestion == "n":
        time.sleep(0.5)
        type_out("Ok, See you next time!")
        time.sleep(0.5)
    else:
        time.sleep(0.5)
        type_out("INVALID COMMAND")
        time.sleep(0.5)

#############
# Main Code #
#############

def main():
    state = load_state()

    ################################
    # Login And Register Functions #
    ################################

    def register():
        print("\033[1A\033[2K", end="")
        type_out("*REGISTER*")
        type_out("Username: ")
        print("\033[1A\033[2K", end="")
        state["username"] = read_command("Username: ")
        type_out("Password: ")
        print("\033[1A\033[2K", end="")
        state["passwd"] = read_password("Password: ")
        state["acess"] = "Basic"
        state["ctask"] = "none"
        state["completed-tasks"] = 0
        state["LunaOnline"] = False
        state["cwd"] = "/"
        save_state(state)
        time.sleep(0.5)

    def login():
        print("\033[1A\033[2K", end="")
        type_out("*LOGIN*")
        type_out("Username: "f"{state["username"]}")
        type_out("Password: ")
        print("\033[1A\033[2K", end="")
        passwd = read_password("Password: ")
        if passwd != state["passwd"]:
            os.system("cls")
            type_out("Authenticating user", 0.03)
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(0.4)
            print("\033[2K\r", end="")
            type_out("ACCESS DENIED!")
            time.sleep(1)
            os.system("cls")
            login()

    #######################
    # Fake Boot and Login #
    #######################
        
    type_out("Booting system...")
    time.sleep(0.5)

    state = load_state()
    if "username" not in state or "passwd" not in state:
        register()
    else:
        login()

    os.system('cls')
    type_out("Authenticating user", 0.03)
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.4)
    print("\033[2K\r", end="")
    type_out("Access granted.")
    time.sleep(1)
    state["LunaOnline"] = True
    save_state(state)
    os.system('cls')
    type_out("Moon OS v0.9")
    type_out(f"{state["username"]}@station:~$ ")
    print("\033[1A\033[2K", end="")

    #############
    # Commands! #
    #############

    while True:
        cmd = read_command(f"{state['username']}@station:{state['cwd']}$ ")
        parts = cmd.split()
        command = parts[0]
        args = parts[1:]

        if command == "help":
            type_out("Comandos disponíveis:")
            type_out("  tasks")
            type_out("  status")
            type_out("  ls")
            type_out("  cd")
            type_out("  cat")
            type_out("  read")
            type_out("  unlock")
            type_out("  repair")
            type_out("  chmod")
            type_out("  clear")
            type_out("  exit")

        elif command == "status":
            state = load_state()
            type_out(f"User: {state["username"]}")
            type_out("status: online")
            type_out(f"Access: {state["acess"]}")
            type_out(f"Current Task: {state["ctask"]}")

        elif command == "tasks":
            if state["completed-tasks"] == 0:
                task1()

            
        elif command == "ls":
            cmd_ls(state, args)

        elif command == "cd":
            cmd_cd(state, args)

        elif command == "cat":
           cmd_cat(state, args)

        elif command == "read":
            cmd_read(state, args)

        elif command == "unlock":
            type_out("")

        elif command == "repair":
            type_out("")

        elif command == "chmod":
            type_out("")

        elif command == "clear":
            print("\033[2J\033[H", end="")

        elif command == "exit":
            # Só atualiza LunaOnline, sem sobrescrever ctask
            current_state = load_state()       # pega o state mais recente do disco
            current_state["LunaOnline"] = False
            save_state(current_state)
            break


        else:
            type_out(f"Comando não reconhecido: {command}")

main()

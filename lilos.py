import msvcrt
import time
import sys
import os
import json

os.system('cls')

STATE_FILE = "state.json"

def task1():
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

def main():
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
    os.system('cls')
    type_out("Moon OS v0.9")
    type_out(f"{state["username"]}@station:~$ ")
    print("\033[1A\033[2K", end="")
    

    while True:
        cmd = read_command(f"{state["username"]}@station:~$ ")

        if cmd == "help":
            type_out("Comandos disponíveis:")
            type_out("  tasks")
            type_out("  status")
            type_out("  clear")
            type_out("  exit")

        elif cmd == "status":
            state = load_state()
            type_out(f"User: {state["username"]}")
            type_out("status: online")
            type_out(f"Access: {state["acess"]}")
            type_out(f"Current Task: {state["ctask"]}")

        elif cmd == "tasks":
            state = load_state()
            if state["completed-tasks"] == 0:
                task1()

            
        elif cmd == "Energize the spaceship":
            type_out("c3")

        elif cmd == "clear":
            print("\033[2J\033[H", end="")

        elif cmd == "exit":
            break

        else:
            type_out(f"Comando não reconhecido: {cmd}")

main()

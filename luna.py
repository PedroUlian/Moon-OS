import tkinter as tk
import json
import os

WINDOWS = os.name == "nt"

STATE_FILE = "state.json"
UPDATE_INTERVAL = 1000  # ms


class LunaWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.last_state = None  # cache seguro

        self.overrideredirect(True)
        self.attributes("-topmost", True)

        if WINDOWS:
        # Windows: transparência por cor
            self.configure(bg="#0C0C0C")
            self.attributes("-transparentcolor", "#0C0C0C")
        else:
        # Linux: transparência por alpha
            self.configure(bg="#111722")  # fundo visível
            self.attributes("-alpha", 0.95)  # leve transparência



        width = 320
        height = 420

        screen_w = self.winfo_screenwidth()
        x = screen_w - width - 10
        y = 10

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.configure(bg="#0C0C0C")

        self.build_ui()
        self.after(500, self.update_state)

    def build_ui(self):
        font_title = ("Consolas", 16, "bold")
        font_label = ("Consolas", 11)
        font_task = ("Consolas", 12, "bold")

        self.lbl_title = tk.Label(
            self, text="LUNA AI", fg="#7df9ff", bg="#0C0C0C", font=font_title
        )
        self.lbl_title.pack(pady=10)

        self.lbl_status = tk.Label(
            self, text="WAITING FOR SYSTEM", fg="#ffaa00",
            bg="#0C0C0C", font=font_label
        )
        self.lbl_status.pack(pady=5)

        self.lbl_user = tk.Label(self, fg="white", bg="#0C0C0C", font=font_label)
        self.lbl_user.pack(pady=5)

        self.lbl_access = tk.Label(self, fg="white", bg="#0C0C0C", font=font_label)
        self.lbl_access.pack(pady=5)

        tk.Label(
            self, text="CURRENT TASK", fg="#7df9ff", bg="#0C0C0C", font=font_label
        ).pack(pady=(20, 5))

        self.lbl_task = tk.Label(
            self, fg="white", bg="#111722",
            font=font_task, wraplength=280, justify="center"
        )
        self.lbl_task.pack(padx=10, pady=5, fill="x")

        tk.Label(
            self, text="LUNA HINT", fg="#7df9ff", bg="#0C0C0C", font=font_label
        ).pack(pady=(20, 5))

        self.lbl_hint = tk.Label(
            self, fg="#bbbbbb", bg="#111722",
            wraplength=280, justify="center", font=font_label
        )
        self.lbl_hint.pack(padx=10, pady=5, fill="x")

        self.bind("<Escape>", lambda e: self.destroy())

    def update_state(self):
        if not os.path.exists(STATE_FILE):
            self.set_offline()
            self.after(UPDATE_INTERVAL, self.update_state)
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)

        # só aceita estado COMPLETO
            if "ctask" in state and "username" in state:
                self.last_valid_state = state
                self.apply_state(state)
            elif self.last_valid_state:
                self.apply_state(self.last_valid_state)

        except Exception:
            if self.last_valid_state:
                self.apply_state(self.last_valid_state)
            else:
                self.set_error()

        self.after(UPDATE_INTERVAL, self.update_state)


    def apply_state(self, state):
        if not state.get("LunaOnline", False):
            self.show_waiting()
            return

        self.lbl_status.config(text="SYSTEM ONLINE", fg="#50fa7b")
        self.lbl_user.config(text=f"USER: {state.get('username', 'UNKNOWN')}")
        self.lbl_access.config(text=f"ACCESS: {state.get('acess', 'N/A')}")

        task = state.get("ctask", "NO TASK")
        self.lbl_task.config(text=task)
        self.lbl_hint.config(text=self.get_task_hint(task))

    def get_task_hint(self, task):
        hints = {
            "energize the spacecraft": "Check the power system directory.",
            "none": "Awaiting new instructions.",
        }
        return hints.get(task, "No data available.")

    def show_waiting(self):
        self.lbl_status.config(text="WAITING FOR SYSTEM", fg="#ffaa00")
        self.lbl_user.config(text="")
        self.lbl_access.config(text="")
        self.lbl_task.config(text="—")
        self.lbl_hint.config(text="Launch Moon OS terminal.")

    def show_error(self):
        self.lbl_status.config(text="STATE ERROR", fg="#ff5555")
        self.lbl_hint.config(text="Failed to read state file.")


if __name__ == "__main__":
    LunaWindow().mainloop()

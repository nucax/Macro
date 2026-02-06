import keyboard
import time
import pyautogui
import threading
from tkinter import Tk, Label, Button, filedialog

class MacroRecorder:
    def __init__(self):
        self.events = []
        self.recording = False
        self.last_time = None
        self.hook = None

        keyboard.add_hotkey("f6", self.play_macro)
        print("F6 = Replay Macro (global)")

    def start_recording(self):
        if self.recording:
            return
        self.events.clear()
        self.recording = True
        self.last_time = time.time()
        self.hook = keyboard.hook(self.record_key_event)
        print("Recording started (F12 to stop)")

    def stop_recording(self):
        if not self.recording:
            return
        self.recording = False
        keyboard.unhook(self.hook)
        print("Recording stopped")
        self.save_macro()

    def record_key_event(self, event):
        if not self.recording or event.event_type != keyboard.KEY_DOWN:
            return

        now = time.time()
        delay = now - self.last_time
        self.last_time = now

        if event.name == "f12":
            self.stop_recording()
            return

        self.events.append((event.name, delay))
        print(f"{event.name} ({delay:.3f}s)")

    def play_macro(self):
        data = self.load_macro()
        if not data:
            return

        print("Replaying macro...")
        time.sleep(0.5)

        for key, delay in data:
            time.sleep(delay)
            keyboard.press_and_release(key)

    def save_macro(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Macro Files", "*.txt")]
        )
        if not path:
            return

        with open(path, "w") as f:
            for key, delay in self.events:
                f.write(f"{key},{delay}\n")

        print("Saved:", path)

    def load_macro(self):
        path = filedialog.askopenfilename(
            filetypes=[("Macro Files", "*.txt")]
        )
        if not path:
            return None

        data = []
        with open(path, "r") as f:
            for line in f:
                key, delay = line.strip().split(",")
                data.append((key, float(delay)))
        return data


class App:
    def __init__(self, master):
        master.title("Macro Recorder")

        self.recorder = MacroRecorder()

        Label(master, text="Macro Recorder").pack(pady=5)

        Button(master, text="Start Recording", command=self.start).pack()
        Button(master, text="Play Macro", command=self.play).pack()

    def start(self):
        threading.Thread(target=self.recorder.start_recording, daemon=True).start()

    def play(self):
        threading.Thread(target=self.recorder.play_macro, daemon=True).start()


if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    root.deiconify()
    App(root)
    root.mainloop()

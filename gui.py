import tkinter as tk
import os
import subprocess
class App:
    def __init__(self, master):
        self.master = master
        master.title("NitroType Bot")
        master.geometry("250x250")
        # Create username label and entry field
        self.username_label = tk.Label(master, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack(pady=5)

        # Create password label and entry field
        self.password_label = tk.Label(master, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=5)

        # Create background checkbox
        self.background_var = tk.BooleanVar()
        self.background_checkbox = tk.Checkbutton(master, text="Hide Browser", variable=self.background_var)
        self.background_checkbox.pack(pady=5)

        # Create slider
        self.slider_label = tk.Label(master, text="Typing Speed:")
        self.slider_label.pack()
        self.slider = tk.Scale(master, from_=1, to=10, orient=tk.HORIZONTAL)
        self.slider.pack()

        # Create run button
        self.run_button = tk.Button(master, text="Run", command=self.run_script)
        self.run_button.pack(pady=10)

        # Load settings from file
        self.load_settings()

    def run_script(self):
        # Save settings to file
        self.save_settings()

        # Launch script in its own process
        username = self.username_entry.get()
        password = self.password_entry.get()
        background = self.background_var.get()
        slider_value = self.slider.get()
        script_path = "main.py"
        subprocess.Popen(["venv/Scripts/python", "main.py", username, password, str(background), str(slider_value)])
    

    def load_settings(self):
        # Load settings from file
        try:
            with open("settings.txt", "r") as f:
                settings = f.read().splitlines()
                self.username_entry.insert(0, settings[0])
                self.password_entry.insert(0, settings[1])
                self.background_var.set(bool(settings[2]))
                self.slider.set(int(settings[3]))
        except:
            pass

    def save_settings(self):
        # Save settings to file
        with open("settings.txt", "w") as f:
            f.write(f"{self.username_entry.get()}\n")
            f.write(f"{self.password_entry.get()}\n")
            f.write(f"{int(self.background_var.get())}\n")
            f.write(f"{self.slider.get()}\n")

root = tk.Tk()
app = App(root)
root.mainloop()
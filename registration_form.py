import tkinter as tk
from tkinter import messagebox
import sqlite3
from styles import style

class RegistrationForm(tk.Toplevel):
    def __init__(self, master=None, db=None, on_success=None, on_back=None):
        super().__init__(master)
        self.title("Register")
        self.geometry("400x300")
        self.db = db
        self.on_success = on_success
        self.on_back = on_back
        self.configure(bg=style["TFrame"]["background"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = tk.Frame(self, **style["MainFrame"])
        main_frame.grid(sticky="nsew")
        
        self.title_label = tk.Label(main_frame, text="Create an Account", **style["TitleLabel"])
        self.title_label.pack(pady=(0, 20))

        self.username_label = tk.Label(main_frame, text="Username", **style["TLabel"])
        self.username_label.pack()
        self.username_entry = tk.Entry(main_frame, **style["TEntry"])
        self.username_entry.pack(pady=(0, 10))

        self.password_label = tk.Label(main_frame, text="Password", **style["TLabel"])
        self.password_label.pack()
        self.password_entry = tk.Entry(main_frame, show="*", **style["TEntry"])
        self.password_entry.pack(pady=(0, 20))

        self.register_button = tk.Button(main_frame, text="Register", command=self.register, **style["TButton"])
        self.register_button.pack(pady=10)

        self.back_button = tk.Button(main_frame, text="Back", command=self.back, **style["TButton"])
        self.back_button.pack(pady=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return

        try:
            self.db.add_user(username, password)
            user = self.db.get_user(username, password)
            if user is not None:
                user_id = user[0]
                messagebox.showinfo("Success", "Registration successful!")
                if self.on_success:
                    self.on_success(user_id, username)
                self.destroy()
            else:
                messagebox.showerror("Error", "User registration failed.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    def back(self):
        if self.on_back:
            self.on_back()
        self.destroy()

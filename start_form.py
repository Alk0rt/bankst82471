import tkinter as tk
from registration_form import RegistrationForm
from login_form import LoginForm
from database import Database
from styles import style

# Создаем экземпляр базы данных
db = Database()

class StartForm(tk.Tk):
    def __init__(self, main_app_class):
        super().__init__()
        self.title("Welcome")
        self.geometry("400x300")
        self.main_app_class = main_app_class
        self.configure(bg=style["TFrame"]["background"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = tk.Frame(self, **style["MainFrame"])
        main_frame.grid(sticky="nsew")

        self.title_label = tk.Label(main_frame, text="Welcome to the Banking App", **style["TitleLabel"])
        self.title_label.pack(pady=(0, 20))

        self.register_button = tk.Button(main_frame, text="Create Account", command=self.open_registration, **style["TButton"])
        self.register_button.pack(pady=10)

        self.login_button = tk.Button(main_frame, text="Login", command=self.open_login, **style["TButton"])
        self.login_button.pack(pady=10)

    def open_registration(self):
        registration_form = RegistrationForm(self, db=db, on_success=self.open_main_app, on_back=self.deiconify)
        self.withdraw()

    def open_login(self):
        login_form = LoginForm(self, db=db, on_success=self.open_main_app, on_back=self.deiconify)
        self.withdraw()

    def open_main_app(self, user_id, username):
        self.withdraw()
        main_app = self.main_app_class(user_id, username)
        main_app.mainloop()

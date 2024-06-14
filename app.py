import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from start_form import StartForm
from customer_form import CustomerForm
from user_management_form import UserManagementForm
from deposit_form import DepositForm
from transfer_form import TransferForm
from database import Database
from styles import style
import os

db = Database()

class MainApp(tk.Tk):
    def __init__(self, user_id, username):
        super().__init__()
        self.title("Banking Application")
        self.geometry("500x700")  # Увеличенный размер окна
        self.user_id = user_id
        self.username = username
        self.configure(bg=style["TFrame"]["background"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Проверка наличия фонового изображения и его загрузка
        try:
            if os.path.exists("background.jpg"):
                self.background_image = Image.open("background.jpg")
                self.background_photo = ImageTk.PhotoImage(self.background_image)
                self.background_label = tk.Label(self, image=self.background_photo)
                self.background_label.place(relwidth=1, relheight=1)
            else:
                self.configure(bg="#e0e0e0")  # Альтернативный фон
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.configure(bg="#e0e0e0")  # Альтернативный фон

        main_frame = tk.Frame(self, bg="#ffffff")
        main_frame.grid(sticky="nsew", padx=20, pady=20)

        self.label = tk.Label(main_frame, text=f"Hello, {username}!", **style["TitleLabel"])
        self.label.pack(pady=20)

        transaction_frame = tk.Frame(main_frame, bg=style["MainFrame"]["background"])
        transaction_frame.pack(pady=10, fill="both", expand=True)

        self.balance_button = tk.Button(transaction_frame, text="View Balance", command=self.view_balance, **style["TButton"])
        self.balance_button.pack(pady=5, fill="x")

        self.transactions_button = tk.Button(transaction_frame, text="View Transactions", command=self.view_transactions, **style["TButton"])
        self.transactions_button.pack(pady=5, fill="x")

        self.deposit_button = tk.Button(transaction_frame, text="Deposit Funds", command=self.open_deposit_form, **style["TButton"])
        self.deposit_button.pack(pady=5, fill="x")

        self.transfer_button = tk.Button(transaction_frame, text="Transfer Funds", command=self.open_transfer_form, **style["TButton"])
        self.transfer_button.pack(pady=5, fill="x")

        admin_frame = tk.Frame(main_frame, bg=style["MainFrame"]["background"])
        admin_frame.pack(pady=10, fill="both", expand=True)

        self.customer_button = tk.Button(admin_frame, text="Manage Customers", command=self.open_customer_form, **style["TButton"])
        self.customer_button.pack(pady=5, fill="x")

        self.user_management_button = tk.Button(admin_frame, text="Manage Account", command=self.open_user_management_form, **style["TButton"])
        self.user_management_button.pack(pady=5, fill="x")

        self.logout_button = tk.Button(admin_frame, text="Log Out", command=self.logout, **style["TButton"])
        self.logout_button.pack(pady=5, fill="x")

        self.save_button = tk.Button(admin_frame, text="Save Users to File", command=self.save_users_to_file, **style["TButton"])
        self.save_button.pack(pady=5, fill="x")

    def view_balance(self):
        balance = db.get_balance(self.user_id)
        messagebox.showinfo("Balance", f"Your balance is: {balance}")
        db.check_accounts()  # Проверка записей в таблице Accounts

    def view_transactions(self):
        transactions = db.get_transactions(self.user_id)
        transactions_str = "\n".join([f"ID: {t[0]}, Amount: {t[2]}, Type: {t[3]}, Date: {t[4]}" for t in transactions])
        messagebox.showinfo("Transactions", f"Your transactions:\n{transactions_str}")

    def open_deposit_form(self):
        deposit_form = DepositForm(self, user_id=self.user_id, db=db)

    def open_transfer_form(self):
        transfer_form = TransferForm(self, from_user_id=self.user_id, db=db)

    def open_customer_form(self):
        customer_form = CustomerForm(self)

    def open_user_management_form(self):
        user_management_form = UserManagementForm(self, user_id=self.user_id, username=self.username)

    def logout(self):
        self.destroy()
        start_form = StartForm(MainApp)
        start_form.mainloop()

    def save_users_to_file(self):
        db.save_users_to_file("users.json")
        messagebox.showinfo("Save to File", "Users saved to file successfully!")

if __name__ == "__main__":
    start_form = StartForm(MainApp)
    start_form.mainloop()

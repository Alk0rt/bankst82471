import tkinter as tk
from tkinter import messagebox
from database import Database

class DepositForm(tk.Toplevel):
    def __init__(self, master=None, user_id=None, db=None):
        super().__init__(master)
        self.title("Deposit")
        self.geometry("300x200")
        self.user_id = user_id
        self.db = db

        self.amount_label = tk.Label(self, text="Amount")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()

        self.deposit_button = tk.Button(self, text="Deposit", command=self.deposit)
        self.deposit_button.pack()

    def deposit(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("The amount must be positive.")
            print(f"DepositForm: deposit amount = {amount}")
            self.db.deposit(self.user_id, amount)
            messagebox.showinfo("Deposit", "Deposit successful!")
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

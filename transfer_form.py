import tkinter as tk
from tkinter import messagebox
from database import Database

class TransferForm(tk.Toplevel):
    def __init__(self, master=None, from_user_id=None, db=None):
        super().__init__(master)
        self.title("Transfer Funds")
        self.geometry("300x200")
        self.from_user_id = from_user_id
        self.db = db

        self.to_user_id_label = tk.Label(self, text="Recipient User ID")
        self.to_user_id_label.pack()
        self.to_user_id_entry = tk.Entry(self)
        self.to_user_id_entry.pack()

        self.amount_label = tk.Label(self, text="Amount")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()

        self.transfer_button = tk.Button(self, text="Transfer", command=self.transfer)
        self.transfer_button.pack()

    def transfer(self):
        try:
            to_user_id = int(self.to_user_id_entry.get())
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("The amount must be positive.")
            from_balance = self.db.get_balance(self.from_user_id)
            if from_balance < amount:
                raise ValueError("Insufficient funds.")
            self.db.transfer_funds(self.from_user_id, to_user_id, amount)
            messagebox.showinfo("Transfer", "Transfer successful!")
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

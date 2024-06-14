import tkinter as tk
from tkinter import messagebox
from database import Database

class UserManagementForm(tk.Toplevel):
    def __init__(self, master=None, user_id=None, username=None):
        super().__init__(master)
        self.title("User Management")
        self.geometry("300x250")
        self.user_id = user_id

        self.db = Database()

        self.username_label = tk.Label(self, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        self.username_entry.insert(0, username)

        self.password_label = tk.Label(self, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.update_button = tk.Button(self, text="Update", command=self.update_user)
        self.update_button.pack()

        self.delete_button = tk.Button(self, text="Delete Account", command=self.delete_user)
        self.delete_button.pack()

    def update_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.db.update_user(self.user_id, username, password)
        messagebox.showinfo("Update", "User updated successfully!")
        self.destroy()

    def delete_user(self):
        self.db.delete_user(self.user_id)
        messagebox.showinfo("Delete", "User deleted successfully!")
        self.master.destroy()  # Закрываем основное окно, так как учетная запись удалена
        self.destroy()

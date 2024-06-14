import tkinter as tk
from database import Database

class CustomerForm(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Manage Customers")
        self.geometry("400x300")

        self.db = Database()

        self.first_name_label = tk.Label(self, text="First Name")
        self.first_name_label.pack()
        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.pack()

        self.last_name_label = tk.Label(self, text="Last Name")
        self.last_name_label.pack()
        self.last_name_entry = tk.Entry(self)
        self.last_name_entry.pack()

        self.address_label = tk.Label(self, text="Address")
        self.address_label.pack()
        self.address_entry = tk.Entry(self)
        self.address_entry.pack()

        self.add_button = tk.Button(self, text="Add Customer", command=self.add_customer)
        self.add_button.pack()

        self.customer_listbox = tk.Listbox(self)
        self.customer_listbox.pack(fill=tk.BOTH, expand=True)
        self.load_customers()

    def add_customer(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        address = self.address_entry.get()
        self.db.add_customer(first_name, last_name, address)
        self.load_customers()

    def load_customers(self):
        self.customer_listbox.delete(0, tk.END)
        customers = self.db.get_customers()
        for customer in customers:
            self.customer_listbox.insert(tk.END, f"{customer[1]} {customer[2]}")

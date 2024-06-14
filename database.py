import sqlite3
import json

class Database:
    def __init__(self, db_name="bank.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT UNIQUE,
                Password TEXT,
                Role TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customers (
                CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName TEXT,
                LastName TEXT,
                Address TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Accounts (
                AccountID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER,
                Balance REAL DEFAULT 0,
                FOREIGN KEY(UserID) REFERENCES Users(UserID)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER,
                Amount REAL,
                Type TEXT,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(UserID) REFERENCES Users(UserID)
            )
        ''')
        self.connection.commit()

    def add_user(self, username, password, role="User"):
        try:
            self.cursor.execute("INSERT INTO Users (Username, Password, Role) VALUES (?, ?, ?)", (username, password, role))
            self.connection.commit()
            user_id = self.cursor.lastrowid
            print(f"add_user: New user ID = {user_id}")  # Отладочное сообщение
            self.cursor.execute("INSERT INTO Accounts (UserID, Balance) VALUES (?, ?)", (user_id, 0))
            self.connection.commit()
            print(f"add_user: Added account for user ID {user_id}")
        except sqlite3.IntegrityError:
            print(f"add_user: username {username} already exists")
            raise

    def get_user(self, username, password):
        self.cursor.execute("SELECT * FROM Users WHERE Username=? AND Password=?", (username, password))
        return self.cursor.fetchone()

    def get_balance(self, user_id):
        self.cursor.execute("SELECT Balance FROM Accounts WHERE UserID=?", (user_id,))
        result = self.cursor.fetchone()
        if result is None:
            print(f"get_balance: no balance record found for user_id={user_id}")
            return 0  # Возвращаем нулевой баланс, если записи не найдены
        print(f"get_balance: user_id={user_id}, balance={result[0]}")
        return result[0]

    def update_balance(self, user_id, new_balance):
        print(f"update_balance: user_id={user_id}, new_balance={new_balance}")  # Отладочное сообщение
        self.cursor.execute("UPDATE Accounts SET Balance=? WHERE UserID=?", (new_balance, user_id))
        self.connection.commit()
        self.cursor.execute("SELECT Balance FROM Accounts WHERE UserID=?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            print(f"Balance after update: {result[0]}")  # Проверка, что баланс обновился в базе данных
        else:
            print(f"Balance update failed for user_id={user_id}")

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM Users WHERE UserID=?", (user_id,))
        self.cursor.execute("DELETE FROM Accounts WHERE UserID=?", (user_id,))
        self.connection.commit()

    def add_customer(self, first_name, last_name, address):
        self.cursor.execute("INSERT INTO Customers (FirstName, LastName, Address) VALUES (?, ?, ?)", (first_name, last_name, address))
        self.connection.commit()

    def get_customers(self):
        self.cursor.execute("SELECT * FROM Customers")
        return self.cursor.fetchall()

    def add_transaction(self, user_id, amount, type):
        self.cursor.execute("INSERT INTO Transactions (UserID, Amount, Type) VALUES (?, ?, ?)", (user_id, amount, type))
        self.connection.commit()
        print(f"add_transaction: user_id={user_id}, amount={amount}, type={type}")
        self.check_accounts()

    def get_transactions(self, user_id):
        self.cursor.execute("SELECT * FROM Transactions WHERE UserID=?", (user_id,))
        return self.cursor.fetchall()

    def deposit(self, user_id, amount):
        if amount <= 0:
            raise ValueError("The amount must be positive.")
        balance = self.get_balance(user_id)
        new_balance = balance + amount
        print(f"deposit: user_id={user_id}, balance={balance}, amount={amount}, new_balance={new_balance}")
        self.update_balance(user_id, new_balance)
        self.add_transaction(user_id, amount, "Deposit")
        self.check_accounts()

    def transfer_funds(self, from_user_id, to_user_id, amount):
        if amount <= 0:
            raise ValueError("The amount must be positive.")
        from_balance = self.get_balance(from_user_id)
        if from_balance < amount:
            raise ValueError("Insufficient funds.")
        to_balance = self.get_balance(to_user_id)
        self.update_balance(from_user_id, from_balance - amount)
        self.update_balance(to_user_id, to_balance + amount)
        self.add_transaction(from_user_id, -amount, "Transfer Out")
        self.add_transaction(to_user_id, amount, "Transfer In")
        self.check_accounts()

    def check_accounts(self):
        self.cursor.execute("SELECT * FROM Accounts")
        accounts = self.cursor.fetchall()
        for account in accounts:
            print(f"Account: {account}")

    def save_users_to_file(self, filename):
        self.cursor.execute("SELECT * FROM Users")
        users = self.cursor.fetchall()
        with open(filename, 'w') as f:
            json.dump(users, f)
        print(f"Users saved to {filename}")

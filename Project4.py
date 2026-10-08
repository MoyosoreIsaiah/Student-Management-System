import json
import os


# Transaction class
class Transaction:
    def __init__(self, transaction_type, amount, description):
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description

    def to_dict(self):
        return {
            "type": self.transaction_type,
            "amount": self.amount,
            "description": self.description
        }


# Account class
class Account:
    def __init__(self, account_number, full_name, email, pin, balance=0):
        self.account_number = account_number
        self.full_name = full_name
        self.email = email
        self.__pin = pin
        self.__balance = balance
        self.transactions = []

    # Check PIN
    def check_pin(self, pin):
        return self.__pin == pin

    # Get balance
    def get_balance(self):
        return self.__balance

    # Deposit money
    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be greater than 0.")
            return False

        self.__balance += amount

        transaction = Transaction(
            "Deposit",
            amount,
            "Money deposited"
        )

        self.transactions.append(transaction)

        print("Deposit successful.")
        return True

    # Withdraw money
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be greater than 0.")
            return False

        if amount > self.__balance:
            print("Insufficient balance.")
            return False

        self.__balance -= amount

        transaction = Transaction(
            "Withdrawal",
            amount,
            "Money withdrawn"
        )

        self.transactions.append(transaction)

        print("Withdrawal successful.")
        return True

    # Add transfer transaction
    def add_transfer(self, amount, description):
        transaction = Transaction(
            "Transfer",
            amount,
            description
        )

        self.transactions.append(transaction)

    # Convert account to dictionary
    def to_dict(self):
        return {
            "account_number": self.account_number,
            "full_name": self.full_name,
            "email": self.email,
            "balance": self.__balance,
            "transactions": [
                transaction.to_dict()
                for transaction in self.transactions
            ]
        }


# Banking system class
class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()

    # Create account
    def create_account(self):
        account_number = input("Enter account number: ")

        if account_number in self.accounts:
            print("Account number already exists.")
            return

        full_name = input("Enter full name: ")
        email = input("Enter email: ")
        pin = input("Create a 4-digit PIN: ")

        if len(pin) != 4 or not pin.isdigit():
            print("Invalid PIN. PIN must be 4 digits.")
            return

        account = Account(
            account_number,
            full_name,
            email,
            pin
        )

        self.accounts[account_number] = account

        self.save_accounts()

        print("Account created successfully.")

    # Login
    def login(self):
        account_number = input("Enter account number: ")

        if account_number not in self.accounts:
            print("Account not found.")
            return None

        pin = input("Enter PIN: ")

        account = self.accounts[account_number]

        if account.check_pin(pin):
            print("Login successful.")
            return account

        print("Invalid PIN.")
        return None

    # Deposit
    def deposit_money(self, account):
        amount = float(input("Enter amount to deposit: "))

        if account.deposit(amount):
            self.save_accounts()

    # Withdrawal
    def withdraw_money(self, account):
        amount = float(input("Enter amount to withdraw: "))

        if account.withdraw(amount):
            self.save_accounts()

    # Transfer
    def transfer_money(self, sender):
        receiver_number = input("Enter receiver account number: ")

        if receiver_number not in self.accounts:
            print("Receiver account not found.")
            return

        if receiver_number == sender.account_number:
            print("You cannot transfer money to the same account.")
            return

        amount = float(input("Enter amount to transfer: "))

        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        if amount > sender.get_balance():
            print("Insufficient balance.")
            return

        receiver = self.accounts[receiver_number]

        # Remove money from sender
        sender.withdraw(amount)

        # Add money to receiver
        receiver.deposit(amount)

        # Add transfer history
        sender.add_transfer(
            amount,
            "Transfer to " + receiver.account_number
        )

        receiver.add_transfer(
            amount,
            "Transfer from " + sender.account_number
        )

        self.save_accounts()

        print("Transfer successful.")

    # Show balance
    def show_balance(self, account):
        print("Current balance:", account.get_balance())

    # Show transaction history
    def show_transactions(self, account):
        print("\nTransaction History")

        if len(account.transactions) == 0:
            print("No transactions yet.")
            return

        for transaction in account.transactions:
            print(
                transaction.transaction_type,
                "-",
                transaction.amount,
                "-",
                transaction.description
            )

    # Save accounts to file
    def save_accounts(self):
        data = {}

        for account_number, account in self.accounts.items():
            data[account_number] = account.to_dict()

        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)

    # Load accounts from file
    def load_accounts(self):
        if not os.path.exists("accounts.json"):
            return

        with open("accounts.json", "r") as file:
            data = json.load(file)

        for account_number, account_data in data.items():

            account = Account(
                account_data["account_number"],
                account_data["full_name"],
                account_data["email"],
                account_data["pin"],
                account_data["balance"]
            )

            for transaction_data in account_data["transactions"]:

                transaction = Transaction(
                    transaction_data["type"],
                    transaction_data["amount"],
                    transaction_data["description"]
                )

                account.transactions.append(transaction)

            self.accounts[account_number] = account


# Main program
bank = BankingSystem()

while True:

    print("\n===== BANKING SYSTEM =====")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        bank.create_account()

    elif choice == "2":

        account = bank.login()

        if account is not None:

            while True:

                print("\n===== ACCOUNT MENU =====")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Transfer")
                print("4. Check Balance")
                print("5. Transaction History")
                print("6. Logout")

                option = input("Enter your choice: ")

                if option == "1":
                    bank.deposit_money(account)

                elif option == "2":
                    bank.withdraw_money(account)

                elif option == "3":
                    bank.transfer_money(account)

                elif option == "4":
                    bank.show_balance(account)

                elif option == "5":
                    bank.show_transactions(account)

                elif option == "6":
                    print("Logged out successfully.")
                    break

                else:
                    print("Invalid choice.")

    elif choice == "3":

        print("Thank you for using the banking system.")
        break

    else:
        print("Invalid choice.")
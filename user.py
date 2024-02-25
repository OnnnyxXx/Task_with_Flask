class Users:
    def __init__(self, user_id, username, balance):
        self.id = user_id
        self.username = username
        self.balance = balance

    def get_balance(self):
        return self.balance

    def update_balance(self, amount):
        if amount >= 0:
            self.balance += amount
            if self.balance < 0:
                self.balance = 0
        else:
            print("Сумма должна быть неотрицательной.")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Недостаточно средств на счете.")

    def get_info(self):
        return self.balance, self.username, self.id

    def __str__(self):
        return f"User ID: {self.id}, Username: {self.username}, Balance: {self.balance}"

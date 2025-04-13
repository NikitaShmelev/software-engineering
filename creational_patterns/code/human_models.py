from base_models import User

class Admin(User):
    def register(self):
        print("Registering admin")

    def login(self):
        print("Logging in admin")

    def logout(self):
        print("Logging out ADMIN")

class Seller(User):
    def register(self):
        print("Registering Seller")

    def login(self):
        print("Logging in Seller")

    def logout(self):
        print("Logging out Seller")


class Buyer(User):
    def register(self):
        print("Registering Buyer")

    def login(self):
        print("Logging in Buyer")

    def logout(self):
        print("Logging out Buyer")


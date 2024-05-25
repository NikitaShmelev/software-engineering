import random

from base_models import User
from datetime import datetime


class Buyer(User):
    pass


class Admin(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.admin = True


class Transaction:
    transactions: dict[int, "Item"] = {}

    class Statuses:
        SUCCESS = "SUCCESS"
        PENDING = "PENDING"

    def __init__(self, item: "Item", buyer: Buyer) -> None:
        self.id: int = None
        self.item: Item = item
        self.buyer: Buyer = buyer
        self.status: str = self.Statuses.PENDING
        self.created_date: datetime = datetime.now()
        self.finished_date: datetime = None

    def __generate_id(self) -> int:
        current_ids = self.transactions.keys()
        return 1 if not current_ids else max(current_ids) + 1

    def submit(self):
        self.id = self.__generate_id()
        self.transactions[self.id] = self

    def finish(self):
        self.status = self.Statuses.SUCCESS
        self.finished_date = datetime.now()
        self.item.status = Item.Statuses.SOLD


class Item:
    items: dict[int, "Item"] = {}

    class Statuses:
        AVAILABLE = "AVAILABLE"
        SOLD = "SOLD"

    def __init__(self, category, title, price, description, seller) -> None:
        self.id: int = None
        self.category: str = category
        self.title: str = title
        self.price: int = price
        self.description: str = description
        self.seller: Seller = seller
        self.date_added: datetime = datetime.now()
        self.status: str = self.Statuses.AVAILABLE

    def __generate_id(self) -> int:
        current_ids = self.items.keys()
        return 1 if not current_ids else max(current_ids) + 1

    def submit(self) -> None:
        self.id = self.__generate_id()
        Item.items[self.id] = self

    def delete(self) -> None:
        del self.items[self.id]

    def buy(self, buyer: Buyer) -> None:
        transaction = Transaction(self, buyer)
        transaction.submit()

    def edit(self, **kwargs) -> None:
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except Exception as e:
            print("Error during update", e)


class Seller(User):
    def buy(self, item: Item, buyer: Buyer):
        self.item = Transaction(item, buyer)
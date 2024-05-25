import unittest

from models import *
from exceptions import *


class TestUser(unittest.TestCase):
    base_data = {
        "name": "Name",
        "surname": "Surname",
        "phone_number": 123,
        "password": "password",
        "email": "gmail@gmail.com",
    }

    def setUp(self) -> None:
        User.users = {}
        User.emails = []
        return super().setUp()

    def user_was_created(self, user: User):
        self.assertEqual(isinstance(user.id, int), True)
        self.assertIsNotNone(user.get_token())
        self.assertEqual(user.is_created, True)
        self.assertEqual(user.is_logged, True)

    def user_was_not_created(self, user: User):
        self.assertEqual(user.id, None)
        self.assertIsNone(user.get_token())
        self.assertEqual(user.is_created, False)
        self.assertEqual(user.is_logged, False)

    def test_user_creation(self):
        user = User(**self.base_data)
        user.register()
        self.user_was_created(user=user)

    def test_user_creation_with_ivalid_email(self):
        user = User(
            **{**self.base_data, "email": "wrong.email"},
        )
        with self.assertRaises(EmailalidationException):
            user.register()

        self.user_was_not_created(user=user)

    def test_user_creation_with_existing_email(self):
        email = "new@gmail.com"
        user1 = User(
            **{**self.base_data, "email": email},
        )
        user1.register()
        self.user_was_created(user=user1)

        user2 = User(
            **{**self.base_data, "email": email},
        )
        with self.assertRaises(EmailalidationException):
            user2.register()

        self.user_was_not_created(user=user2)

    def test_user_change_password(self):
        email = "new1@gmail.com"
        user = User(**{**self.base_data, "email": email})
        user.register()
        self.user_was_created(user=user)

        user.change_password(
            old_password=self.base_data["password"], new_password="123"
        )

        with self.assertRaises(PasswordValidationException):
            user.change_password(
                old_password=self.base_data["password"], new_password="123"
            )


class TestAdmin(TestUser):
    def test_admin_creation(self):

        admin = Admin(**self.base_data)
        admin.register()
        self.user_was_created(user=admin)
        self.assertEqual(admin.admin, True)


class TestBuyer(TestUser):
    def test_buyer_creation(self):
        buyer = Buyer(**self.base_data)
        buyer.register()
        self.user_was_created(user=buyer)


class TestSeller(TestUser):
    def test_seller_creation(self):
        seller = Seller(**self.base_data)
        seller.register()
        self.user_was_created(user=seller)


class TestItem(unittest.TestCase):
    def setUp(self):
        User.users = {}
        User.emails = []
        self.seller = Seller(
            name="John",
            surname="Doe",
            password="pass123",
            phone_number=1234567890,
            email="seller@example.com",
        )
        self.buyer = Buyer(
            name="Jane",
            surname="Doe",
            password="pass123",
            phone_number=9876543210,
            email="buyer@example.com",
        )
        self.seller.register()
        self.buyer.register()
        self.item = Item(
            category="Electronics",
            title="Phone",
            price=999,
            description="Latest smartphone",
            seller=self.seller,
        )

    def test_item_creation(self):
        self.assertEqual(self.item.category, "Electronics")
        self.assertEqual(self.item.title, "Phone")
        self.assertEqual(self.item.price, 999)
        self.assertEqual(self.item.description, "Latest smartphone")
        self.assertEqual(self.item.seller, self.seller)
        self.assertEqual(self.item.status, Item.Statuses.AVAILABLE)

    def test_generate_id(self):
        Item.items = {}
        self.item.submit()
        self.assertEqual(self.item.id, 1)
        item2 = Item("Electronics", "Laptop", 1999, "Latest laptop", self.seller)
        item2.submit()
        self.assertEqual(item2.id, 2)

    def test_edit_item(self):
        self.item.submit()
        self.item.edit(title="New Phone", price=899)
        self.assertEqual(self.item.title, "New Phone")
        self.assertEqual(self.item.price, 899)

    def test_delete_item(self):
        Item.items = {}
        self.item.submit()
        self.item.delete()
        self.assertNotIn(self.item.id, Item.items)

    def test_buy_item(self):
        Item.items = {}
        self.item.submit()
        self.item.buy(self.buyer)
        # breakpoint()
        self.assertIn(self.item.id, Transaction.transactions)
        transaction = Transaction.transactions[self.item.id]
        self.assertEqual(transaction.item, self.item)
        self.assertEqual(transaction.buyer, self.buyer)
        self.assertEqual(transaction.status, Transaction.Statuses.PENDING)


class TestTransaction(unittest.TestCase):
    def setUp(self):
        User.users = {}
        User.emails = []
        self.seller = Seller(
            name="John",
            surname="Doe",
            password="pass123",
            phone_number=1234567890,
            email="seller@example.com",
        )
        self.buyer = Buyer(
            name="Jane",
            surname="Doe",
            password="pass123",
            phone_number=9876543210,
            email="buyer@example.com",
        )
        self.seller.register()
        self.buyer.register()
        self.item = Item(
            category="Electronics",
            title="Phone",
            price=999,
            description="Latest smartphone",
            seller=self.seller,
        )
        self.item.submit()
        self.transaction = Transaction(self.item, self.buyer)

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.item, self.item)
        self.assertEqual(self.transaction.buyer, self.buyer)
        self.assertEqual(self.transaction.status, Transaction.Statuses.PENDING)
        self.assertIsNone(self.transaction.finished_date)

    def test_submit_transaction(self):
        Transaction.transactions = {}
        self.transaction.submit()
        self.assertIn(self.transaction.id, Transaction.transactions)
        self.assertEqual(
            Transaction.transactions[self.transaction.id], self.transaction
        )

    def test_finish_transaction(self):
        self.transaction.submit()
        self.transaction.finish()
        self.assertEqual(self.transaction.status, Transaction.Statuses.SUCCESS)
        self.assertIsNotNone(self.transaction.finished_date)
        self.assertEqual(self.item.status, Item.Statuses.SOLD)


if __name__ == "__main__":
    unittest.main()

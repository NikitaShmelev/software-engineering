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


if __name__ == "__main__":
    unittest.main()

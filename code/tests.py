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
        return super().setUp()

    def __test_user_was_created(self, user: User):

        self.assertEqual(isinstance(user.id, int), True)
        self.assertIsNotNone(user.get_token())
        self.assertEqual(user.is_created, True)
        self.assertEqual(user.is_logged, True)

    def __test_user_was_not_created(self, user: User):
        self.assertEqual(user.id, None)
        self.assertIsNone(user.get_token())
        self.assertEqual(user.is_created, False)
        self.assertEqual(user.is_logged, False)

    def test_user_creation(self):
        user = User(**self.base_data)
        user.register()
        self.__test_user_was_created(user=user)

    def test_user_creation_with_ivalid_email(self):
        user = User(
            **{**self.base_data, "email": "wrong.email"},
        )
        with self.assertRaises(EmailalidationException):
            user.register()

        self.__test_user_was_not_created(user=user)

    def test_user_creation_with_existing_email(self):
        email = "new@gmail.com"
        user1 = User(
            **{**self.base_data, "email": email},
        )
        user1.register()
        self.__test_user_was_created(user=user1)

        user2 = User(
            **{**self.base_data, "email": email},
        )
        with self.assertRaises(EmailalidationException):
            user2.register()

        self.__test_user_was_not_created(user=user2)


if __name__ == "__main__":
    unittest.main()

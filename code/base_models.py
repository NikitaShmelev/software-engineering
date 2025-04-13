from datetime import datetime
from exceptions import PasswordValidationException, EmailalidationException
from utils import validate_email


class User:
    users: dict[int, "User"] = {}
    emails: list[str] = []

    def __init__(
        self, name, surname, password, phone_number, email, nickname=None
    ) -> None:
        self.id: int | None = None
        self.name: str = name
        self.surname: str = surname
        self.nickname: str = nickname
        self.admin: bool = False
        self.phone_number: int = phone_number
        self.password: str = self.__encrypt_password(password)
        self.email: str = email
        self.is_created: bool = False
        self.is_logged: bool = False
        self.__token: int | None = None

    def __encrypt_password(self, password) -> str:
        return str(hash(password))

    def get_token(self):
        return self.__token

    def login(self):
        pass

    def logout(self):
        pass

    def __genetate_id(self) -> int:
        current_ids = self.users.keys()
        return 1 if not current_ids else max(current_ids) + 1

    def register(self):
        if not validate_email(self.email):
            raise EmailalidationException()
        elif self.email in self.emails:
            raise EmailalidationException("Providen email already exists")

        self.is_created = True
        self.is_logged = True
        self.__token = self.__generate_token()

        self.id = self.__genetate_id()

        self.emails.append(self.email)
        self.users[self.id] = self

    def change_password(self, old_password: str, new_password: str) -> None:
        if str(hash(old_password)) == self.password:
            self.password = self.__encrypt_password(new_password)
        else:
            raise PasswordValidationException()

    def __generate_token(self) -> str:
        return str(hash(datetime.now()))

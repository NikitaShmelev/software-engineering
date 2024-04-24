# from typing import Hashable
from datetime import datetime
class User:
    def __init__(self, name, surname, password, phone_number, nickname=None) -> None:
        self._id: int = None
        self.name: str = name
        self.surname: str = surname
        self.nickname: str = nickname
        self.admin: bool = False
        self.phone_number: int = phone_number
        
        self.password: str = self.__generate_password(password)
        self.token = self.__generate_token()
        
    def __generate_password(self, password) -> str:
        return str(hash(password))
    
    
    def __generate_token(self) -> str:
        return str(hash(datetime.now()))

class Buyer(User):
    pass

class Seller(User):
    pass


class Admin(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.admin = True
        
        
user = User(
    name="Nikita",
    surname="Shmelyov",
    phone_number=123,
    password="password"
)


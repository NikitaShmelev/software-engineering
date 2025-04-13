
from typing import Optional
from abc import ABC, abstractmethod


class User(ABC):
    users: dict[int, "User"] = {}
    emails: list[str] = []

    def __init__(
        self, name, email
    ) -> None:
        """
        Admin, Buyer, Seller should inherit from it
        """
        self.id: Optional[int] = None
        self.name: str = name
        self.email: str = email

        # add other fields later

    @abstractmethod
    def register(self):
        # implement in children classes
        pass
    
    @abstractmethod
    def login(self):
        # implement in children classes
        pass

    @abstractmethod
    def logout(self):
        # implement in children classes
        pass

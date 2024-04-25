from base_models import User


class Buyer(User):
    pass


class Seller(User):
    pass


class Admin(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.admin = True

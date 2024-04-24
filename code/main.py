class User:
    def __init__(self, name) -> None:
        self._id = None
        self.name = name
        self.admin = False
    
    


class Buyer(User):
    pass

class Seller(User):
    pass


class Admin(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.admin = True
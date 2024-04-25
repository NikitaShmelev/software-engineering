class PasswordValidationException(Exception):
    def __init__(self, message="Provided password in invalid, try again"):
        self.message = message
        super().__init__(self.message)


class EmailalidationException(Exception):
    def __init__(self, message="Provided email in invalid"):
        self.message = message
        super().__init__(self.message)

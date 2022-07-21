class UserAlreadyExistError(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message

class UserPasswordNotCorrectError(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message

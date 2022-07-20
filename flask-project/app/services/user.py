import datetime

import bcrypt
from flask_jwt_extended import create_access_token
from typing import Optional

from app.model.user import UserModel
from app.error.user import UserAlreadyExistError

class UserService:
    def __init__(self, email: Optional[str], password: Optional[str], name: Optional[str]):
        self.email = email
        self.password = password
        self.name = name

        if UserModel.objects.filter(email=self.email):
            raise UserAlreadyExistError("User is Already Existed", 409)

    def sign_up(self):
        hashed_password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt())
        user_model = UserModel(
            name = self.name,
            password = hashed_password,
            email = self.email,
            activated = False
        )
        user_model.save()

        return create_access_token(identity=self.email, expires_delta=datetime.timedelta(minutes=30))

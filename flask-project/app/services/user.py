import datetime

import bcrypt
from flask_jwt_extended import create_access_token
from typing import Optional

from app.model.user import UserModel
from app.error.user import UserAlreadyExistError, UserPasswordNotCorrectError


class UserService:
    def __init__(self, email: Optional[str], password: Optional[str], name: Optional[str]):
        self.email = email
        self.password = password
        self.name = name

    def sign_up(self):
        if UserModel.objects.filter(email=self.email):
            raise UserAlreadyExistError("User is Already Existed", 409)

        hashed_password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt())
        user_model = UserModel(
            name = self.name,
            password = hashed_password.decode("utf-8"),
            email = self.email,
            activated = False
        )
        user_model.save()

    def login(self):
        user = UserModel.objects(email=self.email).first()

        if user is not None and bcrypt.checkpw(self.password.encode("utf-8"), user.password.encode("utf-8")):
            return create_access_token(identity=self.email, expires_delta=datetime.timedelta(hours=24))
        else:
            raise UserPasswordNotCorrectError("User password Not Correct", 401)

    def edit(self):
        user = UserModel.objects(email=self.email)

        if user is not None and bcrypt.checkpw(self.password.encode("utf-8"), user.password.encode("utf-8")):
            user.update(name=self.name)
            user.save()
            return True
        else:
            raise UserPasswordNotCorrectError("User password Not Correct", 401)

    def delete(self):
        user = UserModel.objects(email=self.email)

        if user is not None and bcrypt.checkpw(self.password.encode("utf-8"), user.password.encode("utf-8")):
            user.delete()
            return True
        else:
            raise UserPasswordNotCorrectError("User password Not Correct", 401)


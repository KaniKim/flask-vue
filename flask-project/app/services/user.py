import bcrypt
import datetime
from typing import Optional

from app.model.user import UserModel
from app.error.user import UserAlreadyExistError


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

    def edit(self):
        return UserModel.objects(email=self.email).update(name=self.name)

    def delete(self):
        user = UserModel.objects(email=self.email).first()

        if user is not None:
            user.deleted_at = datetime.datetime.utcnow()
            user.activated = False
            user.save()
            return True
        return False


import datetime
from functools import wraps
import bcrypt

from app.model.user import UserModel
from app.error.user import UserPasswordNotCorrectError, UserIsDeleted

def check_password(f):
    @wraps(f)
    def decorated_func(self, *args, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")

        if email is None and password is None:
            return f(self, **kwargs)

        user_model = UserModel.objects(email=email).first()

        if user_model is None:
            return "User Email or Password is Wrong", 404

        if user_model.deleted_at is not None and user_model.deleted_at < datetime.datetime.now():
            raise UserIsDeleted("User is Deleted", 404)

        if user_model is not None:
            if bcrypt.checkpw(password.encode("utf-8"), user_model.password.encode("utf-8")):
                return f(self, **kwargs)
            else:
                return "wrong password", 409
        return f(self, **kwargs)
    return decorated_func
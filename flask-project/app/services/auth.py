from functools import wraps
import bcrypt

from app.model.user import UserModel
from app.error.user import UserPasswordNotCorrectError

def check_password(f):
    @wraps(f)
    def decorated_func(self, *args, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")
        user_model = UserModel.objects(email=email).first()
        if user_model is not None and user_model.deleted_at is None:
            if bcrypt.checkpw(password.encode("utf-8"), user_model.password.encode("utf-8")):
                return f(self, **kwargs)
            else:
                raise UserPasswordNotCorrectError("wrong password", 409)
        return f(self, None, None, None)
    return decorated_func
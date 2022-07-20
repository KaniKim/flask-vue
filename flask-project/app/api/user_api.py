from flask_classful import FlaskView, route
from flask_apispec import doc, marshal_with, use_kwargs
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

from app.model.user import UserModel
from app.schema.user import UserSchema, UserSignUpSchema
from app.services.user import UserService

class User(FlaskView):
    @route("/me", methods=["GET"])
    @doc(description="User 정보 조회", summary="User 정보 조회")
    @marshal_with(UserSchema(), code=200)
    @jwt_required()
    def get(self):
        return UserModel.objects.filter(id=id)

    @doc(description="User 회원가입", summary="User 회원가입")
    @route("/sign-up", methods=["POST"])
    @use_kwargs(UserSchema(only=("name", "email", "password"), partial=True), locations=("json", ))
    @marshal_with(UserSignUpSchema(), code=201)
    @cross_origin()
    def post(self, **kwargs):
        user_service = UserService(name=kwargs.get("name"),email=kwargs.get("email"), password=kwargs.get("password"))
        return user_service.sign_up(), 201

    @route("/me", methods=["PUT"])
    def put(self):
        pass

    @route("/me", methods=["DELETE"])
    def unregister(self):
        pass


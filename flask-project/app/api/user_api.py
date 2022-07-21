from flask import jsonify
from flask_classful import FlaskView, route
from flask_apispec import doc, marshal_with, use_kwargs
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.model.user import UserModel
from app.schema.user import UserSchema, UserSignUpSchema, UserLoginSchema
from app.services.user import UserService

class User(FlaskView):
    @route("/me", methods=["GET"])
    @doc(description="User 정보 조회", summary="User 정보 조회")
    @marshal_with(UserSchema(only=("email", "name",), partial=True), code=200)
    @cross_origin()
    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        name = UserModel.objects(email=email).first().name
        return jsonify(email=email, name=name), 200

    @doc(description="User 회원가입", summary="User 회원가입")
    @route("/sign-up", methods=["POST"])
    @cross_origin()
    @use_kwargs(UserSchema(only=("name", "email", "password"), partial=True), locations=("json", ))
    def sign_up(self, **kwargs):
        UserService(name=kwargs.get("name"),email=kwargs.get("email"), password=kwargs.get("password")).sign_up()
        return "SUCCESS", 201

    @doc(description="User 로그인", summary="User 로그인")
    @route("/login", methods=["POST"])
    @use_kwargs(UserSchema(only=("email", "password"), partial=True), locations=("json",))
    @marshal_with(UserLoginSchema(), code=200)
    @cross_origin()
    def login(self, **kwargs):
        user_service = UserService(name=None, email=kwargs.get("email"), password=kwargs.get("password"))
        jwt = user_service.login()
        return jwt, 200

    @route("/me", methods=["PUT"])
    @use_kwargs(UserSchema(only=("email",), partial=True), locations=("json",))
    @marshal_with(UserLoginSchema(), code=201)
    @jwt_required
    @cross_origin()
    def put(self, **kwargs):
        user_service = UserService(name=kwargs.get("name"), password=kwargs.get("password"), email=kwargs.get("email"))
        if user_service.edit():
            return "EDIT SUCCESSFUL", 201
        return "EDIT FAIL", 404

    @route("/me", methods=["DELETE"])
    @use_kwargs(UserSchema(only=("email",), partial=True), locations=("json",))
    @marshal_with(UserSignUpSchema(), code=204)
    @jwt_required
    @cross_origin()
    def unregister(self, **kwargs):
        user_service = UserService(name=kwargs.get("name"), password=kwargs.get("password"), email=kwargs.get("email"))
        if user_service.edit():
            return "EDIT SUCCESSFUL", 204
        return "EDIT FAIL", 404


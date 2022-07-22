from flask_classful import FlaskView, route
from flask_apispec import doc, marshal_with, use_kwargs
from flask_cors import cross_origin
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

import datetime

from app.model.user import UserModel
from app.schema.user import UserSchema
from app.services.auth import check_password
from app.services.user import UserService

class User(FlaskView):
    @route("/me", methods=["GET", "PUT", "DELETE"])
    @doc(description="User 정보 조회, 수정, 삭제", summary="User 정보")
    @marshal_with(UserSchema(exclude=["_id", "password"]), code=200)
    @use_kwargs(UserSchema(only=("name", "email", "password"), partial=True), locations=("json", ))
    @marshal_with(None, code=204)
    @cross_origin()
    @check_password
    @jwt_required()
    def index(self, name=None, password=None, email=None):
        if request.method in ["GET"]:
            user_model = UserModel.objects.filter(email=get_jwt_identity()).only("email", "name").first()
            return user_model.to_json(), 200

        user_service = UserService(name=name, password=password, email=email)
        print(request.method)
        if request.method in ["PUT"]:
            if user_service.edit():
                return "EDIT SUCCESSFUL", 201
            return "EDIT FAIL", 404

        if request.method in ["DELETE"]:
            if user_service.delete():
                return "DELETE SUCCESSFUL", 204
            return "DELETE FAIL", 404

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
    @cross_origin()
    @check_password
    def login(self, email, password):
        return create_access_token(identity=email, expires_delta=datetime.timedelta(hours=24)), 201



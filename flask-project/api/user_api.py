from flask import request, jsonify, make_response, session
from flask_restful import Resource
from flask_apispec import marshal_with, MethodResource

import jwt
import hashlib
import datetime

from ..config import Config
from ..repository.user import UserRepository
from ..domain.user import UserSchema


UserRepo = UserRepository()


class User(MethodResource, Resource):
    @marshal_with(UserSchema)
    def post(self):
        name = request.get_json()["name"]
        email = request.get_json()["email"]
        password = request.get_json()["password"]

        pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        user = UserRepo.find_user_by_email(email=email)
        if user:
            return make_response(jsonify({"msg": "User is already existed"}), 400)

        return make_response(
            jsonify(
                UserRepo.save_user(name=name, email=email, password=pw_hash),
                201,
            )
        )


class UserAuth(MethodResource, Resource):
    @marshal_with(UserSchema)
    def post(self):

        if not request:
            return make_response(jsonify({"msg": "Missing Login Info"}), 400)

        email = request.form.to_dict()["userData[username]"]
        pw_received = request.form.to_dict()["userData[password]"]

        pw_hash = hashlib.sha256(pw_received.encode("utf-8")).hexdigest()

        user = UserRepo.find_user_by_email_and_password(email=email, password=pw_hash)

        if user is None:
            return make_response(jsonify("Wrong Mail or Password"), 404)
        else:

            access_token = jwt.encode(
                {"username": user[0]["email"]}, Config.key, algorithm="HS256"
            )
            return make_response(
                jsonify(
                    username=user[0]["email"],
                    access_token=access_token,
                ),
                200,
            )

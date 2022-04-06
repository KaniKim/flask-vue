from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace
from flask_restx.fields import String, Boolean, Nested

from bson.objectid import ObjectId
import json

from ..model.user_model import User as UserMongo


User = Namespace("User", description="CRUD for User API")

UserPost = User.model(
    "user_post",
    {
        "name": String,
        "email": String,
        "password": String,
    },
)

UserModel = User.inherit(
    "user",
    UserPost,
    {
        "_id": String,
        "activated": Boolean,
    },
)
UserAllModel = User.model("user_all", {"users": Nested(UserModel)})


@User.route("")
class UserAll(Resource):
    @User.marshal_with(UserModel, code=200)
    def get(self):
        if UserMongo.objects is None:
            return None

        return [json.loads(user.to_json()) for user in UserMongo.objects()]

    @User.marshal_with(UserModel, code=200)
    def post(self):

        name = request.get_json()["name"]
        email = request.get_json()["email"]
        password = request.get_json()["password"]

        UserMongo(
            name=name,
            email=email,
            password=password,
            activated=True,
        ).save()
        return {"name": name, "email": email, "password": password}


@User.route("/<string:user_id>")
class UserOne(Resource):
    @User.marshal_with(UserModel, code=200)
    def get(self, user_id: str):

        return json.loads(UserMongo.objects.filter(id=ObjectId(user_id)).to_json())

    @User.marshal_with(UserModel, code=201)
    def put(self, user_id: str):
        name = request.get_json()["name"]
        email = request.get_json()["email"]
        password = request.get_json()["password"]

        user = UserMongo.objects.filter(id=ObjectId(user_id))[0]

        user.name = name
        user.email = email
        user.password = password
        user.save()

        return json.loads(user.to_json())

    def delete(self, user_id: str):
        user = UserMongo.objects.filter(id=ObjectId(user_id))
        user_valid = json.loads(user.to_json())

        if len(user_valid) == 0:
            return make_response(jsonify("No User to delete"), 404)

        user.delete()

        return make_response(jsonify("User is deleted"), 204)

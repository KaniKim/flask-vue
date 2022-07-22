from flask_classful import FlaskView, route
from flask_apispec import doc, marshal_with, use_kwargs
from flask_cors import cross_origin
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

import json

from app.model.column import ColumnModel, TagModel
from app.model.user import UserModel
from app.schema.column import ColumnSchema
from app.schema.user import UserSchema
from app.services.auth import check_password
from app.services.column import ColumnService

class ColumnView(FlaskView):
    @route("/me", methods=["GET", "PUT", "DELETE"])
    @doc(description="User가 쓴 칼럼 조회, 수정, 삭제", summary="User 칼럼 정보")
    @marshal_with(UserSchema(exclude=["_id", "password"]), code=200)
    #@use_kwargs(UserSchema(only=("name", "email", "password"), partial=True), locations=("json",))
    @marshal_with(None, code=204)
    @cross_origin()
    @check_password
    @jwt_required()
    def index(self):
        if request.method in ["GET"]:
            user_id = UserModel.objects.filter(email=get_jwt_identity()).first().id
            column_models = ColumnModel.objects.filter(author=user_id).only("title", "tags")

            return {"columns": [{"title":column_model.title, "tags": [tag.name for tag in column_model.tags]} for column_model in column_models]}, 200


    @doc(description="Column 작성", summary="Column 작성")
    @route("/", methods=["POST"])
    @cross_origin()
    @jwt_required()
    @use_kwargs(ColumnSchema(only=("title", "content", "tags"), partial=True), locations=("json",))
    @marshal_with(None, apply=False,code=201)
    def write_column(self, content, title, tags):
        request_data = json.loads(request.data)
        print(request_data)
        if ColumnService(title=title, content=content, tags=tags, email=get_jwt_identity()).save_column():
            return "SUCCESS", 201
        return "FAILED", 404
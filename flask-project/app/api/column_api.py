from flask_classful import FlaskView, route
from flask_apispec import doc, marshal_with, use_kwargs
from flask_cors import cross_origin
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

import json

from app.model.column import ColumnModel, BoardModel
from app.model.user import UserModel
from app.schema.column import ColumnSchema, ColumnBoardSchema, BoardSchema, ColumnAllSchema
from app.services.auth import check_password
from app.services.column import ColumnService

class ColumnView(FlaskView):
    @route("/me", methods=["GET", "PUT", "DELETE"])
    @doc(description="User가 쓴 칼럼 조회, 수정, 삭제", summary="User 칼럼 정보")
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
    @use_kwargs(ColumnBoardSchema(), locations=("json",))
    @marshal_with(None, apply=False,code=201)
    def write_column(self, content, title, tags, name):
        if ColumnService(title=title, content=content, tags=tags, email=get_jwt_identity(), name=name).save_column():
            return "SUCCESS", 201
        return "FAILED", 404

class BoardView(FlaskView):
    @route('/all', methods=["GET"])
    @doc(description="모든 Board의 게시글들 조회", summary="게시글들 조회")
    @marshal_with(ColumnAllSchema(), 200)
    @cross_origin()
    @jwt_required()
    def index(self):
        boards = BoardModel.objects.all()
        board_columns = [json.loads(ColumnModel.objects.filter(id=column.id).first().to_json()) for board in boards for column in board.columns ]
        return {"columns": board_columns}, 200

    @route('/page/<board_id>', methods=["GET"])
    @doc(description="특정 Board의 게시글들 조회", summary="게시글들 조회")
    @marshal_with(BoardSchema(), 200)
    @marshal_with(None, 404)
    @cross_origin()
    @jwt_required()
    def get_board(self, board_id):
        board = BoardModel.objects.filter(id=board_id).first()
        board_columns = [ColumnModel.objects.filter(id=column_id).first() for column_id in board.columns]
        return {"name": board.name, "columns": board_columns}, 200

    @route('/page/<board_id>/column/<column_id>', methods=["GET"])
    @doc(description="특정 Board의 게시글 조회", summary="게시글 조회")
    @marshal_with(ColumnSchema(), 200)
    @marshal_with(None, 404)
    @cross_origin()
    @jwt_required()
    def get_column(self, board_id, column_id):
        board = BoardModel.objects.filter(id=board_id).first()
        if column_id in board.columns:
            return ColumnModel.objects.filter(id=column_id).first()
        return None, 404
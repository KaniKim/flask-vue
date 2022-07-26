from flask_classful import FlaskView, route
from flask_apispec import doc, marshal_with, use_kwargs
from flask_cors import cross_origin
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

import json
from bson import ObjectId

from app.model.column import ColumnModel, BoardModel, TagModel, CommentModel
from app.model.user import UserModel
from app.schema.column import ColumnSchema, ColumnBoardSchema, BoardSchema, ColumnAllSchema, LikeSchema, CommentSchema, \
    NextCommentSchema, ListCommentSchema
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
    @use_kwargs(ColumnBoardSchema(), location="json")
    @marshal_with(None, apply=False,code=201)
    def write_column(self, content, title, tags, name):
        if ColumnService(title=title, content=content, tags=tags, email=get_jwt_identity(), name=name).save_column():
            return "SUCCESS", 201
        return "FAILED", 404

    @doc(description="Column 좋아요 추가", summary="Column 좋아요 추가")
    @route("/<column_id>/like", methods=["POST"])
    @cross_origin()
    @jwt_required()
    @marshal_with(LikeSchema(), 201)
    def like_column(self, column_id):
        column = ColumnModel.objects(id=ObjectId(column_id)).first()
        if column:
            column.like += 1
            column.save()
            return column.like, 201
        return None, 404

    @doc(description="Column 댓글 조회", summary="Column 댓글 조회")
    @route("/<column_id>/comment", methods=["GET"])
    @cross_origin()
    @jwt_required()
    @marshal_with(CommentSchema(only=("content",), partial=True), 201)
    @marshal_with(ListCommentSchema(), 200)
    def get_comment_column(self, column_id):
        column = ColumnModel.objects(id=ObjectId(column_id)).first()

        if not column:
            return "No column", 404

        comments = [CommentModel.objects.filter(id=comment.id).first() for comment in column.comments]

        next_comments = {"comments": [
                            {
                                "id": str(comment.id),
                                "content": comment.content,
                                "author": UserModel.objects.filter(id=ObjectId(comment.author.id)).first().name,
                                "next_comment":
                                    [
                                        {
                                            "content" : CommentModel.objects.filter(id=ObjectId(next_comment.id)).first().content,
                                            "author" : UserModel.objects.filter(id=ObjectId(CommentModel.objects.filter(id=ObjectId(next_comment.id)).first().author.id)).first().name
                                        }
                                        for next_comment in comment.next_comment
                                    ]
                             }
                            for comment in comments]
                        }

        return next_comments, 200

    @doc(description="Column 댓글 추가", summary="Column 댓글 추가 ")
    @route("/<column_id>/comment", methods=["POST"])
    @cross_origin()
    @jwt_required()
    @use_kwargs(CommentSchema(only=("content",), partial=True), location="json")
    @marshal_with(CommentSchema(only=("content",), partial=True), 201)
    @marshal_with(ListCommentSchema(), 200)
    def post_comment_column(self, column_id, content):
        column = ColumnModel.objects(id=ObjectId(column_id)).first()

        if not column:
            return "No column", 404

        user = UserModel.objects.filter(email=get_jwt_identity()).first()
        if column.comments:
            comment = CommentModel(content=content, author=user, next_comment=[]).save()
            column.comments.append(comment)
        else:
            column.comments = [CommentModel(content=content, author=user, next_comment=[]).save()]
        column.save()
        return content, 201


class CommentView(FlaskView):
    @doc(description="Column 대댓글 추가", summary="Column 대댓글 추가")
    @route("/<comment_id>/next", methods=["POST"])
    @cross_origin()
    @jwt_required()
    @use_kwargs(NextCommentSchema(only=("content",), partial=True), location="json")
    @marshal_with(NextCommentSchema(only=("content",), partial=True), 201)
    def comment_column(self, comment_id, content):
        comment = CommentModel.objects.filter(id=ObjectId(comment_id)).first()
        if comment:
            user = UserModel.objects.filter(email=get_jwt_identity()).first()
            if comment.next_comment:
                comment = CommentModel(content=content, author=user).save()
                comment.next_comment.append(comment)
            else:
                comment.next_comment = [CommentModel(content=content, author=user).save()]
            comment.save()
            return content, 201
        return None, 404

class BoardView(FlaskView):
    @route('/all', methods=["GET"])
    @doc(description="모든 Board의 게시글들 조회", summary="게시글들 조회")
    @marshal_with(ColumnAllSchema(), 200)
    @cross_origin()
    @jwt_required()
    def index(self):
        boards = BoardModel.objects.all()
        board_columns = [{"column" : json.loads(ColumnModel.objects.filter(id=column.id).first().to_json()), "name": board.name } for board in boards for column in board.columns ]
        return {"columns": board_columns}, 200

    @route('/<board_name>', methods=["GET"])
    @doc(description="특정 Board의 게시글들 조회", summary="게시글들 조회")
    @marshal_with(BoardSchema(), 200)
    @use_kwargs(BoardSchema(only=("name",), partial=True), location="json")
    @marshal_with(None, 404)
    @cross_origin()
    @jwt_required()
    def get_board(self, board_name):
        board = BoardModel.objects.filter(name=board_name).first()
        if board is None:
            return "There is no COLUMN", 404
        board_columns = [{"column":json.loads(ColumnModel.objects.filter(id=column.id).first().to_json()), "name": board.name} for column in board.columns]
        return {"columns": board_columns}, 200

    @route('/<board_name>/column/<column_id>', methods=["GET"])
    @doc(description="특정 Board의 게시글 조회", summary="게시글 조회")
    @marshal_with(ColumnSchema(), 200)
    @marshal_with(None, 404)
    @cross_origin()
    @jwt_required()
    def get_column(self, board_name, column_id):
        board = BoardModel.objects.filter(name=board_name).first()
        if board is None:
            return None, 404
        column = ColumnModel.objects.filter(id=ObjectId(column_id)).first()

        return_value = {
            "id": str(column.id),
            "author": UserModel.objects.filter(id=column.author.id).first().name,
            "content": column.content,
            "tags": [TagModel.objects.filter(id=tag.id).first().name for tag in column.tags],
            "title": column.title,
            "like": column.like,
        }
        return return_value, 200
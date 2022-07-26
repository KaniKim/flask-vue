from app.api.user_api import UserView
from app.api.column_api import CommentView, ColumnView, BoardView
from flask import Blueprint, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

api = Blueprint("api", __name__)
def register_api(app):
    UserView.register(api, route_base="/user", trailing_slash=False)
    BoardView.register(api, route_base="/board", trailing_slash=False)
    ColumnView.register(api, route_base="/column", trailing_slash=False)
    CommentView.register(api, route_base="/comment", trailing_slash=False)


    register_swagger(api)
    app.register_blueprint(api)
    SWAGGER_URL = '/swagger'
    API_URL = '/apispec'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test application"
        },
    )

    app.register_blueprint(swaggerui_blueprint)


def register_swagger(bp):
    from app.apidocs_utils import generate_api_spec

    @bp.route("/apispec")
    def apispec():
        return jsonify(generate_api_spec(title="Aimmo On-Boarding 게시판 만들기", version="v1", bp_name=bp.name if isinstance(bp, Blueprint) else None))
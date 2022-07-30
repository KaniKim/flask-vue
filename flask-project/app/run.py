from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from mongoengine import connect

from app.api.column_api import ColumnView, BoardView, CommentView
from app.api.user_api import UserView
from app import register_api


def create_app(test=False):
    app = Flask(__name__)
    app.config.update(
        DEBUG=True,
        JWT_SECRET_KEY="HELLO GUYS"
    )
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='kani',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version="3.0.2",
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',
    })
    if not test:
        connect("test", username="kani", password="123456", host="mongodb://mongodb:27017", port=27017, connect=False)
    else:
        connect(host="mongomock://localhost")
    CORS(app,
         intercept_exceptions=False,
         supports_credentials=True,
         resources={
             r"/*": {
                 "origins": [
                     "http://localhost:8080",
                     "http://localhost",
                     "http://127.0.0.1:8080",
                     "http://127.0.0.1",
                 ]
             }
         },
         )
    jwt = JWTManager(app)

    UserView.register(app, route_base="/user", trailing_slash=False)
    ColumnView.register(app, route_base="/column", trailing_slash=False)
    BoardView.register(app, route_base='/board', trailing_slash=False)
    CommentView.register(app, route_base='/comment', trailing_slash=False)

    register_api(app)

    return app
application = create_app()
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
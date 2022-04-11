from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager

from .config import Config
from .model import db
from .api.user_api import User, UserAuth
from .api.post_api import Post


app = Flask(__name__)


app.config["MONGODB_SETTINGS"] = {
    "db": "test",
    "port": 27017,
    "username": "kani",
    "password": "123456",
    "host": "mongodb://mongodb/test",
}
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_FORM_KEY"] = "access_token"
app.config["JWT_ALGORITHM"] = "HS512"
app.config["JWT_SECRET_KEY"] = Config.key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.access
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = Config.refresh

CORS(app)

jwt = JWTManager(app)
api = Api(app)

api.add_resource(UserAuth, "/auth", endpoint="auth")
api.add_resource(User, "/user", endpoint="user")
api.add_resource(Post, "/post", endpoint="post")

app.config["APISPEC_SPEC"] = APISpec(
    title="Awesome Project",
    version="v1",
    plugins=[MarshmallowPlugin()],
    openapi_version="2.0.0",
)

docs = FlaskApiSpec(app)

with app.app_context():
    docs.register(User, "user")
    docs.register(UserAuth, "auth")
    docs.register(Post, "post")
db.init_app(app)

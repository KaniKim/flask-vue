from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from mongoengine import connect

from app.api.column_api import ColumnView, BoardView, CommentView
from app.api.user_api import User

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "HELLO GUYS"
)

connect("test", username="kani", password="123456", host="mongodb://kani:123456@127.0.01:27017/test?authSource=admin", port=27017)
CORS(app,
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

User.register(app, route_base="/user",  trailing_slash=False)
ColumnView.register(app, route_base="/column", trailing_slash=False)
BoardView.register(app, route_base='/board', trailing_slash=False)
CommentView.register(app, route_base='/comment', trailing_slash=False)

if __name__ == "__main__":
    app.run()


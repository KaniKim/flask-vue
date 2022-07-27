import pytest
from app.run import create_app


@pytest.fixture(scope="session", autouse=True)
def app():
    app = create_app(True)
    return app

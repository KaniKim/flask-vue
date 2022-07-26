import pytest

class Describe_UserView:
    @pytest.fixture
    def password(self):
        return "qwer!1234"

    @pytest.fixture
    def user(self, password):
        pass
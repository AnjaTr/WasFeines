import pytest

from wasfeines.app import create_app
from wasfeines.app import valid_user_session
from wasfeines.models import User

def mock_valid_user_session() -> User:
    return User(
        name="Test User",
        email="test@user.com",
        picture="https://example.com/picture.jpg",
        given_name="Test",
        family_name="User",
        sub="1234567890",
    )

@pytest.fixture
def app():
    app = create_app()
    app.dependency_overrides[valid_user_session] = mock_valid_user_session
    yield app
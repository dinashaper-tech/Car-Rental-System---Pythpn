import pytest
from src.database import Database
from src.auth_service import AuthService
from src.models import User, Role, Base
from sqlalchemy import create_engine

@pytest.fixture
def db():
    # Setup an in-memory SQLite database for isolated tests
    db = Database()
    db._engine = create_engine("sqlite:///:memory:")  # in-memory DB
    Base.metadata.create_all(db._engine)  # create all tables
    yield db
    Base.metadata.drop_all(db._engine)  # clean up tables after tests

def test_register_valid(db):
    # test registering a valid user
    auth = AuthService(db.get_session())
    user = auth.register("John", "Doe", "john@example.com", "1234567890", "Test123")
    assert user.email == "john@example.com"
    assert user.role == Role.MEMBER

def test_register_duplicate_email(db):
    # test that registering a duplicate email raises an error
    auth = AuthService(db.get_session())
    auth.register("John", "Doe", "john@example.com", "1234567890", "Test123")
    with pytest.raises(ValueError, match="Email already exists."):
        auth.register("Jane", "Doe", "john@example.com", "0987654321", "Test123")

def test_login_invalid(db):
    # test that login fails for non-existent user
    auth = AuthService(db.get_session())
    with pytest.raises(ValueError, match="Invalid email or password."):
        auth.login("john@example.com", "Test123")

import bcrypt
from sqlalchemy.orm import Session
from src.models import User, Role
import re
from datetime import datetime

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def validate_password(self, password: str) -> bool:
        # password must be at least 6 chars, contain letters and numbers
        if len(password) < 6 or not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
            raise ValueError("Password must be ≥6 chars, include one number and one letter.")
        return True

    def register(self, first_name: str, last_name: str, email: str, mobile_number: str, password: str, role: Role = Role.MEMBER) -> User:
        # prevent duplicate email registration
        if self.db.query(User).filter(User.email == email).first():
            raise ValueError("Email already exists.")
        
        # check password rules
        self.validate_password(password)

        # hash password before storing
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # create new user
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
            password_hash=hashed,
            role=role
        )
        self.db.add(user)
        self.db.commit()
        return user

    def login(self, email: str, password: str) -> User:
        # check if user exists
        user = self.db.query(User).filter(User.email == email).first()
        # verify password
        if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            raise ValueError("Invalid email or password.")
        return user

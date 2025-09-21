from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base
import os

class Database:
    _instance = None  

    def __new__(cls):
        
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)

            # set database file path
            db_path = os.path.join("db", "car_rental.db")

            # make sure "db" folder exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            # create SQLite engine
            cls._engine = create_engine(f"sqlite:///{db_path}")

            # create tables if they don't exist
            Base.metadata.create_all(cls._engine)

            # session factory
            cls._Session = sessionmaker(bind=cls._engine)

        return cls._instance

    def get_session(self):
        # open a new database session
        return self._Session()

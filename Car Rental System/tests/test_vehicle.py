import pytest
from src.database import Database
from src.vehicle_service import VehicleService
from src.models import VehicleType, Base
from sqlalchemy import create_engine

@pytest.fixture
def db():
    # Setup an in-memory SQLite database for isolated testing
    db = Database()
    db._engine = create_engine("sqlite:///:memory:")  # use in-memory DB
    Base.metadata.create_all(db._engine)  # create tables
    yield db
    Base.metadata.drop_all(db._engine)  # drop tables after test

def test_add_vehicle(db):
    # initialize the VehicleService
    service = VehicleService(db.get_session())
    
    # add a test vehicle
    vehicle = service.add_vehicle(
        "ABC123", "Toyota Camry", VehicleType.SEDAN, 2020, 50000, 100000, 2, 72, 500
    )
    
    # check that the vehicle was added correctly
    assert vehicle.plate == "ABC123"

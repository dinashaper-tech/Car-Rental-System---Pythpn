import pytest
from src.database import Database
from src.rental_service import RentalService
from src.vehicle_service import VehicleService
from src.auth_service import AuthService
from src.models import VehicleType, Role, Base
from datetime import datetime, timedelta
from sqlalchemy import create_engine

@pytest.fixture
def db():
    # setup an in-memory SQLite database for isolated testing
    db = Database()
    db._engine = create_engine("sqlite:///:memory:")  # use in-memory DB
    Base.metadata.create_all(db._engine)  # create all tables
    yield db
    Base.metadata.drop_all(db._engine)  # drop tables after test

def test_create_booking(db):
    # initialize services
    auth = AuthService(db.get_session())
    vehicle_service = VehicleService(db.get_session())
    rental_service = RentalService(db.get_session())
    
    # create a test user
    user = auth.register("John", "Doe", "john@example.com", "1234567890", "Test123", Role.MEMBER)
    
    # add a test vehicle
    vehicle = vehicle_service.add_vehicle(
        "ABC123", "Toyota Camry", VehicleType.SEDAN, 2020, 50000, 100000, 2, 72, 500
    )
    
    # create a booking for 4 hours in the future
    start_at = datetime.utcnow() + timedelta(days=1)
    end_at = start_at + timedelta(hours=4)
    booking = rental_service.create_booking(user.id, vehicle.id, start_at, end_at)
    
    # check if the initial rental cost is calculated correctly
    assert booking.initial_rental_cents == 4 * 500

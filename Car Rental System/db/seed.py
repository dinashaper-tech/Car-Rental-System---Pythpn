from src.database import Database
from src.models import User, Vehicle, Role, VehicleType
import bcrypt
from datetime import datetime

def seed_database(db: Database):
    session = db.get_session()
    
    # Seed admin user if not already in database
    admin = session.query(User).filter(User.email == "dinashaper@gmail.com").first()
    if not admin:
        hashed = bcrypt.hashpw("Abc546&".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")  # hash the password
        admin = User(
            first_name="Admin",
            last_name="User",
            email="dinashaper@gmail.com",
            mobile_number="1234567890",
            password_hash=hashed,
            role=Role.ADMIN
        )
        session.add(admin)

    # Seed some vehicles if they don't exist
    vehicles = [
        Vehicle(plate="ABC123", model="Toyota Camry", type=VehicleType.SEDAN, year=2020, vehicle_mileage=50000,
                mileage_threshold=100000, min_rent_hours=2, max_rent_hours=72, hourly_rate_cents=500),
        Vehicle(plate="XYZ789", model="Honda CR-V", type=VehicleType.SUV, year=2021, vehicle_mileage=30000,
                mileage_threshold=80000, min_rent_hours=4, max_rent_hours=48, hourly_rate_cents=700)
    ]
    for v in vehicles:
        if not session.query(Vehicle).filter(Vehicle.plate == v.plate).first():
            session.add(v)
    
    # commit all seeded data
    session.commit()

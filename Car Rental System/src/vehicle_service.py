from sqlalchemy.orm import Session
from src.models import Vehicle, VehicleType
from datetime import datetime
from typing import List, Optional

class VehicleService:
    def __init__(self, db: Session):
        self.db = db  
        
    def add_vehicle(self, plate: str, model: str, type: VehicleType, year: int, vehicle_mileage: float,
                    mileage_threshold: float, min_rent_hours: int, max_rent_hours: int, hourly_rate_cents: int,
                    photo_url: Optional[str] = None) -> Vehicle:
        # avoid duplicate plates
        if self.db.query(Vehicle).filter(Vehicle.plate == plate).first():
            raise ValueError("Vehicle plate already exists.")

        vehicle = Vehicle(
            plate=plate, model=model, type=type, year=year, vehicle_mileage=vehicle_mileage,
            mileage_threshold=mileage_threshold, min_rent_hours=min_rent_hours, max_rent_hours=max_rent_hours,
            hourly_rate_cents=hourly_rate_cents, photo_url=photo_url
        )

        self.db.add(vehicle)
        self.db.commit()
        return vehicle

    def update_vehicle(self, plate: str, **kwargs) -> Vehicle:
        # only update active (not deleted) vehicles
        vehicle = self.db.query(Vehicle).filter(Vehicle.plate == plate, Vehicle.is_deleted == False).first()
        if not vehicle:
            raise ValueError("Vehicle not found or deleted.")

        # update given fields
        for key, value in kwargs.items():
            setattr(vehicle, key, value)

        vehicle.updated_at = datetime.utcnow()
        self.db.commit()
        return vehicle

    def delete_vehicle(self, plate: str) -> None:
        from src.rental_service import RentalService  # local import to avoid circular dependency

        vehicle = self.db.query(Vehicle).filter(Vehicle.plate == plate, Vehicle.is_deleted == False).first()
        if not vehicle:
            raise ValueError("Vehicle not found or already deleted.")

        rental_service = RentalService(self.db)
        # don’t allow deleting vehicles with active bookings
        if rental_service.has_active_bookings(vehicle.id):
            raise ValueError("Cannot delete vehicle with active or pending bookings.")

        # soft delete
        vehicle.is_deleted = True
        vehicle.updated_at = datetime.utcnow()
        self.db.commit()

    def get_available_vehicles(self, vehicle_type: VehicleType, start_at: datetime, end_at: datetime) -> List[Vehicle]:
        from src.rental_service import RentalService

        # ask rental service for vehicles free in the given time range
        rental_service = RentalService(self.db)
        return rental_service.search_available_vehicles(vehicle_type, start_at, end_at)

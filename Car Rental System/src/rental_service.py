from sqlalchemy.orm import Session
from src.models import Rental, Vehicle, ApprovalStatus, BookingStatus, PaymentMethod
from datetime import datetime, timedelta
from math import ceil
from typing import List, Optional

class RentalService:
    def __init__(self, db: Session):
        self.db = db  # database session

    def search_available_vehicles(self, vehicle_type: str, start_at: datetime, end_at: datetime) -> List[Vehicle]:
        # basic validation on dates
        if start_at < datetime.utcnow():
            raise ValueError("Start date/time cannot be in the past.")
        if end_at <= start_at:
            raise ValueError("End date/time must be after start date/time.")
        
        # calculate rental duration in hours
        duration_hours = ceil((end_at - start_at).total_seconds() / 3600)

        # add buffer time to avoid back-to-back overlaps
        buffer_start = start_at - timedelta(hours=6)
        buffer_end = end_at + timedelta(hours=6)

        # filter vehicles that match requirements
        vehicles = self.db.query(Vehicle).filter(
            Vehicle.type == vehicle_type,
            Vehicle.is_deleted == False,
            Vehicle.vehicle_mileage < Vehicle.mileage_threshold,
            Vehicle.min_rent_hours <= duration_hours,
            Vehicle.max_rent_hours >= duration_hours
        ).all()

        available = []
        for vehicle in vehicles:
            # check if there’s an overlapping booking
            overlapping = self.db.query(Rental).filter(
                Rental.vehicle_id == vehicle.id,
                Rental.booking_status.in_([BookingStatus.REQUESTED, BookingStatus.ACTIVE]),
                Rental.approval_status.in_([ApprovalStatus.PENDING, ApprovalStatus.APPROVED]),
                Rental.start_at < buffer_end,
                Rental.end_at > buffer_start
            ).first()
            if not overlapping:
                available.append(vehicle)
        return available

    def create_booking(self, user_id: int, vehicle_id: int, start_at: datetime, end_at: datetime) -> Rental:
        # check if vehicle exists and is not deleted
        vehicle = self.db.query(Vehicle).filter(Vehicle.id == vehicle_id, Vehicle.is_deleted == False).first()
        if not vehicle:
            raise ValueError("Vehicle not found or deleted.")

        # calculate booking duration
        duration_hours = ceil((end_at - start_at).total_seconds() / 3600)

        # make sure duration fits vehicle rental limits
        if duration_hours < vehicle.min_rent_hours or duration_hours > vehicle.max_rent_hours:
            raise ValueError("Booking duration out of vehicle rental limits.")

        # block booking if vehicle passed mileage threshold
        if vehicle.vehicle_mileage >= vehicle.mileage_threshold:
            raise ValueError("Vehicle exceeds mileage threshold.")
        
        # create new booking record
        booking = Rental(
            user_id=user_id,
            vehicle_id=vehicle_id,
            start_at=start_at,
            end_at=end_at,
            initial_rental_cents=duration_hours * vehicle.hourly_rate_cents,
            total_rental_cents=duration_hours * vehicle.hourly_rate_cents
        )
        self.db.add(booking)
        self.db.commit()
        return booking

    def cancel_booking(self, booking_id: int, cancelled_by: str, reason: str) -> None:
        # find booking to cancel
        booking = self.db.query(Rental).filter(Rental.id == booking_id).first()
        if not booking:
            raise ValueError("Booking not found.")

        # prevent cancelling finished or already cancelled bookings
        if booking.booking_status in [BookingStatus.COMPLETED, BookingStatus.CANCELLED]:
            raise ValueError("Booking already completed or cancelled.")

        # mark booking as cancelled
        booking.booking_status = BookingStatus.CANCELLED
        booking.cancelled_at = datetime.utcnow()
        booking.cancelled_by = cancelled_by
        booking.cancelled_reason = reason
        self.db.commit()

    def has_active_bookings(self, vehicle_id: int) -> bool:
        # check if this vehicle has any ongoing or pending bookings
        return self.db.query(Rental).filter(
            Rental.vehicle_id == vehicle_id,
            Rental.booking_status.in_([BookingStatus.REQUESTED, BookingStatus.ACTIVE]),
            Rental.approval_status.in_([ApprovalStatus.PENDING, ApprovalStatus.APPROVED])
        ).first() is not None

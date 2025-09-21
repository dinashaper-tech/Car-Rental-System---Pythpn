from sqlalchemy.orm import Session
from src.models import Rental, Vehicle, Role, ApprovalStatus, BookingStatus
from src.auth_service import AuthService
from datetime import datetime

class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.auth_service = AuthService(db)  # reuse AuthService for admin creation

    def create_admin(self, first_name: str, last_name: str, email: str, mobile_number: str, password: str):
        # create a new admin user
        return self.auth_service.register(first_name, last_name, email, mobile_number, password, role=Role.ADMIN)

    def review_booking(self, booking_id: int, approve: bool, reason: str = None):
        # approve or reject a booking
        booking = self.db.query(Rental).filter(Rental.id == booking_id).first()
        if not booking:
            raise ValueError("Booking not found.")
        if booking.approval_status != ApprovalStatus.PENDING:  
            raise ValueError("Booking is not pending approval.")
        booking.approval_status = ApprovalStatus.APPROVED if approve else ApprovalStatus.REJECTED  
        booking.reject_reason = reason
        self.db.commit()

    def issue_vehicle(self, booking_id: int):
        # mark a booking as issued
        booking = self.db.query(Rental).filter(Rental.id == booking_id).first()
        if not booking:
            raise ValueError("Booking not found.")
        if booking.approval_status != ApprovalStatus.APPROVED:  
            raise ValueError("Booking not approved.")
        if booking.booking_status != BookingStatus.REQUESTED:  
            raise ValueError("Booking is not in REQUESTED status.")
        booking.booking_status = BookingStatus.ACTIVE  
        booking.issued_at = datetime.utcnow()  
        self.db.commit()

    def return_vehicle(self, booking_id: int, ending_mileage: float, surcharge_cents: int, comment: str, payment_method: str):
        # complete a booking and update vehicle info
        booking = self.db.query(Rental).filter(Rental.id == booking_id).first()
        if not booking:
            raise ValueError("Booking not found.")
        if booking.booking_status != BookingStatus.ACTIVE:  
            raise ValueError("Booking is not active.")
        vehicle = self.db.query(Vehicle).filter(Vehicle.id == booking.vehicle_id).first()
        booking.booking_status = BookingStatus.COMPLETED
        booking.ending_mileage = ending_mileage
        booking.surcharge_cents = surcharge_cents  
        booking.total_rental_cents = booking.initial_rental_cents + surcharge_cents  
        booking.payment_method = payment_method
        booking.completed_at = datetime.utcnow()  
        booking.paid_at = datetime.utcnow()  
        vehicle.vehicle_mileage = ending_mileage  # update vehicle mileage
        self.db.commit()

    def get_no_show_bookings(self):
        # get bookings that were approved but never started (no-shows)
        now = datetime.utcnow()
        return self.db.query(Rental).filter(
            Rental.approval_status == ApprovalStatus.APPROVED, 
            Rental.booking_status == BookingStatus.REQUESTED,   
            Rental.start_at < now
        ).all()

    def get_vehicles_over_mileage(self):
        # get vehicles that exceeded mileage threshold
        return self.db.query(Vehicle).filter(Vehicle.vehicle_mileage >= Vehicle.mileage_threshold).all()

    def get_cancelled_bookings(self):
        # get all cancelled bookings
        return self.db.query(Rental).filter(Rental.booking_status == BookingStatus.CANCELLED).all() 

    def get_all_vehicles(self):
        # fetch all vehicles
        return self.db.query(Vehicle).all()
from datetime import datetime 
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
import re

Base = declarative_base()

# roles for system users
class Role(Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

# different types of vehicles
class VehicleType(Enum):
    SEDAN = "SEDAN"
    SUV = "SUV"
    VAN = "VAN"
    HATCHBACK = "HATCHBACK"
    TRUCK = "TRUCK"

# approval workflow for rental requests
class ApprovalStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

# status of a booking
class BookingStatus(Enum):
    REQUESTED = "REQUESTED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

# available payment methods
class PaymentMethod(Enum):
    CARD = "CARD"
    CASH = "CASH"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mobile_number = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(SQLEnum(Role), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # validate email format before saving
    @validates("email")
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    # make sure mobile number is 10 digits
    @validates("mobile_number")
    def validate_mobile_number(self, key, mobile):
        if not re.match(r"^\d{10}$", mobile):
            raise ValueError("Mobile number must be 10 digits")
        return mobile

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True)
    plate = Column(String, unique=True, nullable=False)  # unique vehicle plate
    model = Column(String, nullable=False)
    type = Column(SQLEnum(VehicleType), nullable=False)
    year = Column(Integer, nullable=False)
    vehicle_mileage = Column(Float, nullable=False)  # current mileage
    mileage_threshold = Column(Float, nullable=False)  # max mileage before service
    min_rent_hours = Column(Integer, nullable=False)
    max_rent_hours = Column(Integer, nullable=False)
    hourly_rate_cents = Column(Integer, nullable=False)  # rental price per hour
    photo_url = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False)  # soft delete 
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Rental(Base):
    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    approval_status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING)
    booking_status = Column(SQLEnum(BookingStatus), default=BookingStatus.REQUESTED)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=True)
    initial_rental_cents = Column(Integer, nullable=False)  # base rental cost
    surcharge_cents = Column(Integer, default=0)  # extra charges
    total_rental_cents = Column(Integer, nullable=False)
    ending_mileage = Column(Float, nullable=True)  # mileage when returned
    cancelled_at = Column(DateTime, nullable=True)
    cancelled_reason = Column(String, nullable=True)
    cancelled_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    issued_at = Column(DateTime, nullable=True)  # when approved
    completed_at = Column(DateTime, nullable=True)  # when rental finished
    paid_at = Column(DateTime, nullable=True)  # when payment done

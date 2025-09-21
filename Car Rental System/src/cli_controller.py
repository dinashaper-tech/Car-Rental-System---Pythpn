from sqlalchemy.orm import Session
from src.auth_service import AuthService
from src.vehicle_service import VehicleService
from src.rental_service import RentalService
from src.admin_service import AdminService
from src.models import Role, VehicleType, PaymentMethod, Vehicle, Rental
from datetime import datetime
from math import ceil
from dateutil.parser import parse
from tabulate import tabulate


class CLIController:
    def __init__(self, db: Session):
        # setup database session and services
        self.db = db.get_session()
        self.auth_service = AuthService(self.db)
        self.vehicle_service = VehicleService(self.db)
        self.rental_service = RentalService(self.db)
        self.admin_service = AdminService(self.db)
        self.current_user = None  # store the logged-in user

    def run(self):
        # entry point of the CLI
        while True:
            if not self.current_user:  # no user logged in
                print("\nWelcome to the DINA Car Rental System! \n1. Login\n2. Register \n3. Exit")
                choice = input("Select an option: ")
                if choice == "1":
                    self.login()
                elif choice == "2":
                    self.register()
                elif choice == "3":
                    break
                else:
                    print("Invalid option.")
            else:  # user logged in
                if self.current_user.role == Role.ADMIN:
                    self.admin_menu()
                else:
                    self.customer_menu()

    def login(self):
        # login flow
        try:
            email = input("Email: ")
            password = input("Password: ")
            self.current_user = self.auth_service.login(email, password)
            print(f"Welcome, {self.current_user.first_name}!")
        except ValueError as e:
            print(f"Error: {e}")

    def register(self):
        # register flow
        try:
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("Email: ")
            mobile_number = input("Mobile Number (10 digits): ")
            password = input("Password: ")
            self.auth_service.register(first_name, last_name, email, mobile_number, password)
            print("Registration successful. Please login.")
        except ValueError as e:
            print(f"Error: {e}")

    def customer_menu(self):
        # menu shown to customers
        while True:
            print("\nCustomer Menu:")
            print("1. Search Vehicles\n2. Book Vehicle\n3. Cancel Booking\n4. View my Bookings\n5. Logout")
            choice = input("Select an option: ")
            try:
                if choice == "1":
                    self.search_vehicles()
                elif choice == "2":
                    self.book_vehicle()
                elif choice == "3":
                    self.cancel_booking()
                elif choice == "4":
                    self.view_user_bookings()
                elif choice == "5":
                    self.current_user = None
                    break
                else:
                    print("Invalid option.")
            except ValueError as e:
                print(f"Error: {e}")

    def admin_menu(self):
        # menu shown to admins
        while True:
            print("\nAdmin Menu:")
            print("1. Add Vehicle\n2. Update Vehicle\n3. Delete Vehicle\n4. Review Booking\n5. Issue Vehicle\n6. Return Vehicle\n7. Cancel No-Show\n8. View All Bookings\n9. View Vehicles Over Mileage\n10. View Cancelled Bookings Report\n11. Create Admin\n12. View All Vehicles\n13. Logout")
            choice = input("Select an option: ")
            try:
                if choice == "1":
                    self.add_vehicle()
                elif choice == "2":
                    self.update_vehicle()
                elif choice == "3":
                    self.delete_vehicle()
                elif choice == "4":
                    self.review_booking()
                elif choice == "5":
                    self.issue_vehicle()
                elif choice == "6":
                    self.return_vehicle()
                elif choice == "7":
                    self.cancel_noshow()
                elif choice == "8":
                    self.view_bookings()
                elif choice == "9":
                    self.view_vehicles_over_mileage()
                elif choice == "10":
                    self.view_cancelled_report()
                elif choice == "11":
                    self.create_admin()
                elif choice == "12":
                    self.view_all_vehicles()
                elif choice == "13":
                    self.current_user = None
                    break
                else:
                    print("Invalid option.")
            except ValueError as e:
                print(f"Error: {e}")

    def search_vehicles(self):
        # customers search available vehicles
        vehicle_type = input("Vehicle Type (SEDAN, SUV, VAN, HATCHBACK, TRUCK): ").upper()
        start_at = parse(input("Start Date (YYYY-MM-DD HH:MM): "))
        end_at = parse(input("End Date (YYYY-MM-DD HH:MM): "))
        vehicles = self.rental_service.search_available_vehicles(VehicleType[vehicle_type], start_at, end_at)
        
        table = []
        for v in vehicles:
            duration_hours = ceil((end_at - start_at).total_seconds() / 3600)
            cost = duration_hours * v.hourly_rate_cents
            table.append([v.id, v.plate, v.model, f"${cost/100:.2f}"])
        print(tabulate(table, headers=["ID", "Plate", "Model", "Estimated Cost"], tablefmt="grid"))

    def book_vehicle(self):
        # create a booking
        vehicle_id = int(input("Vehicle ID: "))
        start_at = parse(input("Start Date (YYYY-MM-DD HH:MM): "))
        end_at = parse(input("End Date (YYYY-MM-DD HH:MM): "))
        vehicle = self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        duration_hours = ceil((end_at - start_at).total_seconds() / 3600)
        cost = duration_hours * vehicle.hourly_rate_cents
        print(f"Estimated Cost: ${cost/100:.2f}")
        confirm = input("Confirm booking? (y/n): ")
        if confirm.lower() == "y":
            booking = self.rental_service.create_booking(self.current_user.id, vehicle_id, start_at, end_at)
            print(f"Booking created with ID: {booking.id}")
        else:
            print("Booking not confirmed.")

    def cancel_booking(self):
        # customer cancels a booking
        booking_id = int(input("Booking ID: "))
        reason = input("Cancellation Reason: ")
        self.rental_service.cancel_booking(booking_id, "CUSTOMER", reason)
        print("Booking cancelled.")

    def view_user_bookings(self):
        # show all bookings for current user
        bookings = self.db.query(Rental).filter(Rental.user_id == self.current_user.id).all()
        if not bookings:
            print("No bookings found.")
            return
        table = []
        for b in bookings:
            vehicle = self.db.query(Vehicle).filter(Vehicle.id == b.vehicle_id).first()
            table.append([b.id, vehicle.plate, vehicle.model, b.start_at, b.end_at,
                          b.booking_status.value, b.approval_status.value, f"${b.total_rental_cents/100:.2f}"])
        print(tabulate(table, headers=["Booking ID", "Plate", "Model", "Start", "End",
                                       "Status", "Approval", "Total Cost"], tablefmt="grid"))

    def add_vehicle(self):
        # admin adds a vehicle
        plate = input("Plate: ")
        model = input("Model: ")
        type = VehicleType[input("Type (SEDAN, SUV, VAN, HATCHBACK, TRUCK): ").upper()]
        year = int(input("Year: "))
        vehicle_mileage = float(input("Mileage: "))
        mileage_threshold = float(input("Mileage Threshold: "))
        min_rent_hours = int(input("Min Rent Hours: "))
        max_rent_hours = int(input("Max Rent Hours: "))
        hourly_rate_cents = int(input("Hourly Rate (cents): "))
        photo_url = input("Photo URL (optional): ") or None
        self.vehicle_service.add_vehicle(plate, model, type, year, vehicle_mileage, mileage_threshold,
                                        min_rent_hours, max_rent_hours, hourly_rate_cents, photo_url)
        print("Vehicle added.")

    def update_vehicle(self):
        # admin updates vehicle details
        plate = input("Plate: ")
        fields = {"model": input("Model (leave blank to keep unchanged): ") or None,
                  "vehicle_mileage": float(input("Mileage (leave blank to keep unchanged): ") or 0) or None,
                  "mileage_threshold": float(input("Mileage Threshold (leave blank to keep unchanged): ") or 0) or None}
        fields = {k: v for k, v in fields.items() if v is not None}
        self.vehicle_service.update_vehicle(plate, **fields)
        print("Vehicle updated.")

    def delete_vehicle(self):
        # admin deletes a vehicle
        plate = input("Plate: ")
        self.vehicle_service.delete_vehicle(plate)
        print("Vehicle deleted.")

    def review_booking(self):
        # admin approves or rejects a booking
        booking_id = int(input("Booking ID: "))
        approve = input("Approve? (y/n): ").lower() == "y"
        reason = input("Reason (if rejecting): ") if not approve else None
        self.admin_service.review_booking(booking_id, approve, reason)
        print("Booking reviewed.")

    def issue_vehicle(self):
        # admin issues vehicle for a booking
        booking_id = int(input("Booking ID: "))
        booking = self.db.query(Rental).filter(Rental.id == booking_id).first()
        vehicle = self.db.query(Vehicle).filter(Vehicle.id == booking.vehicle_id).first()
        print(f"Booking: {booking.id}, Vehicle: {vehicle.plate}, Start: {booking.start_at}, End: {booking.end_at}")
        confirm = input("Confirm issue? (y/n): ")
        if confirm.lower() == "y":
            self.admin_service.issue_vehicle(booking_id)
            print("Vehicle issued.")

    def return_vehicle(self):
        # admin handles vehicle return
        booking_id = int(input("Booking ID: "))
        ending_mileage = float(input("Ending Mileage: "))
        surcharge_cents = int(input("Surcharge (cents): "))
        comment = input("Comment: ")
        payment_method = PaymentMethod[input("Payment Method (CARD, CASH): ").upper()]
        self.admin_service.return_vehicle(booking_id, ending_mileage, surcharge_cents, comment, payment_method)
        print("Vehicle returned.")

    def cancel_noshow(self):
        # admin cancels no-show bookings
        bookings = self.admin_service.get_no_show_bookings()
        table = []
        for b in bookings:
            vehicle = self.db.query(Vehicle).filter(Vehicle.id == b.vehicle_id).first()
            table.append([b.id, vehicle.plate, b.start_at])
            print(tabulate(table, headers=["Booking ID", "Plate", "Start"], tablefmt="grid"))
        booking_id = int(input("Booking ID to cancel: "))
        reason = input("Cancellation Reason: ")
        self.rental_service.cancel_booking(booking_id, "ADMIN", reason)
        print("No-show booking cancelled.")

    def view_bookings(self):
        # admin views all bookings
        bookings = self.db.query(Rental).all()
        table = []
        for b in bookings:
            vehicle = self.db.query(Vehicle).filter(Vehicle.id == b.vehicle_id).first()
            table.append([b.id, vehicle.plate, b.booking_status.value, b.approval_status.value])
        print(tabulate(table, headers=["Booking ID", "Plate", "Status", "Approval"], tablefmt="grid"))

    def view_vehicles_over_mileage(self):
        # admin views vehicles that crossed mileage threshold
        vehicles = self.admin_service.get_vehicles_over_mileage()
        table = []
        for v in vehicles:
             table.append([v.plate, v.model, v.vehicle_mileage, v.mileage_threshold])
        print(tabulate(table, headers=["Plate", "Model", "Mileage", "Threshold"], tablefmt="grid"))


    def view_cancelled_report(self):
        # admin views cancelled bookings report
        bookings = self.admin_service.get_cancelled_bookings()
        table = []
        for b in bookings:
            vehicle = self.db.query(Vehicle).filter(Vehicle.id == b.vehicle_id).first()
            table.append([b.id, vehicle.plate, b.cancelled_by, b.cancelled_reason])
        print(tabulate(table, headers=["Booking ID", "Plate", "Cancelled By", "Reason"], tablefmt="grid"))

    def create_admin(self):
        # create a new admin user
        try:
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("Email: ")
            mobile_number = input("Mobile Number (10 digits): ")
            password = input("Password: ")
            self.admin_service.create_admin(first_name, last_name, email, mobile_number, password)
            print("Admin created successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def view_all_vehicles(self):
        # admin views all vehicles
        vehicles = self.admin_service.get_all_vehicles()
        if not vehicles:
            print("No vehicles found.")
            return
        table = []
        for v in vehicles:
            status = "Deleted" if v.is_deleted else "Active"
            table.append([v.id, v.plate, v.model, v.type.name, v.vehicle_mileage, status])
        print(tabulate(table, headers=["ID", "Plate", "Model", "Type", "Mileage", "Status"], tablefmt="grid"))
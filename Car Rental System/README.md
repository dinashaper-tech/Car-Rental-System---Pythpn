Welcome to the DINA Car Rental System! 

The Car Rental System is command-line-based app built with Python and SQLAlchemy, making it easy to manage vehicle rentals. Customers can browse and book cars, while admins handle everything from adding new vehicles to processing bookings. It’s all backed by a SQLite database, so data stays safe and organized.

Users - Customer and Admin

As a Customer: 
1. Register
2. Log in
3. Search for available vehicles
4. Book vehicle
5. Cancel booking 
6. View my Bookings
{
example: 
Email - dinashaperera995@gmail.com
Password - Dina123()
}


As an Admin: 
1. Add vehicle
2. Update vehicle
3. Delete vehicle
4. Review bookings (approve or reject customer booking request)
5. Issue vehicles (update when booking vehice is issued)
6. Return vehicle (update when booking vehice is returned)
7. Cancel No-Show (when a customer not come to pick the booked vehicle, cancel the booking)
8. View All bookkings 
9. View vehicles over mileage (when a vehicle reaches its service mileage threshold, it will be reflected here)
10. View Cancel bookings report ( admin can get an idea on cancelled bookings)
11. Create admin (admin can create another admin account)
12. View all vehicles
13. Logout
14. Log in
{
example:
Email: dinashaper@gmail.com
Password: Abc546&
}


Behind the Scenes: A tidy SQLite database keeps track of users, roles, vehicles, and rentals, with a straightforward CLI to tie it all together.

Requirements : 
Computer
Python: Version 3.13 
Operating System: Works on Windows, macOS, or Linux.
Dependencies: All listed in requirements.txt 

Steps to follow :
Download the project ZIP or clone the repository computer.
Jump into the Project Folder:Open terminal or command prompt.
1. navigate to the project directory:
   cd path/to/dina_car_rental_system

2. Set Up a Virtual Environment
   python -m venv venv

3. Activate the Virtual Environment:
   On Windows:.\venv\Scripts\activate

4. Install all required packages with:
   pip install -r requirements.txt

5. Set Up the Database:Create the SQLite database (db/car_rental.db) and add starter data ( admin role and sample cars):
   python start.py init-db

6. Launch the App:
   python start.py run

Use the Car Rental System
Once run python start.py run, it comes welcoming main menu:
Welcome to the DINA Car Rental System
1. Login
2. Register
3. Exit

Type the number of your choice (e.g., 1 to log in) and hit Enter. 

***For New Customers: Can regisetr: Pick option 2, enter an email (e.g., dina@gmail.com) and a password (like Abc546&).

***For existing customer can Log In: Choose option 1, enter your email and password.
Customer Menu:Customer Menu
1. Search Vehicles
2. Book Vehicle
3. View My Bookings
4. Logout


-->Search Vehicles: Type a vehicle type (e.g., SUV) and a date range (like 2025-09-10 10:00 to 2025-09-11 10:00) to see what’s available.
-->Book a Vehicle: Enter a vehicle ID from the search, your rental dates, and confirm. You’ll get a booking ID, and the status will be REQUESTED.
-->View My Bookings: Check out all your bookings, including status and details.
Logout: Back to the main menu.

***For Admins:
Log In: Use option 1 with admin credentials (e.g., Email: dinashaper@gmail.com , Password: Abc546&).
Admin Menu:Admin Menu
1. Add Vehicle : 
2. Update Vehicle
3. Delete Vehicle
4. Review Booking
5. Issue Vehicle
6. Return Vehicle
7. Create Admin
8. View All Bookings
9. Search Vehicles
10. Book Vehicle
11. View My Bookings
12. View All Vehicles
13. Logout

Feture Explanation: 
Update Vehicle: Provide the plate and new details (e.g., mileage=15000).
Delete Vehicle: Enter the plate to mark it as deleted (it stays in the database since soft delete but won’t show as available or not eligible for bookings).
Review Booking: Approve or reject customer bookings.
Issue Vehicle: Enter a booking ID to mark it as ISSUED.
Return Vehicle: Provide booking ID, ending mileage, surcharge, comments, and payment method to mark it as COMPLETED.
View All Bookings : See all bookings in the system.
View All Vehicles: See all vehicles in the system.
Create Admin: Add another admin user.
Logout: Back to the main menu.

Exit the App: Choose option 3 (main menu), 13 (admin menu), or 4 (customer menu) to quit.


Project’s files:
car_rental_system/
├── README.md              # Explains how to use and understand the system.
├── requirements.txt       # Lists all the Python packages need 
├── start.py               # The starting point—run this to set up the database and launch the app.
├── src/
│   ├── __init__.py        # src/ is a package
│   ├── models.py          # Defines the database tables (Users, Roles, Vehicles, Rentals).
│   ├── database.py        # Sets up the SQLite database connection.
│   ├── auth_service.py    # Handles user sign-up and login magic.
│   ├── vehicle_service.py # Manages adding, updating, deleting, and searching vehicles.
│   ├── rental_service.py  # Booking creation and searching.
│   ├── admin_service.py   # Admin tasks. eg: issuing vehicles and creating admins.
│   ├── cli_controller.py  # The CLI brain handles menus and user inputs.
│   ├── utils.py           # Functions (e.g., password hashing, date checking).
├── db/
│   ├── __init__.py        # db/ as a package.
│   ├── seed.py            # Adds starter data (roles and sample cars) to the database.
├── tests/
│   ├── __init__.py        # tests/ as a package.
│   ├── test_auth.py       # Tests for login and registration.
│   ├── test_vehicle.py    # Tests for vehicle operations.
│   ├── test_rental.py     # Tests for booking operations.
├── ARCHITECTURE.md        # UML diagrams (use case, sequence, activity, ER ) 
├── MAINTENANCE.md         # Tips for developers.
├── CHANGELOG.md           # Tracks updates and changes to the project.



Tests
These tests check authentication (test_auth.py), vehicle operations (test_vehicle.py), and bookings (test_rental.py).
Need to activate the virtual environment and install dependencies.


Database Setup:
If python start.py init-db fails, need to chek whether its having write permissions in the db/ folder or delete any old db/car_rental.db file.


Input Glitches:
Messy date formats (e.g., 2025-13-01) can trip things up. Stick to YYYY-MM-DD HH:MM (e.g., 2025-09-10 10:00).
Duplicate plates or invalid vehicle types (not SEDAN, SUV, etc.) will show error messages—follow the prompts.


Python Version:
Python 3.13 with SQLAlchemy 2.0.35. .


Soft Deletion:
Deleted vehicles (is_deleted=True).


Database Problems:
If init-db fails, delete db/car_rental.db and try again:python start.py init-db



## License

This Car Rental System was created by **Liyanage Dinasha Lahirunee Perera**.  

You are free to use, modify, distribute, and adapt this project in any form, 
for personal, academic, or commercial purposes, without restriction.  

No warranty is provided.

## Known Issues

Currently, there are no known bugs or issues.  
If you encounter any unexpected behavior, please report it or submit a pull request.


## Credits

This Car Rental System is developed by **Liyanage Dinasha Lahirunee Perera** as an assignment for the **Yoobee College of Creative Innovation – Master of Software Engineering Program**, **Professional Software Engineering** module.  

I would like to express my sincere gratitude and appreciation to **Sir Mohammad Norouzifard** for his guidance, support, and teaching, which helped make this project a success.

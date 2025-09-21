# Architecture

## Overview
The Car Rental System is a Python CLI application built with a modular, object-oriented design. It follows the Service-Repository pattern with a Singleton database connection for efficiency and consistency.

## Components
- **Models (models.py)**: SQLAlchemy ORM models for User, Vehicle, and Rental, with validation logic.
- **Database (database.py)**: Singleton SQLite connection with session management.
- **AuthService (auth_service.py)**: Handles user registration, login, and password hashing with bcrypt.
- **VehicleService (vehicle_service.py)**: Manages vehicle CRUD operations with soft-delete support.
- **RentalService (rental_service.py)**: Handles booking lifecycle, availability checks, and cost calculations.
- **AdminService (admin_service.py)**: Admin-specific operations like booking approval, vehicle issuance, and reports.
- **CLIController (cli_controller.py)**: Manages user interaction, input validation, and menu navigation.
- **Utils (utils.py)**: Shared utilities for validation and formatting.

## Design Patterns
- **Singleton**: Ensures a single database connection.
- **Service/Repository**: Separates business logic (services) from data access (SQLAlchemy).
- **Command Pattern**: CLIController encapsulates user commands.

[CLIController]
|
v
[AuthService] <-> [Database] <-> [Models]
[VehicleService] <-> [Database]
[RentalService] <-> [Database]
[AdminService] <-> [Database]


## Indexing
- Users: Index on `email` for fast lookup.
- Vehicles: Index on `plate` for uniqueness checks.
- Rentals: Indexes on `vehicle_id`, `start_at`, `end_at` for efficient availability queries.
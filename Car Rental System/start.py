import sys
from src.cli_controller import CLIController
from src.database import Database
from db.seed import seed_database

def main():
    db = Database()
    if len(sys.argv) > 1 and sys.argv[1] == "init-db":
        seed_database(db)
        print("Database initialized and seeded successfully.")
        return
    controller = CLIController(db)
    controller.run()

if __name__ == "__main__":
    main()
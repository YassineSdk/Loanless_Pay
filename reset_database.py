"""
Database Reset Script for Loanless Pay
This script will clear all existing data and reinitialize the database with fresh tables.
"""

from app import app, db
from models import User, Loan
import os


def reset_database():
    """
    Delete the existing database file and create fresh tables.
    WARNING: This will permanently delete all data!
    """

    with app.app_context():
        print("=" * 60)
        print("DATABASE RESET SCRIPT")
        print("=" * 60)
        print("\nWARNING: This will delete ALL data in the database!")
        print("This includes:")
        print("  - All user accounts")
        print("  - All loan applications")
        print("  - All uploaded documents")
        print("=" * 60)

        # Ask for confirmation
        confirm = input("\nType 'YES' to confirm database reset: ")

        if confirm != "YES":
            print("\n❌ Database reset cancelled.")
            return

        print("\n🔄 Starting database reset...")

        # Step 1: Drop all tables
        print("  → Dropping all existing tables...")
        db.drop_all()
        print("  ✓ Tables dropped")

        # Step 2: Create fresh tables
        print("  → Creating fresh tables...")
        db.create_all()
        print("  ✓ Tables created")

        # Step 3: Optional - Create a default admin user
        create_admin = input("\nCreate a default admin user? (yes/no): ").lower()

        if create_admin == "yes":
            from werkzeug.security import generate_password_hash

            admin_email = input("Enter admin email: ").strip()
            admin_password = input("Enter admin password: ").strip()
            admin_name = input("Enter admin name: ").strip()

            if admin_email and admin_password and admin_name:
                admin_user = User(
                    username=admin_name,
                    email=admin_email,
                    is_admin=True,
                )
                admin_user.set_password(admin_password)
                db.session.add(admin_user)
                db.session.commit()
                print(f"  ✓ Admin user created: {admin_email}")
            else:
                print("  ⚠ Admin creation skipped (missing information)")

        print("\n" + "=" * 60)
        print("✅ Database reset complete!")
        print("=" * 60)
        print("\nYour database is now clean with fresh tables.")
        print("You can start the application with: python app.py")
        print("=" * 60)


if __name__ == "__main__":
    reset_database()

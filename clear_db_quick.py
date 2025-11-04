"""
Quick Database Clear Script
Clears all data from the database without confirmation prompts.
Use this when you want to quickly reset during development.
"""

from app import app, db
from models import User, Loan
from werkzeug.security import generate_password_hash


def clear_database_quick():
    """Clear database and create a default admin user"""

    with app.app_context():
        print("🗑️  Clearing database...")

        # Drop all tables
        db.drop_all()
        print("  ✓ Dropped all tables")

        # Create fresh tables
        db.create_all()
        print("  ✓ Created fresh tables")

        # Create default admin user
        admin = User(
            username="admin",
            email="admin@loanless.com",
            is_admin=True,
        )
        admin.set_password("admin123")
        db.session.add(admin)

        # Create a test regular user
        test_user = User(
            username="testuser",
            email="user@test.com",
            is_admin=False,
        )
        test_user.set_password("test123")
        db.session.add(test_user)

        db.session.commit()

        print("\n✅ Database cleared and reset!")
        print("\nDefault accounts created:")
        print("  Admin: username='admin' password='admin123'")
        print("  User:  username='testuser' password='test123'")
        print("\n⚡ You can now run the app: python app.py")


if __name__ == "__main__":
    clear_database_quick()

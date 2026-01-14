"""
Database Migration Script for Funding Partner Features
Adds new columns to existing database without losing data
"""

from app import app, db
from models import User, FundingTransaction, FundingUsage
import sqlite3
import os

def migrate_database():
    """Add new columns to existing database"""

    database_path = os.path.join('instance', 'database.db')

    if not os.path.exists(database_path):
        print("No existing database found. Creating fresh database...")
        with app.app_context():
            db.create_all()
            print("✅ Fresh database created successfully!")
        return

    print("📦 Existing database found. Starting migration...")

    # Connect directly to SQLite
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Check if user_role column exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    print(f"Current columns in users table: {columns}")

    try:
        # Add user_role column if it doesn't exist
        if 'user_role' not in columns:
            print("Adding user_role column...")
            cursor.execute("ALTER TABLE users ADD COLUMN user_role VARCHAR(20) DEFAULT 'client'")
            cursor.execute("UPDATE users SET user_role = 'client' WHERE user_role IS NULL")
            cursor.execute("UPDATE users SET user_role = 'admin' WHERE is_admin = 1")
            print("✅ user_role column added")
        else:
            print("✓ user_role column already exists")

        # Add company_name column if it doesn't exist
        if 'company_name' not in columns:
            print("Adding company_name column...")
            cursor.execute("ALTER TABLE users ADD COLUMN company_name VARCHAR(200)")
            print("✅ company_name column added")
        else:
            print("✓ company_name column already exists")

        # Add company_registration column if it doesn't exist
        if 'company_registration' not in columns:
            print("Adding company_registration column...")
            cursor.execute("ALTER TABLE users ADD COLUMN company_registration VARCHAR(100)")
            print("✅ company_registration column added")
        else:
            print("✓ company_registration column already exists")

        # Add initial_funding column if it doesn't exist
        if 'initial_funding' not in columns:
            print("Adding initial_funding column...")
            cursor.execute("ALTER TABLE users ADD COLUMN initial_funding FLOAT DEFAULT 0.0")
            print("✅ initial_funding column added")
        else:
            print("✓ initial_funding column already exists")

        conn.commit()
        print("\n✅ Users table migration completed!")

    except Exception as e:
        print(f"❌ Error during users table migration: {e}")
        conn.rollback()
        conn.close()
        return False

    # Create new tables if they don't exist
    try:
        # Check if funding_transactions table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='funding_transactions'")
        if not cursor.fetchone():
            print("\nCreating funding_transactions table...")
            cursor.execute("""
                CREATE TABLE funding_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    funder_id INTEGER NOT NULL,
                    amount FLOAT NOT NULL,
                    transaction_type VARCHAR(20) DEFAULT 'deposit',
                    status VARCHAR(20) DEFAULT 'completed',
                    notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    processed_by INTEGER,
                    FOREIGN KEY (funder_id) REFERENCES users(id)
                )
            """)
            print("✅ funding_transactions table created")
        else:
            print("✓ funding_transactions table already exists")

        # Check if funding_usage table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='funding_usage'")
        if not cursor.fetchone():
            print("Creating funding_usage table...")
            cursor.execute("""
                CREATE TABLE funding_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    loan_id INTEGER NOT NULL,
                    amount_used FLOAT NOT NULL,
                    usage_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'active',
                    notes TEXT,
                    FOREIGN KEY (loan_id) REFERENCES loans(id)
                )
            """)
            print("✅ funding_usage table created")
        else:
            print("✓ funding_usage table already exists")

        conn.commit()
        print("\n✅ New tables created successfully!")

    except Exception as e:
        print(f"❌ Error creating new tables: {e}")
        conn.rollback()
        conn.close()
        return False

    conn.close()

    # Now use SQLAlchemy to create demo investor account
    print("\n📝 Creating demo accounts...")
    with app.app_context():
        try:
            # Check if investor account exists
            investor = User.query.filter_by(username="investor").first()
            if not investor:
                investor = User(
                    username="investor",
                    email="investor@loanless.com",
                    user_role="funding_party",
                    company_name="Demo Investment Partners",
                    company_registration="REG-2024-001",
                    is_active=True
                )
                investor.set_password("investor123")
                db.session.add(investor)
                db.session.commit()
                print("✅ Demo investor account created (investor/investor123)")
            else:
                print("✓ Investor account already exists")

            # Ensure admin account has correct role
            admin = User.query.filter_by(username="admin").first()
            if admin:
                if admin.user_role != "admin":
                    admin.user_role = "admin"
                    db.session.commit()
                    print("✅ Admin role updated")
                else:
                    print("✓ Admin role correct")

            # Ensure demo account has correct role
            demo = User.query.filter_by(username="demo").first()
            if demo:
                if demo.user_role != "client":
                    demo.user_role = "client"
                    db.session.commit()
                    print("✅ Demo role updated")
                else:
                    print("✓ Demo role correct")

        except Exception as e:
            print(f"❌ Error creating demo accounts: {e}")
            db.session.rollback()

    print("\n" + "="*60)
    print("✅ DATABASE MIGRATION COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nYou can now run the application with:")
    print("  python app.py")
    print("\nNew login credentials:")
    print("  - Funding Partner: investor/investor123")
    print("  - Client: demo/demo123")
    print("  - Admin: admin/admin123")
    print("="*60)

    return True


if __name__ == "__main__":
    print("="*60)
    print("LOANLESS PAY - DATABASE MIGRATION")
    print("Funding Partner System")
    print("="*60)
    print()

    migrate_database()

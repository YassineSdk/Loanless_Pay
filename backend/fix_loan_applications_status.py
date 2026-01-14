"""
Database Migration: Add status column to loan_applications table
"""

import sqlite3
import os

def migrate():
    # Get database path
    db_path = os.path.join("instance", "database.db")

    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return

    print("🔄 Starting migration...")
    print(f"📂 Database: {db_path}")

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if status column exists
        cursor.execute("PRAGMA table_info(loan_applications)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'status' in columns:
            print("✅ Column 'status' already exists!")
        else:
            print("➕ Adding 'status' column...")
            cursor.execute("""
                ALTER TABLE loan_applications
                ADD COLUMN status VARCHAR(20) DEFAULT 'pending' NOT NULL
            """)
            conn.commit()
            print("✅ Column 'status' added successfully!")

        # Update existing records to have 'pending' status if NULL
        cursor.execute("""
            UPDATE loan_applications
            SET status = 'pending'
            WHERE status IS NULL
        """)
        updated = cursor.rowcount
        if updated > 0:
            conn.commit()
            print(f"✅ Updated {updated} records with default status")

        # Verify the column exists
        cursor.execute("PRAGMA table_info(loan_applications)")
        columns = cursor.fetchall()

        print("\n📋 Current loan_applications table structure:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")

        print("\n✅ Migration completed successfully!")

    except sqlite3.Error as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()

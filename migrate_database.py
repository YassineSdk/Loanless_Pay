"""
Database Migration Script
Adds missing columns to loan_applications table
"""

import os
import sqlite3
from datetime import datetime

# Database paths
DB_PATHS = [
    os.path.join(os.path.dirname(__file__), "instance", "database.db"),
    os.path.join(os.path.dirname(__file__), "backend", "instance", "database.db"),
]


def migrate_single_database(db_path):
    """Add missing columns to a single database"""

    if not os.path.exists(db_path):
        print(f"⏭️  Database not found at: {db_path}")
        return None

    print(f"📁 Database found at: {db_path}")
    print("🔄 Starting migration...\n")

    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get existing columns in loan_applications table
        cursor.execute("PRAGMA table_info(loan_applications)")
        existing_columns = [column[1] for column in cursor.fetchall()]

        print(
            f"✅ Found {len(existing_columns)} existing columns in loan_applications table"
        )

        # Columns that should exist (based on the model)
        columns_to_add = [
            ("kyc_approved_at", "DATETIME"),
            ("kyc_approved_by", "INTEGER"),
            ("kyc_notes", "TEXT"),
            ("financial_submitted_at", "DATETIME"),
            ("financial_approved_at", "DATETIME"),
            ("financial_approved_by", "INTEGER"),
            ("financial_notes", "TEXT"),
            ("decision_made_at", "DATETIME"),
            ("decision_made_by", "INTEGER"),
            ("decision_notes", "TEXT"),
        ]

        added_count = 0
        skipped_count = 0

        # Add missing columns
        for column_name, column_type in columns_to_add:
            if column_name not in existing_columns:
                try:
                    sql = f"ALTER TABLE loan_applications ADD COLUMN {column_name} {column_type}"
                    cursor.execute(sql)
                    print(f"✅ Added column: {column_name} ({column_type})")
                    added_count += 1
                except sqlite3.OperationalError as e:
                    print(f"⚠️  Could not add {column_name}: {e}")
            else:
                print(f"⏭️  Column already exists: {column_name}")
                skipped_count += 1

        # Commit changes
        conn.commit()

        print(f"\n{'=' * 60}")
        print(f"✅ Migration completed successfully!")
        print(f"   - Columns added: {added_count}")
        print(f"   - Columns skipped (already exist): {skipped_count}")
        print(f"{'=' * 60}\n")

        # Verify the changes
        cursor.execute("PRAGMA table_info(loan_applications)")
        final_columns = [column[1] for column in cursor.fetchall()]
        print(f"📊 Total columns in loan_applications table: {len(final_columns)}")

        conn.close()
        return True

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        if "conn" in locals():
            conn.rollback()
            conn.close()
        return False


def migrate_database():
    """Migrate all database files"""
    print("=" * 60)
    print("🔧 DATABASE MIGRATION SCRIPT")
    print("=" * 60)
    print()

    results = []
    for db_path in DB_PATHS:
        print(f"\n{'=' * 60}")
        print(f"Processing: {db_path}")
        print(f"{'=' * 60}\n")
        result = migrate_single_database(db_path)
        if result is not None:
            results.append((db_path, result))

    print(f"\n{'=' * 60}")
    print("📊 MIGRATION SUMMARY")
    print(f"{'=' * 60}")

    if not results:
        print("❌ No databases found to migrate!")
        return False

    for db_path, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {os.path.basename(db_path)}")

    all_success = all(success for _, success in results)

    if all_success:
        print("\n✅ All databases migrated successfully!")
        print("🔄 Please restart your application.")
    else:
        print("\n⚠️  Some migrations failed. Please check errors above.")

    print()
    return all_success


if __name__ == "__main__":
    migrate_database()

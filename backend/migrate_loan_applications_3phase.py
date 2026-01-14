"""
Migration script to add 3-phase loan application system fields
This adds Phase 1 (KYC), Phase 2 (Financial), and Phase 3 (Decision) tracking
"""

import sqlite3
import os
from datetime import datetime

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'database.db')

def migrate():
    """Add new columns for 3-phase loan application system"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Starting migration: Adding 3-phase loan application fields...")

    try:
        # Get existing columns
        cursor.execute("PRAGMA table_info(loan_applications)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        print(f"Existing columns: {existing_columns}")

        # Define new columns to add
        columns_to_add = [
            # Phase Management
            ("current_phase", "INTEGER DEFAULT 1"),
            ("overall_status", "VARCHAR(20) DEFAULT 'in_progress'"),

            # Phase 1: KYC Status
            ("kyc_status", "VARCHAR(20) DEFAULT 'pending'"),
            ("kyc_submitted_at", "DATETIME"),
            ("kyc_approved_at", "DATETIME"),
            ("kyc_approved_by", "INTEGER"),
            ("kyc_notes", "TEXT"),

            # Phase 2: Financial Status
            ("financial_status", "VARCHAR(20) DEFAULT 'not_started'"),
            ("financial_submitted_at", "DATETIME"),
            ("financial_approved_at", "DATETIME"),
            ("financial_approved_by", "INTEGER"),
            ("financial_notes", "TEXT"),

            # Phase 3: Decision Status
            ("decision_status", "VARCHAR(20) DEFAULT 'not_started'"),
            ("final_decision", "VARCHAR(20)"),
            ("decision_made_at", "DATETIME"),
            ("decision_made_by", "INTEGER"),
            ("decision_notes", "TEXT"),

            # Personal Information (Phase 1 - KYC)
            ("full_name", "VARCHAR(200)"),
            ("date_of_birth", "DATE"),
            ("nationality", "VARCHAR(100)"),
            ("phone_number", "VARCHAR(20)"),
            ("address", "TEXT"),
            ("national_id_number", "VARCHAR(50)"),
        ]

        # Add each column if it doesn't exist
        for column_name, column_type in columns_to_add:
            if column_name not in existing_columns:
                try:
                    sql = f"ALTER TABLE loan_applications ADD COLUMN {column_name} {column_type}"
                    cursor.execute(sql)
                    print(f"✓ Added column: {column_name}")
                except sqlite3.OperationalError as e:
                    print(f"✗ Could not add {column_name}: {e}")
            else:
                print(f"- Column already exists: {column_name}")

        # Make nullable fields that were previously NOT NULL
        print("\nUpdating nullable constraints...")
        nullable_fields = [
            "loan_amount_requested",
            "loan_purpose",
            "loan_duration_months",
            "monthly_income",
            "employment_status"
        ]

        for field in nullable_fields:
            if field in existing_columns:
                print(f"  Note: {field} should be nullable (requires table rebuild in SQLite)")

        # Update loan_documents table to add phase and other fields
        print("\nUpdating loan_documents table...")
        cursor.execute("PRAGMA table_info(loan_documents)")
        doc_columns = [column[1] for column in cursor.fetchall()]

        doc_columns_to_add = [
            ("phase", "INTEGER DEFAULT 1"),
        ]

        for column_name, column_type in doc_columns_to_add:
            if column_name not in doc_columns:
                try:
                    sql = f"ALTER TABLE loan_documents ADD COLUMN {column_name} {column_type}"
                    cursor.execute(sql)
                    print(f"✓ Added column to loan_documents: {column_name}")
                except sqlite3.OperationalError as e:
                    print(f"✗ Could not add {column_name} to loan_documents: {e}")
            else:
                print(f"- Column already exists in loan_documents: {column_name}")

        # Initialize existing records with sensible defaults
        print("\nInitializing existing records...")

        # Set current_phase based on status
        cursor.execute("""
            UPDATE loan_applications
            SET current_phase = CASE
                WHEN status = 'pending' THEN 1
                WHEN status = 'approved' THEN 3
                WHEN status = 'rejected' THEN 1
                WHEN status = 'active' THEN 3
                WHEN status = 'completed' THEN 3
                ELSE 1
            END
            WHERE current_phase IS NULL OR current_phase = 0
        """)
        print(f"✓ Updated current_phase for {cursor.rowcount} records")

        # Set overall_status based on status
        cursor.execute("""
            UPDATE loan_applications
            SET overall_status = CASE
                WHEN status = 'completed' THEN 'completed'
                WHEN status = 'rejected' THEN 'cancelled'
                ELSE 'in_progress'
            END
            WHERE overall_status IS NULL OR overall_status = ''
        """)
        print(f"✓ Updated overall_status for {cursor.rowcount} records")

        # Set kyc_status based on status
        cursor.execute("""
            UPDATE loan_applications
            SET kyc_status = CASE
                WHEN status IN ('approved', 'active', 'completed') THEN 'approved'
                WHEN status = 'rejected' THEN 'rejected'
                ELSE 'pending'
            END
            WHERE kyc_status IS NULL OR kyc_status = ''
        """)
        print(f"✓ Updated kyc_status for {cursor.rowcount} records")

        # Set financial_status
        cursor.execute("""
            UPDATE loan_applications
            SET financial_status = CASE
                WHEN status IN ('approved', 'active', 'completed') THEN 'approved'
                WHEN status = 'rejected' THEN 'not_started'
                ELSE 'not_started'
            END
            WHERE financial_status IS NULL OR financial_status = ''
        """)
        print(f"✓ Updated financial_status for {cursor.rowcount} records")

        # Set decision_status
        cursor.execute("""
            UPDATE loan_applications
            SET decision_status = CASE
                WHEN status IN ('approved', 'active', 'completed') THEN 'approved'
                WHEN status = 'rejected' THEN 'rejected'
                ELSE 'not_started'
            END
            WHERE decision_status IS NULL OR decision_status = ''
        """)
        print(f"✓ Updated decision_status for {cursor.rowcount} records")

        # Set final_decision
        cursor.execute("""
            UPDATE loan_applications
            SET final_decision = CASE
                WHEN status IN ('approved', 'active', 'completed') THEN 'accepted'
                WHEN status = 'rejected' THEN 'rejected'
                ELSE NULL
            END
            WHERE final_decision IS NULL OR final_decision = ''
        """)
        print(f"✓ Updated final_decision for {cursor.rowcount} records")

        # Commit changes
        conn.commit()
        print("\n✅ Migration completed successfully!")

        # Show summary
        cursor.execute("SELECT COUNT(*) FROM loan_applications")
        total = cursor.fetchone()[0]
        print(f"\nTotal loan applications: {total}")

        cursor.execute("SELECT current_phase, COUNT(*) FROM loan_applications GROUP BY current_phase")
        phases = cursor.fetchall()
        print("\nApplications by phase:")
        for phase, count in phases:
            print(f"  Phase {phase}: {count}")

        cursor.execute("SELECT kyc_status, COUNT(*) FROM loan_applications GROUP BY kyc_status")
        kyc_stats = cursor.fetchall()
        print("\nKYC Status:")
        for status, count in kyc_stats:
            print(f"  {status}: {count}")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        exit(1)

    print(f"Database: {DB_PATH}")
    response = input("Continue with migration? (yes/no): ")

    if response.lower() in ['yes', 'y']:
        migrate()
    else:
        print("Migration cancelled.")

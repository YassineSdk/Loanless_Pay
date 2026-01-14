"""
Simple script to add sample loan applications using raw SQL
This avoids SQLAlchemy caching issues
"""

import sqlite3
import os
from datetime import datetime, timedelta

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'database.db')

def add_sample_data():
    """Add sample loan applications using raw SQL"""

    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Get demo user ID
        cursor.execute("SELECT id FROM users WHERE username = 'demo'")
        result = cursor.fetchone()
        if not result:
            print("Error: Demo user not found")
            return

        user_id = result[0]
        print(f"Found demo user with ID: {user_id}")

        # Clear existing loan applications for demo user
        cursor.execute("DELETE FROM loan_applications WHERE user_id = ?", (user_id,))
        print(f"Cleared existing applications")

        # Sample applications data
        applications = [
            # Phase 1 - KYC Pending
            (user_id, 'pending', 1, 'in_progress', 'pending', 'not_started', 'not_started',
             'John Doe', '1990-05-15', 'United States', '+1-555-0101',
             '123 Main Street, New York, NY 10001', '123-45-6789',
             50000.0, 'Business expansion - Opening new retail location', 36,
             0.0, 'Unknown', None, 0, None),

            # Phase 2 - Financial Pending
            (user_id, 'pending', 2, 'in_progress', 'approved', 'pending', 'not_started',
             'Jane Smith', '1985-08-22', 'Canada', '+1-555-0102',
             '456 Oak Avenue, Toronto, ON M5H 2N2', '987-65-4321',
             75000.0, 'Equipment purchase for manufacturing', 48,
             8500.0, 'Self-Employed', 'Smith Manufacturing LLC', 0, None),

            # Phase 3 - Decision Pending
            (user_id, 'pending', 3, 'in_progress', 'approved', 'approved', 'pending',
             'Michael Johnson', '1988-03-10', 'United Kingdom', '+44-20-1234-5678',
             '789 High Street, London, SW1A 1AA', 'AB123456C',
             100000.0, 'Real estate investment - Rental property', 60,
             12000.0, 'Employed', 'Tech Solutions Ltd', 1, 15000.0),

            # Completed - Accepted
            (user_id, 'approved', 3, 'completed', 'approved', 'approved', 'approved',
             'Sarah Williams', '1992-11-05', 'Australia', '+61-2-9876-5432',
             '321 Beach Road, Sydney, NSW 2000', 'AUS123456',
             30000.0, 'Working capital for online business', 24,
             6500.0, 'Self-Employed', 'Williams E-Commerce', 0, None),

            # Cancelled - KYC Rejected
            (user_id, 'rejected', 1, 'cancelled', 'rejected', 'not_started', 'not_started',
             'Robert Brown', '1995-07-18', 'Germany', '+49-30-1234-5678',
             'Unter den Linden 1, Berlin, 10117', 'DE987654321',
             25000.0, 'Debt consolidation', 30,
             0.0, 'Unknown', None, 0, None),
        ]

        # Insert applications
        for i, app_data in enumerate(applications, 1):
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute("""
                INSERT INTO loan_applications (
                    user_id, status, current_phase, overall_status,
                    kyc_status, financial_status, decision_status,
                    full_name, date_of_birth, nationality, phone_number,
                    address, national_id_number,
                    loan_amount_requested, loan_purpose, loan_duration_months,
                    monthly_income, employment_status, employer_name,
                    has_other_loans, other_loans_amount,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (*app_data, now, now))

            print(f"✓ Created application #{i}: {app_data[7]} - Phase {app_data[2]}")

        # For the completed application, add approved loan terms
        cursor.execute("""
            UPDATE loan_applications
            SET approved_amount = 30000.0,
                approved_duration = 24,
                interest_rate = 8.5,
                monthly_payment = 1378.50,
                final_decision = 'accepted'
            WHERE full_name = 'Sarah Williams'
        """)
        print("✓ Added loan terms for approved application")

        # Commit changes
        conn.commit()

        # Show summary
        cursor.execute("SELECT COUNT(*) FROM loan_applications WHERE user_id = ?", (user_id,))
        total = cursor.fetchone()[0]
        print(f"\n✅ Successfully created {total} sample loan applications!")

        cursor.execute("""
            SELECT current_phase, COUNT(*)
            FROM loan_applications
            WHERE user_id = ?
            GROUP BY current_phase
        """, (user_id,))

        print("\nApplications by phase:")
        for phase, count in cursor.fetchall():
            print(f"  Phase {phase}: {count}")

        print(f"\n🌐 View them at: http://127.0.0.1:5000/admin/loan-applications")
        print(f"📊 Dashboard at: http://127.0.0.1:5000/admin/dashboard")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Adding Sample Loan Applications (Raw SQL)")
    print("=" * 60)
    add_sample_data()

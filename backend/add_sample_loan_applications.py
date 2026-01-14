"""
Script to add sample loan applications for testing the admin dashboard
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User, LoanApplication
from datetime import datetime, timedelta
import random

def create_sample_applications():
    """Create sample loan applications for testing"""

    with app.app_context():
        # Get or create demo user
        demo_user = User.query.filter_by(username="demo").first()

        if not demo_user:
            print("Demo user not found. Please run the app first to initialize the database.")
            return

        print(f"Creating sample loan applications for user: {demo_user.username}")

        # Sample data
        sample_applications = [
            {
                "current_phase": 1,
                "kyc_status": "pending",
                "financial_status": "not_started",
                "decision_status": "not_started",
                "overall_status": "in_progress",
                "full_name": "John Doe",
                "date_of_birth": datetime(1990, 5, 15).date(),
                "nationality": "United States",
                "phone_number": "+1-555-0101",
                "address": "123 Main Street, New York, NY 10001",
                "national_id_number": "123-45-6789",
                "loan_amount_requested": 50000.00,
                "loan_duration_months": 36,
                "loan_purpose": "Business expansion - Opening new retail location",
            },
            {
                "current_phase": 2,
                "kyc_status": "approved",
                "financial_status": "pending",
                "decision_status": "not_started",
                "overall_status": "in_progress",
                "full_name": "Jane Smith",
                "date_of_birth": datetime(1985, 8, 22).date(),
                "nationality": "Canada",
                "phone_number": "+1-555-0102",
                "address": "456 Oak Avenue, Toronto, ON M5H 2N2",
                "national_id_number": "987-65-4321",
                "loan_amount_requested": 75000.00,
                "loan_duration_months": 48,
                "loan_purpose": "Equipment purchase for manufacturing",
                "monthly_income": 8500.00,
                "employment_status": "Self-Employed",
                "employer_name": "Smith Manufacturing LLC",
                "kyc_submitted_at": datetime.utcnow() - timedelta(days=5),
                "kyc_approved_at": datetime.utcnow() - timedelta(days=3),
                "financial_submitted_at": datetime.utcnow() - timedelta(days=1),
            },
            {
                "current_phase": 3,
                "kyc_status": "approved",
                "financial_status": "approved",
                "decision_status": "pending",
                "overall_status": "in_progress",
                "full_name": "Michael Johnson",
                "date_of_birth": datetime(1988, 3, 10).date(),
                "nationality": "United Kingdom",
                "phone_number": "+44-20-1234-5678",
                "address": "789 High Street, London, SW1A 1AA",
                "national_id_number": "AB123456C",
                "loan_amount_requested": 100000.00,
                "loan_duration_months": 60,
                "loan_purpose": "Real estate investment - Rental property",
                "monthly_income": 12000.00,
                "employment_status": "Employed",
                "employer_name": "Tech Solutions Ltd",
                "has_other_loans": True,
                "other_loans_amount": 15000.00,
                "kyc_submitted_at": datetime.utcnow() - timedelta(days=10),
                "kyc_approved_at": datetime.utcnow() - timedelta(days=8),
                "financial_submitted_at": datetime.utcnow() - timedelta(days=5),
                "financial_approved_at": datetime.utcnow() - timedelta(days=3),
            },
            {
                "current_phase": 3,
                "kyc_status": "approved",
                "financial_status": "approved",
                "decision_status": "approved",
                "overall_status": "completed",
                "final_decision": "accepted",
                "full_name": "Sarah Williams",
                "date_of_birth": datetime(1992, 11, 5).date(),
                "nationality": "Australia",
                "phone_number": "+61-2-9876-5432",
                "address": "321 Beach Road, Sydney, NSW 2000",
                "national_id_number": "AUS123456",
                "loan_amount_requested": 30000.00,
                "loan_duration_months": 24,
                "loan_purpose": "Working capital for online business",
                "monthly_income": 6500.00,
                "employment_status": "Self-Employed",
                "employer_name": "Williams E-Commerce",
                "approved_amount": 30000.00,
                "approved_duration": 24,
                "interest_rate": 8.5,
                "monthly_payment": 1378.50,
                "kyc_submitted_at": datetime.utcnow() - timedelta(days=20),
                "kyc_approved_at": datetime.utcnow() - timedelta(days=18),
                "financial_submitted_at": datetime.utcnow() - timedelta(days=15),
                "financial_approved_at": datetime.utcnow() - timedelta(days=12),
                "decision_made_at": datetime.utcnow() - timedelta(days=10),
            },
            {
                "current_phase": 1,
                "kyc_status": "rejected",
                "financial_status": "not_started",
                "decision_status": "not_started",
                "overall_status": "cancelled",
                "full_name": "Robert Brown",
                "date_of_birth": datetime(1995, 7, 18).date(),
                "nationality": "Germany",
                "phone_number": "+49-30-1234-5678",
                "address": "Unter den Linden 1, Berlin, 10117",
                "national_id_number": "DE987654321",
                "loan_amount_requested": 25000.00,
                "loan_duration_months": 30,
                "loan_purpose": "Debt consolidation",
                "kyc_submitted_at": datetime.utcnow() - timedelta(days=7),
                "kyc_notes": "Incomplete documentation - missing proof of address",
            },
        ]

        # Create applications
        created_count = 0
        for app_data in sample_applications:
            # Add common fields
            app_data["user_id"] = demo_user.id
            app_data["created_at"] = datetime.utcnow() - timedelta(days=random.randint(1, 30))
            app_data["updated_at"] = datetime.utcnow() - timedelta(days=random.randint(0, 5))

            # Create application
            application = LoanApplication(**app_data)
            db.session.add(application)
            created_count += 1

            print(f"Created application #{created_count}: {app_data['full_name']} - Phase {app_data['current_phase']}")

        # Commit all changes
        try:
            db.session.commit()
            print(f"\n✅ Successfully created {created_count} sample loan applications!")
            print(f"\nYou can now view them at: http://127.0.0.1:5000/admin/loan-applications")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error creating applications: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Creating Sample Loan Applications")
    print("=" * 60)
    create_sample_applications()

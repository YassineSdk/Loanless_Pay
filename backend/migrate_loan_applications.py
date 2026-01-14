"""
Database Migration Script for Loan Application System
This script creates the new tables for the 3-phase loan application process
"""

from app import app
from models import db, LoanApplication, LoanPhase, LoanDocument, AdminReview

def migrate():
    """Create new tables for loan application system"""
    with app.app_context():
        print("Starting database migration for loan application system...")

        try:
            # Create all tables
            db.create_all()
            print("✓ All tables created successfully!")

            # Verify tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()

            required_tables = [
                'loan_applications',
                'loan_phases',
                'loan_documents',
                'admin_reviews'
            ]

            print("\nVerifying tables:")
            for table in required_tables:
                if table in tables:
                    print(f"  ✓ {table} - Created")
                else:
                    print(f"  ✗ {table} - Missing")

            print("\n" + "="*50)
            print("Migration completed successfully!")
            print("="*50)
            print("\nNew tables added:")
            print("  - loan_applications: Main application tracking")
            print("  - loan_phases: Phase progression tracking")
            print("  - loan_documents: Document storage and management")
            print("  - admin_reviews: Admin actions and notes")
            print("\nThe loan application system is now ready to use!")

        except Exception as e:
            print(f"\n✗ Migration failed: {str(e)}")
            raise

if __name__ == "__main__":
    migrate()

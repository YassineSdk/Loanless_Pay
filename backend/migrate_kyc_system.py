"""
Database Migration Script for Separated KYC and Loan Application System
This script creates the new structure where:
- KYC is one-time user verification
- Loan Applications are per-loan financial audits
"""

from app import app
from models import db
from sqlalchemy import text

def migrate():
    """Migrate to new KYC + Loan Application structure"""
    with app.app_context():
        print("="*60)
        print("Starting migration to separated KYC & Loan system...")
        print("="*60)

        try:
            # Drop old tables if they exist
            print("\n1. Cleaning up old tables...")
            db.session.execute(text('DROP TABLE IF EXISTS admin_reviews'))
            db.session.execute(text('DROP TABLE IF EXISTS loan_phases'))
            db.session.commit()
            print("   ✓ Dropped old tables")

            # Add KYC columns to users table if they don't exist
            print("\n2. Adding KYC columns to users table...")

            try:
                db.session.execute(text("""
                    ALTER TABLE users ADD COLUMN nationality VARCHAR(100)
                """))
                print("   ✓ Added nationality column")
            except Exception as e:
                if "duplicate column" not in str(e).lower() and "already exists" not in str(e).lower():
                    print(f"   ⚠ nationality: {e}")
                else:
                    print("   ✓ nationality column already exists")

            try:
                db.session.execute(text("""
                    ALTER TABLE users ADD COLUMN national_id_number VARCHAR(100)
                """))
                print("   ✓ Added national_id_number column")
            except Exception as e:
                if "duplicate column" not in str(e).lower() and "already exists" not in str(e).lower():
                    print(f"   ⚠ national_id_number: {e}")
                else:
                    print("   ✓ national_id_number column already exists")

            try:
                db.session.execute(text("""
                    ALTER TABLE users ADD COLUMN kyc_status VARCHAR(20) DEFAULT 'pending'
                """))
                print("   ✓ Added kyc_status column")
            except Exception as e:
                if "duplicate column" not in str(e).lower() and "already exists" not in str(e).lower():
                    print(f"   ⚠ kyc_status: {e}")
                else:
                    print("   ✓ kyc_status column already exists")

            try:
                db.session.execute(text("""
                    ALTER TABLE users ADD COLUMN kyc_submitted INTEGER DEFAULT 0
                """))
                print("   ✓ Added kyc_submitted column")
            except Exception as e:
                if "duplicate column" not in str(e).lower() and "already exists" not in str(e).lower():
                    print(f"   ⚠ kyc_submitted: {e}")
                else:
                    print("   ✓ kyc_submitted column already exists")

            try:
                db.session.execute(text("""
                    ALTER TABLE users ADD COLUMN kyc_submitted_at DATETIME
                """))
                print("   ✓ Added kyc_submitted_at column")
            except Exception as e:
                if "duplicate column" not in str(e).lower() and "already exists" not in str(e).lower():
                    print(f"   ⚠ kyc_submitted_at: {e}")
                else:
                    print("   ✓ kyc_submitted_at column already exists")

            try:
                db.session.execute(text("""
                    ALTER TABLE users ADD COLUMN kyc_approved_at DATETIME
                """))
                print("   ✓ Added kyc_approved_at column")
            except Exception as e:
                if "duplicate column" not in str(e).lower() and "already exists" not in str(e).lower():
                    print(f"   ⚠ kyc_approved_at: {e}")
                else:
                    print("   ✓ kyc_approved_at column already exists")

            try:
                db.session.execute(text("""
                    ALTER TABLE users ADD COLUMN kyc_approved_by INTEGER
                """))
                print("   ✓ Added kyc_approved_by column")
            except Exception as e:
                if "duplicate column" not in str(e).lower() and "already exists" not in str(e).lower():
                    print(f"   ⚠ kyc_approved_by: {e}")
                else:
                    print("   ✓ kyc_approved_by column already exists")

            db.session.commit()

            # Create all new tables
            print("\n3. Creating new table structure...")
            db.create_all()
            print("   ✓ All tables created/updated successfully!")

            # Set all existing users to kyc_status='pending'
            print("\n4. Setting default KYC status for existing users...")
            db.session.execute(text("""
                UPDATE users
                SET kyc_status = 'pending', kyc_submitted = 0
                WHERE kyc_status IS NULL OR kyc_status = ''
            """))
            db.session.commit()
            print("   ✓ Updated existing users")

            print("\n" + "="*60)
            print("✓ Migration completed successfully!")
            print("="*60)
            print("\nNew System Structure:")
            print("\n1. KYC VERIFICATION (One-time per user)")
            print("   - User registers → KYC status = 'pending'")
            print("   - User completes KYC form + uploads documents")
            print("   - Admin reviews and approves/rejects USER")
            print("   - Once approved, user can apply for loans")
            print("\n2. LOAN APPLICATIONS (Per loan)")
            print("   - KYC-approved users can apply for loans")
            print("   - Each application requires financial info + documents")
            print("   - Admin reviews and approves/rejects each LOAN")
            print("\n3. TABLES:")
            print("   - users: User accounts with KYC status")
            print("   - kyc_documents: KYC verification documents")
            print("   - loan_applications: Individual loan requests")
            print("   - loan_documents: Financial documents per loan")
            print("\n" + "="*60)
            print("System is ready to use!")
            print("="*60)

        except Exception as e:
            print(f"\n✗ Migration failed: {str(e)}")
            print("\nError details:")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            raise

if __name__ == "__main__":
    migrate()

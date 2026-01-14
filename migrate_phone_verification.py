"""
Database Migration Script for Phone Verification
Adds phone verification fields to existing User table
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app import app, db
from models import User
from sqlalchemy import text


def migrate_database():
    """Add phone verification fields to users table"""

    print("\n" + "=" * 70)
    print("PHONE VERIFICATION DATABASE MIGRATION")
    print("=" * 70 + "\n")

    with app.app_context():
        try:
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            columns = [col["name"] for col in inspector.get_columns("users")]

            new_columns = [
                "phone_verified",
                "phone_verification_code",
                "phone_verification_expires",
                "phone_verified_at",
            ]

            columns_to_add = [col for col in new_columns if col not in columns]

            if not columns_to_add:
                print("✓ All phone verification columns already exist!")
                print("  No migration needed.\n")
                return True

            print(f"Adding {len(columns_to_add)} new columns to users table...\n")

            # SQLite-specific migration (adjust for other databases)
            with db.engine.connect() as conn:
                if "phone_verified" in columns_to_add:
                    print("  → Adding column: phone_verified")
                    conn.execute(
                        text(
                            "ALTER TABLE users ADD COLUMN phone_verified BOOLEAN DEFAULT 0 NOT NULL"
                        )
                    )
                    conn.commit()

                if "phone_verification_code" in columns_to_add:
                    print("  → Adding column: phone_verification_code")
                    conn.execute(
                        text(
                            "ALTER TABLE users ADD COLUMN phone_verification_code VARCHAR(10)"
                        )
                    )
                    conn.commit()

                if "phone_verification_expires" in columns_to_add:
                    print("  → Adding column: phone_verification_expires")
                    conn.execute(
                        text(
                            "ALTER TABLE users ADD COLUMN phone_verification_expires DATETIME"
                        )
                    )
                    conn.commit()

                if "phone_verified_at" in columns_to_add:
                    print("  → Adding column: phone_verified_at")
                    conn.execute(
                        text("ALTER TABLE users ADD COLUMN phone_verified_at DATETIME")
                    )
                    conn.commit()

            print("\n✓ Migration completed successfully!")
            print("\nNew columns added:")
            for col in columns_to_add:
                print(f"  • {col}")

            # Verify migration
            print("\nVerifying migration...")
            inspector = db.inspect(db.engine)
            new_column_list = [col["name"] for col in inspector.get_columns("users")]

            all_present = all(col in new_column_list for col in new_columns)

            if all_present:
                print("✓ All columns verified successfully!\n")

                # Show current users
                users = User.query.all()
                print(f"Current users in database: {len(users)}")
                if users:
                    print(
                        "\nNote: Existing users will need to verify their phone numbers."
                    )
                    print("Their phone_verified status is currently False.\n")

                return True
            else:
                print("✗ Verification failed. Some columns may be missing.\n")
                return False

        except Exception as e:
            print(f"\n✗ Migration failed: {str(e)}\n")
            import traceback

            traceback.print_exc()
            return False


def rollback_migration():
    """Remove phone verification columns (rollback)"""

    print("\n" + "=" * 70)
    print("ROLLING BACK PHONE VERIFICATION MIGRATION")
    print("=" * 70 + "\n")

    print("⚠ WARNING: This will remove phone verification columns!")
    confirm = input("Are you sure? Type 'yes' to continue: ")

    if confirm.lower() != "yes":
        print("\nRollback cancelled.\n")
        return False

    with app.app_context():
        try:
            # Note: SQLite doesn't support DROP COLUMN easily
            # For production, you'd need to recreate the table
            print("\n⚠ SQLite doesn't support DROP COLUMN.")
            print("To rollback, you would need to:")
            print("  1. Backup your data")
            print("  2. Drop the users table")
            print("  3. Recreate without phone verification fields")
            print("  4. Restore your data\n")
            print("For now, columns will remain but won't be used.\n")

            return True

        except Exception as e:
            print(f"\n✗ Rollback failed: {str(e)}\n")
            return False


def check_migration_status():
    """Check if migration has been applied"""

    print("\n" + "=" * 70)
    print("PHONE VERIFICATION MIGRATION STATUS")
    print("=" * 70 + "\n")

    with app.app_context():
        try:
            inspector = db.inspect(db.engine)
            columns = [col["name"] for col in inspector.get_columns("users")]

            required_columns = [
                "phone_verified",
                "phone_verification_code",
                "phone_verification_expires",
                "phone_verified_at",
            ]

            print("Checking for phone verification columns:\n")

            all_present = True
            for col in required_columns:
                status = "✓" if col in columns else "✗"
                print(f"  {status} {col}")
                if col not in columns:
                    all_present = False

            print("\n" + "-" * 70)

            if all_present:
                print("Status: ✓ Migration completed - All columns present")

                # Show verification stats
                total_users = User.query.count()
                verified_users = User.query.filter_by(phone_verified=True).count()
                unverified_users = total_users - verified_users

                print(f"\nUser Statistics:")
                print(f"  Total users: {total_users}")
                print(f"  Phone verified: {verified_users}")
                print(f"  Not verified: {unverified_users}")

            else:
                print("Status: ✗ Migration needed - Some columns missing")
                print("\nRun: python migrate_phone_verification.py migrate")

            print("\n" + "=" * 70 + "\n")

            return all_present

        except Exception as e:
            print(f"\n✗ Status check failed: {str(e)}\n")
            return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "migrate":
            success = migrate_database()
            sys.exit(0 if success else 1)

        elif command == "rollback":
            success = rollback_migration()
            sys.exit(0 if success else 1)

        elif command == "status":
            success = check_migration_status()
            sys.exit(0 if success else 1)

        else:
            print("\nUnknown command. Available commands:")
            print("  migrate  - Apply phone verification migration")
            print("  rollback - Remove phone verification columns")
            print("  status   - Check migration status\n")
            sys.exit(1)
    else:
        # Default: run migration
        print("\nRunning phone verification migration...")
        print("(Use 'python migrate_phone_verification.py status' to check status)\n")

        success = migrate_database()
        sys.exit(0 if success else 1)

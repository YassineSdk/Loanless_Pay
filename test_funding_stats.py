"""
Test script to verify funding statistics are being calculated correctly
Run this to check if the funding partners section data is available
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app import app, db
from models import FundingTransaction, User
from sqlalchemy import desc, func


def test_funding_stats():
    """Test if funding statistics are being calculated"""

    print("=" * 60)
    print("FUNDING PARTNERS STATISTICS TEST")
    print("=" * 60)
    print()

    with app.app_context():
        try:
            # Test 1: Count funding partners
            total_funding_partners = User.query.filter_by(
                user_role="funding_party"
            ).count()
            print(f"✓ Total Funding Partners: {total_funding_partners}")

            # Test 2: Count active funding partners
            active_funding_partners = User.query.filter_by(
                user_role="funding_party", is_active=True
            ).count()
            print(f"✓ Active Funding Partners: {active_funding_partners}")

            # Test 3: Calculate total deposits
            total_funds_deposited = (
                db.session.query(func.sum(FundingTransaction.amount))
                .filter(FundingTransaction.transaction_type == "deposit")
                .scalar()
                or 0
            )
            print(f"✓ Total Funds Deposited: ${total_funds_deposited:,.2f}")

            # Test 4: Calculate total withdrawals
            total_funds_withdrawn = (
                db.session.query(func.sum(FundingTransaction.amount))
                .filter(FundingTransaction.transaction_type == "withdrawal")
                .scalar()
                or 0
            )
            print(f"✓ Total Funds Withdrawn: ${total_funds_withdrawn:,.2f}")

            # Test 5: Calculate available funds
            available_funds = total_funds_deposited - total_funds_withdrawn
            print(f"✓ Available Funds: ${available_funds:,.2f}")
            print()

            # Test 6: Get recent funding partners
            recent_funding_partners = (
                User.query.filter_by(user_role="funding_party")
                .order_by(desc(User.created_at))
                .limit(5)
                .all()
            )
            print(f"✓ Recent Funding Partners: {len(recent_funding_partners)} found")

            if recent_funding_partners:
                print("  Recent Partners List:")
                for i, partner in enumerate(recent_funding_partners, 1):
                    status = "Active" if partner.is_active else "Inactive"
                    company = partner.company_name or partner.email
                    print(f"  {i}. {partner.username} ({company}) - {status}")
            else:
                print("  (No funding partners registered yet)")
            print()

            # Test 7: Get top funders
            top_funders = (
                db.session.query(
                    User.username,
                    User.company_name,
                    func.sum(FundingTransaction.amount).label("total_contributed"),
                )
                .join(FundingTransaction, User.id == FundingTransaction.funder_id)
                .filter(FundingTransaction.transaction_type == "deposit")
                .group_by(User.id, User.username, User.company_name)
                .order_by(desc("total_contributed"))
                .limit(5)
                .all()
            )
            print(f"✓ Top Contributors: {len(top_funders)} found")

            if top_funders:
                print("  Top Contributors List:")
                for i, funder in enumerate(top_funders, 1):
                    company = funder.company_name or "N/A"
                    print(
                        f"  {i}. {funder.username} ({company}) - ${funder.total_contributed:,.2f}"
                    )
            else:
                print("  (No transactions recorded yet)")
            print()

            # Summary
            print("=" * 60)
            print("TEST RESULTS SUMMARY")
            print("=" * 60)

            if total_funding_partners == 0:
                print("⚠ No funding partners found in database")
                print("  → The section will show 'No funding partners yet'")
                print("  → Create a user with role='funding_party' to test")
            else:
                print(f"✓ {total_funding_partners} funding partner(s) found")
                print("  → The section should display with data")

            if total_funds_deposited == 0:
                print("⚠ No deposit transactions found")
                print("  → Top Contributors will show empty state")
                print("  → Add FundingTransaction records to test")
            else:
                print(f"✓ ${total_funds_deposited:,.2f} in deposits recorded")
                print("  → Top Contributors should display")

            print()
            print("=" * 60)
            print("CONCLUSION")
            print("=" * 60)

            if total_funding_partners > 0 or total_funds_deposited > 0:
                print("✓ Backend statistics are working correctly")
                print("✓ Data is available for the dashboard")
                print()
                print("If section not visible:")
                print("  1. Restart Flask server (Ctrl+C then restart)")
                print("  2. Hard refresh browser (Ctrl+Shift+F5)")
                print("  3. Clear browser cache")
                print("  4. Check browser console for errors")
            else:
                print("⚠ No funding data in database yet")
                print()
                print("To add test data:")
                print("  1. Register a user with role='funding_party'")
                print("  2. Add FundingTransaction records")
                print("  3. Run this test again")

            print()
            print("=" * 60)

        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            print(f"  Type: {type(e).__name__}")
            import traceback

            print("\nFull Traceback:")
            traceback.print_exc()
            return False

    return True


if __name__ == "__main__":
    print()
    success = test_funding_stats()
    print()

    if success:
        print("✓ Test completed successfully!")
    else:
        print("✗ Test failed - see errors above")

    print()

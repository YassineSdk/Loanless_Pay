"""
Test script to verify funding routes are working correctly
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app import app
from flask import url_for


def test_funding_routes():
    """Test all funding routes"""
    print("\n" + "=" * 60)
    print("FUNDING ROUTES VERIFICATION")
    print("=" * 60 + "\n")

    with app.test_request_context():
        routes_to_test = [
            ("funding.dashboard", {}, "Funding Dashboard"),
            ("funding.transactions", {}, "Transactions Page"),
            ("funding.profile", {}, "Profile Page"),
            ("funding.add_funding", {}, "Add Funding Page"),
            ("funding.analytics", {}, "Analytics Page"),
            ("funding.funded_loans", {}, "Funded Loans Page"),
        ]

        passed = 0
        failed = 0

        for endpoint, params, description in routes_to_test:
            try:
                url = url_for(endpoint, **params)
                print(f"✓ {description:30} → {url}")
                passed += 1
            except Exception as e:
                print(f"✗ {description:30} → ERROR: {str(e)}")
                failed += 1

        print("\n" + "-" * 60)
        print(f"Results: {passed} passed, {failed} failed")
        print("-" * 60)

        if failed == 0:
            print("\n✅ All funding routes are working correctly!")
            print("\nYou can now access:")
            print("  • Transactions: http://127.0.0.1:5000/funding/transactions")
            print("  • Profile:      http://127.0.0.1:5000/funding/profile")
            print("  • Dashboard:    http://127.0.0.1:5000/funding/dashboard")
        else:
            print("\n⚠️ Some routes failed. Please check the errors above.")

        print("\n" + "=" * 60 + "\n")

        return failed == 0


if __name__ == "__main__":
    success = test_funding_routes()
    sys.exit(0 if success else 1)

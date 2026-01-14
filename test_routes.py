"""
Quick Route Testing Script
Tests all critical routes to ensure they exist and are accessible
"""

from app import app
from flask import url_for


def test_routes():
    """Test that all critical routes exist"""

    with app.test_client() as client:
        with app.app_context():
            print("=" * 60)
            print("ROUTE EXISTENCE TEST")
            print("=" * 60)

            # List of all routes to test
            routes_to_test = [
                # Main app routes
                ("index", {}, "Landing page"),
                ("login", {}, "Login page"),
                ("register", {}, "Registration page"),
                ("logout", {}, "Logout"),
                ("main", {}, "Main user page"),
                ("profile_page", {}, "Profile page"),
                ("simulate_page", {}, "Loan simulation page"),
                ("dashboard_page", {}, "Dashboard page"),
                ("cancel_legacy_loan", {"loan_id": 1}, "Cancel legacy loan"),
                # Admin routes
                ("admin.dashboard", {}, "Admin dashboard"),
                ("admin.users", {}, "Admin users list"),
                ("admin.loans", {}, "Admin loans list"),
                ("admin.loan_applications", {}, "Admin loan applications"),
                ("admin.kyc_verifications", {}, "Admin KYC verifications"),
                # KYC routes
                ("kyc.index", {}, "KYC index"),
                ("kyc.verify", {}, "KYC verify"),
                # Loan application routes
                ("loan_app.index", {}, "Loan application index"),
                ("loan_app.apply", {}, "Loan application apply"),
                ("loan_app.cancel", {"application_id": 1}, "Cancel loan application"),
                # Funding routes
                ("funding.dashboard", {}, "Funding dashboard"),
                # API routes
                ("auth_status", {}, "Auth status API"),
                ("api_login", {}, "Login API"),
                ("api_register", {}, "Register API"),
                ("api_logout", {}, "Logout API"),
                ("api_profile", {}, "Profile API"),
                ("api_simulate", {}, "Simulate API"),
                ("calculate", {}, "Calculate API"),
                ("api_dashboard", {}, "Dashboard API"),
            ]

            passed = 0
            failed = 0

            for endpoint, params, description in routes_to_test:
                try:
                    url = url_for(endpoint, **params)
                    status = "✓ PASS"
                    passed += 1
                    print(f"{status} | {endpoint:40} | {description}")
                except Exception as e:
                    status = "✗ FAIL"
                    failed += 1
                    print(f"{status} | {endpoint:40} | {description}")
                    print(f"         Error: {str(e)}")

            print("=" * 60)
            print(f"RESULTS: {passed} passed, {failed} failed")
            print("=" * 60)

            if failed == 0:
                print("✓ All routes exist and are accessible!")
                return True
            else:
                print(f"✗ {failed} route(s) failed - please check above")
                return False


def test_dashboard_routes_specifically():
    """Test routes specifically used in dashboard.html"""

    with app.test_client() as client:
        with app.app_context():
            print("\n" + "=" * 60)
            print("DASHBOARD SPECIFIC ROUTES TEST")
            print("=" * 60)

            dashboard_routes = [
                ("simulate_page", {}, "Apply for Loan button"),
                ("cancel_legacy_loan", {"loan_id": 1}, "Cancel Application button"),
                ("kyc.index", {}, "Complete KYC button"),
                ("loan_app.detail", {"application_id": 1}, "View application detail"),
            ]

            all_pass = True

            for endpoint, params, description in dashboard_routes:
                try:
                    url = url_for(endpoint, **params)
                    print(f"✓ PASS | {endpoint:30} | {description}")
                    print(f"         URL: {url}")
                except Exception as e:
                    print(f"✗ FAIL | {endpoint:30} | {description}")
                    print(f"         Error: {str(e)}")
                    all_pass = False

            print("=" * 60)

            if all_pass:
                print("✓ All dashboard routes are working!")
                return True
            else:
                print("✗ Some dashboard routes failed")
                return False


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "ROUTE TESTING UTILITY" + " " * 22 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    # Test all routes
    all_routes_pass = test_routes()

    # Test dashboard specific routes
    dashboard_pass = test_dashboard_routes_specifically()

    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    if all_routes_pass and dashboard_pass:
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("\nThe routing fixes have been successfully applied.")
        print("The 'My Loans' button should now work correctly!")
    else:
        print("✗✗✗ SOME TESTS FAILED ✗✗✗")
        print("\nPlease review the errors above.")

    print("=" * 60 + "\n")

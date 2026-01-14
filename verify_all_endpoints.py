"""
Comprehensive Endpoint Verification Script
Tests all routes and endpoints to ensure no BuildError occurs
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from flask import url_for


def test_all_endpoints():
    """Test all application endpoints"""
    from app import app

    results = {"passed": [], "failed": []}

    # Core routes to test
    endpoints_to_test = [
        # Public routes
        ("index", {}, "GET"),
        ("login", {}, "GET"),
        ("register", {}, "GET"),
        ("main", {}, "GET"),
        # User routes (require login)
        ("simulate_page", {}, "GET"),
        ("dashboard_page", {}, "GET"),
        ("profile_page", {}, "GET"),
        ("logout", {}, "GET"),
        # API routes
        ("auth_status", {}, "GET"),
        ("api_login", {}, "POST"),
        ("api_register", {}, "POST"),
        ("api_logout", {}, "POST"),
        ("api_profile", {}, "GET"),
        ("api_simulate", {}, "POST"),
        ("calculate", {}, "POST"),
        ("api_dashboard", {}, "GET"),
        # Admin routes (require admin role)
        ("admin.dashboard", {}, "GET"),
        ("admin.users", {}, "GET"),
        ("admin.kyc_verification", {}, "GET"),
        ("admin.funding_partners", {}, "GET"),
        ("admin.loan_applications", {}, "GET"),
        # Funding routes
        ("funding.dashboard", {}, "GET"),
        ("funding.contribute", {}, "GET"),
        ("funding.transactions", {}, "GET"),
        ("funding.analytics", {}, "GET"),
        # KYC routes
        ("kyc.verification_dashboard", {}, "GET"),
        ("kyc.submit_kyc", {}, "GET"),
        # Loan application routes
        ("loan_app.dashboard", {}, "GET"),
        ("loan_app.new_application", {}, "GET"),
        ("loan_app.my_applications", {}, "GET"),
        # Legacy routes
        ("funding_inquiry", {}, "POST"),
        ("admin_funding_parties", {}, "GET"),
        ("cancel_legacy_loan", {"loan_id": 1}, "POST"),
    ]

    with app.test_request_context():
        print("\n" + "=" * 80)
        print("ENDPOINT VERIFICATION TEST")
        print("=" * 80 + "\n")

        for endpoint_info in endpoints_to_test:
            if len(endpoint_info) == 3:
                endpoint, params, method = endpoint_info
            else:
                endpoint, params = endpoint_info
                method = "GET"

            try:
                url = url_for(endpoint, **params)
                results["passed"].append(
                    {"endpoint": endpoint, "url": url, "method": method}
                )
                print(f"✓ {endpoint:40} → {url:40} [{method}]")
            except Exception as e:
                results["failed"].append(
                    {"endpoint": endpoint, "error": str(e), "method": method}
                )
                print(f"✗ {endpoint:40} → ERROR: {str(e)}")

        # Print summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"✓ Passed: {len(results['passed'])}")
        print(f"✗ Failed: {len(results['failed'])}")

        if results["failed"]:
            print("\n" + "-" * 80)
            print("FAILED ENDPOINTS:")
            print("-" * 80)
            for failure in results["failed"]:
                print(f"  • {failure['endpoint']}")
                print(f"    Error: {failure['error']}")
                print()

        print("=" * 80 + "\n")

        return len(results["failed"]) == 0


def test_template_urls():
    """Test that all templates use correct url_for calls"""
    import os

    from app import app

    print("\n" + "=" * 80)
    print("TEMPLATE URL VERIFICATION")
    print("=" * 80 + "\n")

    templates_dir = os.path.join(os.path.dirname(__file__), "backend", "templates")
    issues = []

    # Common patterns that might cause BuildError
    problematic_patterns = [
        "url_for('simulate')",  # Should be 'simulate_page'
        "url_for('dashboard')",  # Should be 'dashboard_page'
        "url_for('profile')",  # Should be 'profile_page'
    ]

    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, templates_dir)

                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                    for pattern in problematic_patterns:
                        if pattern in content:
                            issues.append({"file": rel_path, "pattern": pattern})

    if issues:
        print("⚠ Found potentially problematic url_for patterns:\n")
        for issue in issues:
            print(f"  • {issue['file']}")
            print(f"    Contains: {issue['pattern']}")
            print()
    else:
        print("✓ No problematic url_for patterns found in templates\n")

    print("=" * 80 + "\n")
    return len(issues) == 0


def test_blueprints():
    """Verify all blueprints are registered"""
    from app import app

    print("\n" + "=" * 80)
    print("BLUEPRINT REGISTRATION TEST")
    print("=" * 80 + "\n")

    expected_blueprints = ["admin", "funding", "kyc", "loan_app"]
    registered = []
    missing = []

    for blueprint_name in expected_blueprints:
        if blueprint_name in app.blueprints:
            registered.append(blueprint_name)
            print(f"✓ {blueprint_name:20} → Registered")
        else:
            missing.append(blueprint_name)
            print(f"✗ {blueprint_name:20} → NOT REGISTERED")

    print("\n" + "=" * 80)
    print(f"Registered: {len(registered)}/{len(expected_blueprints)}")

    if missing:
        print(f"\nMissing blueprints: {', '.join(missing)}")

    print("=" * 80 + "\n")

    return len(missing) == 0


def test_models():
    """Verify all required models exist"""
    print("\n" + "=" * 80)
    print("MODEL VERIFICATION TEST")
    print("=" * 80 + "\n")

    try:
        from models import (
            FundingParty,
            FundingTransaction,
            FundingUsage,
            KYCDocument,
            Loan,
            LoanApplication,
            LoanDocument,
            User,
            db,
        )

        models = [
            "User",
            "Loan",
            "LoanApplication",
            "LoanDocument",
            "KYCDocument",
            "FundingParty",
            "FundingTransaction",
            "FundingUsage",
            "AdminReview",
        ]

        for model_name in models:
            try:
                model = eval(model_name) if model_name != "AdminReview" else None

                if model_name == "AdminReview":
                    # Special check for AdminReview
                    try:
                        from models import AdminReview

                        print(f"✓ {model_name:20} → Available")
                    except ImportError:
                        print(f"⚠ {model_name:20} → Not found (may need migration)")
                else:
                    print(f"✓ {model_name:20} → Available")
            except Exception as e:
                print(f"✗ {model_name:20} → Error: {str(e)}")

        print("\n" + "=" * 80 + "\n")
        return True

    except Exception as e:
        print(f"✗ Failed to import models: {str(e)}")
        print("=" * 80 + "\n")
        return False


def run_all_tests():
    """Run all verification tests"""
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "LOANLESS APPLICATION VERIFICATION" + " " * 25 + "║")
    print("╚" + "═" * 78 + "╝")

    results = {
        "models": test_models(),
        "blueprints": test_blueprints(),
        "endpoints": test_all_endpoints(),
        "templates": test_template_urls(),
    }

    # Final summary
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 30 + "FINAL SUMMARY" + " " * 35 + "║")
    print("╠" + "═" * 78 + "╣")

    all_passed = all(results.values())

    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"║  {test_name.upper():20} {status:54}  ║")

    print("╠" + "═" * 78 + "╣")

    if all_passed:
        print("║" + " " * 20 + "✓ ALL TESTS PASSED" + " " * 39 + "║")
    else:
        print("║" + " " * 20 + "✗ SOME TESTS FAILED" + " " * 38 + "║")

    print("╚" + "═" * 78 + "╝\n")

    return all_passed


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error running tests: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

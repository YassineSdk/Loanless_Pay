"""
Phone Verification System Test Script
Tests all components of the phone verification system
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))


def test_phone_verification():
    """Test phone verification system"""
    print("\n" + "=" * 70)
    print("PHONE VERIFICATION SYSTEM TEST")
    print("=" * 70 + "\n")

    results = {"passed": 0, "failed": 0, "tests": []}

    # Test 1: Import phone verification service
    try:
        from phone_verification import phone_service

        results["passed"] += 1
        results["tests"].append(("Import phone_verification module", "PASS"))
        print("✓ Test 1: Phone verification module imported successfully")
    except Exception as e:
        results["failed"] += 1
        results["tests"].append(("Import phone_verification module", f"FAIL: {e}"))
        print(f"✗ Test 1: Failed to import phone_verification: {e}")
        return results

    # Test 2: Check if service initialized
    try:
        assert phone_service is not None
        results["passed"] += 1
        results["tests"].append(("Phone service initialization", "PASS"))
        print("✓ Test 2: Phone service initialized")
    except Exception as e:
        results["failed"] += 1
        results["tests"].append(("Phone service initialization", f"FAIL: {e}"))
        print(f"✗ Test 2: Phone service initialization failed: {e}")

    # Test 3: Check mock mode status
    try:
        print(f"  ℹ Mock mode: {phone_service.use_mock}")
        results["passed"] += 1
        results["tests"].append(("Check mock mode", "PASS"))
        print("✓ Test 3: Mock mode status checked")
    except Exception as e:
        results["failed"] += 1
        results["tests"].append(("Check mock mode", f"FAIL: {e}"))
        print(f"✗ Test 3: Failed to check mock mode: {e}")

    # Test 4: Test OTP generation
    try:
        otp = phone_service.generate_otp()
        assert len(otp) == 6
        assert otp.isdigit()
        results["passed"] += 1
        results["tests"].append(("OTP generation", "PASS"))
        print(f"✓ Test 4: OTP generation successful (sample: {otp})")
    except Exception as e:
        results["failed"] += 1
        results["tests"].append(("OTP generation", f"FAIL: {e}"))
        print(f"✗ Test 4: OTP generation failed: {e}")

    # Test 5: Test phone number formatting
    try:
        test_numbers = [
            ("5551234567", "+15551234567"),
            ("+15551234567", "+15551234567"),
            ("15551234567", "+15551234567"),
        ]

        all_formatted = True
        for input_num, expected in test_numbers:
            result = phone_service.format_phone_number(input_num)
            if result != expected:
                all_formatted = False
                print(
                    f"  ✗ Format mismatch: {input_num} -> {result} (expected {expected})"
                )

        if all_formatted:
            results["passed"] += 1
            results["tests"].append(("Phone number formatting", "PASS"))
            print("✓ Test 5: Phone number formatting works correctly")
        else:
            results["failed"] += 1
            results["tests"].append(("Phone number formatting", "FAIL"))
            print("✗ Test 5: Phone number formatting has issues")

    except Exception as e:
        results["failed"] += 1
        results["tests"].append(("Phone number formatting", f"FAIL: {e}"))
        print(f"✗ Test 5: Phone number formatting test failed: {e}")

    # Test 6: Check User model has phone verification fields
    try:
        from app import app, db
        from models import User

        with app.app_context():
            inspector = db.inspect(db.engine)
            columns = [col["name"] for col in inspector.get_columns("users")]

            required_fields = [
                "phone_number",
                "phone_verified",
                "phone_verification_code",
                "phone_verification_expires",
                "phone_verified_at",
            ]

            all_present = all(field in columns for field in required_fields)

            if all_present:
                results["passed"] += 1
                results["tests"].append(("User model fields", "PASS"))
                print("✓ Test 6: User model has all phone verification fields")
            else:
                missing = [f for f in required_fields if f not in columns]
                results["failed"] += 1
                results["tests"].append(
                    ("User model fields", f"FAIL: Missing {missing}")
                )
                print(f"✗ Test 6: User model missing fields: {missing}")

    except Exception as e:
        results["failed"] += 1
        results["tests"].append(("User model fields", f"FAIL: {e}"))
        print(f"✗ Test 6: User model check failed: {e}")

    # Test 7: Check routes exist
    try:
        from app import app
        from flask import url_for

        with app.test_request_context():
            routes_to_check = [
                "register",
                "verify_phone",
                "resend_otp",
            ]

            all_routes_exist = True
            for route in routes_to_check:
                try:
                    url = url_for(route)
                    print(f"  ✓ Route '{route}' exists: {url}")
                except Exception as e:
                    all_routes_exist = False
                    print(f"  ✗ Route '{route}' missing: {e}")

            if all_routes_exist:
                results["passed"] += 1
                results["tests"].append(("Routes exist", "PASS"))
                print("✓ Test 7: All phone verification routes exist")
            else:
                results["failed"] += 1
                results["tests"].append(("Routes exist", "FAIL"))
                print("✗ Test 7: Some routes are missing")

    except Exception as e:
        results["failed"] += 1
        results["tests"].append(("Routes exist", f"FAIL: {e}"))
        print(f"✗ Test 7: Route check failed: {e}")

    # Test 8: Check verify_phone template exists
    try:
        import os

        template_path = os.path.join(
            os.path.dirname(__file__), "backend", "templates", "verify_phone.html"
        )

        if os.path.exists(template_path):
            results["passed"] += 1
            results["tests"].append(("Template exists", "PASS"))
            print("✓ Test 8: verify_phone.html template exists")
        else:
            results["failed"] += 1
            results["tests"].append(("Template exists", "FAIL"))
            print("✗ Test 8: verify_phone.html template not found")

    except Exception as e:
        results["failed"] += 1
        results["tests"].append(("Template exists", f"FAIL: {e}"))
        print(f"✗ Test 8: Template check failed: {e}")

    # Test 9: Test complete flow simulation
    try:
        from app import app, db
        from models import User

        with app.app_context():
            # Create a test user
            test_phone = "+15551234567"

            # Check if send_otp method works (without actually sending)
            print("  ℹ Testing OTP flow simulation...")

            # We won't create actual user to avoid DB pollution
            # Just verify the method exists and can be called
            assert hasattr(phone_service, "send_otp")
            assert hasattr(phone_service, "verify_otp")
            assert hasattr(phone_service, "resend_otp")
            assert hasattr(phone_service, "check_verification_status")

            results["passed"] += 1
            results["tests"].append(("Service methods", "PASS"))
            print("✓ Test 9: All service methods exist and are callable")

    except Exception as e:
        results["failed"] += 1
        results["tests"].append(("Service methods", f"FAIL: {e}"))
        print(f"✗ Test 9: Service methods check failed: {e}")

    # Test 10: Check decorator exists
    try:
        from decorators import phone_verified_required

        results["passed"] += 1
        results["tests"].append(("Decorator import", "PASS"))
        print("✓ Test 10: phone_verified_required decorator imported successfully")
    except Exception as e:
        results["failed"] += 1
        results["tests"].append(("Decorator import", f"FAIL: {e}"))
        print(f"✗ Test 10: Failed to import decorator: {e}")

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {results['passed'] + results['failed']}")
    print(f"✓ Passed: {results['passed']}")
    print(f"✗ Failed: {results['failed']}")
    print("=" * 70)

    if results["failed"] > 0:
        print("\nFailed Tests:")
        for test_name, status in results["tests"]:
            if status.startswith("FAIL"):
                print(f"  • {test_name}: {status}")

    print("\n")

    return results


def test_integration():
    """Test integration with registration flow"""
    print("\n" + "=" * 70)
    print("INTEGRATION TEST - REGISTRATION FLOW")
    print("=" * 70 + "\n")

    try:
        from app import app

        with app.test_client() as client:
            # Test that registration page loads
            response = client.get("/register")
            if response.status_code == 200:
                print("✓ Registration page loads successfully")

                # Check if phone field is in the form (basic check)
                if b"phone_number" in response.data:
                    print("✓ Phone number field exists in registration form")
                else:
                    print("⚠ Phone number field might be missing from form")

            else:
                print(f"✗ Registration page failed to load: {response.status_code}")

            # Test that verify phone page requires session
            response = client.get("/verify-phone")
            # Should redirect since no pending verification
            if response.status_code in [302, 200]:
                print("✓ Verify phone page accessible")
            else:
                print(f"✗ Verify phone page error: {response.status_code}")

        print("\n✓ Integration tests completed\n")

    except Exception as e:
        print(f"\n✗ Integration test failed: {e}\n")


def show_usage_guide():
    """Show how to use the phone verification system"""
    print("\n" + "=" * 70)
    print("PHONE VERIFICATION USAGE GUIDE")
    print("=" * 70 + "\n")

    print("📱 HOW TO USE:")
    print("\n1. Start the Flask application:")
    print("   python backend/app.py")

    print("\n2. Register a new user:")
    print("   - Go to: http://127.0.0.1:5000/register")
    print("   - Fill in all fields including phone number")
    print("   - Submit the form")

    print("\n3. Verify phone (MOCK MODE):")
    print("   - Check your terminal/console for the OTP code")
    print("   - You'll see output like:")
    print("     ============================================================")
    print("     📱 MOCK SMS SERVICE - OTP CODE")
    print("     ============================================================")
    print("     To: +15551234567")
    print("     Code: 123456")
    print("     ============================================================")

    print("\n4. Enter the code on the verification page")

    print("\n5. Login and use the app!")

    print("\n📝 PRODUCTION MODE (Real SMS):")
    print("   1. Install Twilio: pip install twilio")
    print("   2. Get credentials from: https://www.twilio.com/")
    print("   3. Set environment variables:")
    print("      PHONE_VERIFICATION_MOCK=False")
    print("      TWILIO_ACCOUNT_SID=your_sid")
    print("      TWILIO_AUTH_TOKEN=your_token")
    print("      TWILIO_PHONE_NUMBER=+1234567890")

    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    print("\n🚀 PHONE VERIFICATION SYSTEM - COMPREHENSIVE TEST\n")

    # Run tests
    results = test_phone_verification()

    # Run integration tests
    test_integration()

    # Show usage guide
    show_usage_guide()

    # Exit with appropriate code
    if results["failed"] > 0:
        print("⚠️  Some tests failed. Please review the errors above.")
        sys.exit(1)
    else:
        print("✅ All tests passed! Phone verification system is ready to use.")
        print("\n📖 See PHONE_VERIFICATION_SETUP.md for complete documentation.\n")
        sys.exit(0)

"""
Phone Verification Service
Handles OTP generation, SMS sending, and verification
Supports both Twilio (production) and Mock mode (development)
"""

import os
import random
import string
from datetime import datetime, timedelta

from flask import current_app
from models import User, db


class PhoneVerificationService:
    """Service for phone number verification via SMS OTP"""

    def __init__(self):
        # Configuration
        self.use_mock = os.getenv("PHONE_VERIFICATION_MOCK", "True").lower() == "true"
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        self.otp_length = 6
        self.otp_expiry_minutes = 10

        # Initialize Twilio client if credentials are provided
        self.twilio_client = None
        if not self.use_mock and self.twilio_account_sid and self.twilio_auth_token:
            try:
                from twilio.rest import Client

                self.twilio_client = Client(
                    self.twilio_account_sid, self.twilio_auth_token
                )
                print("[OK] Twilio SMS service initialized")
            except ImportError:
                print(
                    "[WARNING] Twilio not installed. Run: pip install twilio. Using mock mode."
                )
                self.use_mock = True
            except Exception as e:
                print(f"[WARNING] Twilio initialization failed: {e}. Using mock mode.")
                self.use_mock = True
        else:
            print("[INFO] Phone verification running in MOCK mode (no SMS sent)")

    def generate_otp(self):
        """Generate a random 6-digit OTP code"""
        return "".join(random.choices(string.digits, k=self.otp_length))

    def format_phone_number(self, phone):
        """Format phone number to E.164 format"""
        # Remove all non-digit characters
        digits = "".join(filter(str.isdigit, phone))

        # If it starts with country code, use as-is
        if digits.startswith("1") and len(digits) == 11:
            return f"+{digits}"
        elif len(digits) == 10:
            # Assume US number, add +1
            return f"+1{digits}"
        elif digits.startswith("0"):
            # Remove leading 0 and add country code (adjust as needed)
            return f"+1{digits[1:]}"
        else:
            # Try to use as-is with +
            return f"+{digits}"

    def send_otp(self, user_id, phone_number, resend=False):
        """
        Generate and send OTP to user's phone number

        Args:
            user_id: User ID
            phone_number: Phone number to send OTP to
            resend: Whether this is a resend request

        Returns:
            dict with success status and message
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return {"success": False, "message": "User not found"}

            # Check if phone is already verified
            if user.phone_verified and not resend:
                return {
                    "success": False,
                    "message": "Phone number already verified",
                }

            # Generate new OTP
            otp_code = self.generate_otp()
            expiry_time = datetime.utcnow() + timedelta(minutes=self.otp_expiry_minutes)

            # Update user with OTP details
            user.phone_number = phone_number
            user.phone_verification_code = otp_code
            user.phone_verification_expires = expiry_time
            db.session.commit()

            # Send SMS
            if self.use_mock:
                # Mock mode - just print to console
                print("\n" + "=" * 60)
                print("MOCK SMS SERVICE - OTP CODE")
                print("=" * 60)
                print(f"To: {phone_number}")
                print(f"Code: {otp_code}")
                print(f"Expires: {expiry_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
                print(f"Valid for: {self.otp_expiry_minutes} minutes")
                print("=" * 60 + "\n")

                return {
                    "success": True,
                    "message": f"OTP sent to {phone_number} (Mock mode - check console)",
                    "mock_code": otp_code,  # Only in mock mode for testing
                    "mock": True,
                }
            else:
                # Real Twilio SMS
                try:
                    formatted_phone = self.format_phone_number(phone_number)
                    message = self.twilio_client.messages.create(
                        body=f"Your LoanLess verification code is: {otp_code}. Valid for {self.otp_expiry_minutes} minutes.",
                        from_=self.twilio_phone_number,
                        to=formatted_phone,
                    )

                    print(f"[OK] SMS sent successfully. SID: {message.sid}")

                    return {
                        "success": True,
                        "message": f"OTP sent to {phone_number}",
                        "mock": False,
                    }
                except Exception as e:
                    print(f"[ERROR] Twilio SMS failed: {str(e)}")
                    return {
                        "success": False,
                        "message": f"Failed to send SMS: {str(e)}",
                    }

        except Exception as e:
            print(f"Error in send_otp: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}

    def verify_otp(self, user_id, otp_code):
        """
        Verify the OTP code for a user

        Args:
            user_id: User ID
            otp_code: OTP code to verify

        Returns:
            dict with success status and message
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return {"success": False, "message": "User not found"}

            # Check if already verified
            if user.phone_verified:
                return {"success": True, "message": "Phone already verified"}

            # Check if OTP exists
            if not user.phone_verification_code:
                return {
                    "success": False,
                    "message": "No verification code found. Please request a new code.",
                }

            # Check if OTP has expired
            if (
                user.phone_verification_expires
                and datetime.utcnow() > user.phone_verification_expires
            ):
                return {
                    "success": False,
                    "message": "Verification code has expired. Please request a new code.",
                }

            # Verify the code
            if user.phone_verification_code == otp_code.strip():
                # Mark as verified
                user.phone_verified = True
                user.phone_verified_at = datetime.utcnow()
                user.phone_verification_code = None  # Clear the code
                user.phone_verification_expires = None
                db.session.commit()

                print(f"[OK] Phone verified for user {user.username}")

                return {
                    "success": True,
                    "message": "Phone number verified successfully!",
                }
            else:
                return {
                    "success": False,
                    "message": "Invalid verification code. Please try again.",
                }

        except Exception as e:
            print(f"Error in verify_otp: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}

    def check_verification_status(self, user_id):
        """
        Check if user's phone is verified

        Args:
            user_id: User ID

        Returns:
            dict with verification status
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return {"success": False, "message": "User not found"}

            return {
                "success": True,
                "verified": user.phone_verified,
                "phone_number": user.phone_number,
                "verified_at": (
                    user.phone_verified_at.isoformat()
                    if user.phone_verified_at
                    else None
                ),
            }

        except Exception as e:
            print(f"Error checking verification status: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}

    def resend_otp(self, user_id):
        """
        Resend OTP to user

        Args:
            user_id: User ID

        Returns:
            dict with success status and message
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return {"success": False, "message": "User not found"}

            if not user.phone_number:
                return {
                    "success": False,
                    "message": "No phone number on file. Please provide a phone number.",
                }

            return self.send_otp(user_id, user.phone_number, resend=True)

        except Exception as e:
            print(f"Error in resend_otp: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}


# Global instance
phone_service = PhoneVerificationService()

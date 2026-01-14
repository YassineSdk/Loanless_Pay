from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and personal information"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    user_role = db.Column(db.String(20), default='client', nullable=False)  # 'client', 'funding_party', 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Personal Information Fields
    full_name = db.Column(db.String(200), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    address = db.Column(db.Text, nullable=True)
    gender = db.Column(db.String(20), nullable=True)  # 'male', 'female', 'other'
    phone_number = db.Column(db.String(20), nullable=True)
    nationality = db.Column(db.String(100), nullable=True)
    national_id_number = db.Column(db.String(100), nullable=True)
    profile_completed = db.Column(db.Boolean, default=False, nullable=False)

    # KYC Verification (One-time process)
    kyc_status = db.Column(db.String(20), default='pending', nullable=False)  # pending, approved, rejected
    kyc_submitted = db.Column(db.Boolean, default=False, nullable=False)
    kyc_submitted_at = db.Column(db.DateTime, nullable=True)
    kyc_approved_at = db.Column(db.DateTime, nullable=True)
    kyc_approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Funding Party Specific Fields
    company_name = db.Column(db.String(200), nullable=True)
    company_registration = db.Column(db.String(100), nullable=True)
    initial_funding = db.Column(db.Float, default=0.0, nullable=True)

    # Relationship with loans
    loans = db.relationship(
        "Loan", backref="user", lazy=True, foreign_keys="Loan.user_id"
    )
    approved_loans = db.relationship(
        "Loan", backref="approver", lazy=True, foreign_keys="Loan.approved_by"
    )
    funding_transactions = db.relationship(
        "FundingTransaction", backref="funder", lazy=True, foreign_keys="FundingTransaction.funder_id"
    )
    kyc_approver = db.relationship(
        "User", remote_side="User.id", foreign_keys=[kyc_approved_by], backref="approved_kyc_users"
    )
    loan_applications = db.relationship(
        "LoanApplication", backref="applicant", lazy=True, foreign_keys="LoanApplication.user_id"
    )

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "user_role": self.user_role,
            "profile_completed": self.profile_completed,
            "full_name": self.full_name,
            "company_name": self.company_name,
            # Add other fields as needed for the frontend
        }

    def __repr__(self):
        return f"<User {self.username}>"


class Loan(db.Model):
    """Loan model for storing loan subscriptions with professional info and documents"""

    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Basic Loan Information
    amount = db.Column(db.Float, nullable=False)
    work_years = db.Column(db.Integer, nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    payment_period = db.Column(db.Integer, nullable=False)  # in months
    monthly_payment = db.Column(db.Float, nullable=False)
    status = db.Column(
        db.String(20), default="pending"
    )  # 'pending', 'approved', 'rejected', 'active', 'completed'

    # Professional Information
    job_title = db.Column(db.String(200), nullable=True)
    salary_range = db.Column(db.String(50), nullable=True)
    has_other_debts = db.Column(db.Boolean, default=False, nullable=True)
    owns_house = db.Column(db.Boolean, default=False, nullable=True)
    number_of_children = db.Column(db.Integer, default=0, nullable=True)

    # Document Uploads (storing file paths)
    id_document = db.Column(db.String(500), nullable=True)  # ID or Passport
    payment_statements = db.Column(db.Text, nullable=True)  # JSON array of file paths

    # Admin fields
    admin_notes = db.Column(db.Text, nullable=True)
    approved_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "monthly_payment": self.monthly_payment,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "payment_period": self.payment_period
        }

    def __repr__(self):
        return f"<Loan {self.id} - ${self.amount}>"


class FundingParty(db.Model):
    """Model for managing external funding parties (legacy - being deprecated)"""
    __tablename__ = "funding_parties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    capital_available = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default="interested") # interested, confirmed, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "contact_email": self.contact_email,
            "phone": self.phone,
            "capital_available": self.capital_available,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }


class FundingTransaction(db.Model):
    """Model for tracking funding deposits by funding parties"""
    __tablename__ = "funding_transactions"

    id = db.Column(db.Integer, primary_key=True)
    funder_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(20), default="deposit")  # deposit, withdrawal, adjustment
    status = db.Column(db.String(20), default="completed")  # pending, completed, failed
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    processed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "funder_id": self.funder_id,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }


class FundingUsage(db.Model):
    """Model for tracking how funding is consumed by loans"""
    __tablename__ = "funding_usage"

    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey("loans.id"), nullable=False)
    amount_used = db.Column(db.Float, nullable=False)
    usage_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default="active")  # active, repaid, defaulted
    notes = db.Column(db.Text, nullable=True)

    # Relationship
    loan = db.relationship("Loan", backref="funding_usage_records", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "loan_id": self.loan_id,
            "amount_used": self.amount_used,
            "usage_date": self.usage_date.isoformat(),
            "status": self.status,
            "notes": self.notes
        }


class KYCDocument(db.Model):
    """Model for storing KYC documents (one-time verification)"""
    __tablename__ = "kyc_documents"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)  # national_id, passport, proof_of_address
    document_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=True)
    mime_type = db.Column(db.String(100), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    user = db.relationship("User", backref="kyc_documents")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "document_type": self.document_type,
            "document_name": self.document_name,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None
        }

    def __repr__(self):
        return f"<KYCDocument {self.document_type} - User {self.user_id}>"


class LoanApplication(db.Model):
    """Model for managing loan applications (3-phase financial audit system)"""
    __tablename__ = "loan_applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Application status
    status = db.Column(db.String(20), default="pending", nullable=False)  # pending, approved, rejected, active, completed

    # Phase Management
    current_phase = db.Column(db.Integer, default=1, nullable=False)  # 1=KYC, 2=Financial, 3=Decision
    overall_status = db.Column(db.String(20), default="in_progress", nullable=False)  # in_progress, completed, cancelled

    # Phase 1: KYC Status
    kyc_status = db.Column(db.String(20), default="pending", nullable=False)  # pending, approved, rejected
    kyc_submitted_at = db.Column(db.DateTime, nullable=True)
    kyc_approved_at = db.Column(db.DateTime, nullable=True)
    kyc_approved_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    kyc_notes = db.Column(db.Text, nullable=True)

    # Phase 2: Financial Status
    financial_status = db.Column(db.String(20), default="not_started", nullable=False)  # not_started, pending, approved, rejected
    financial_submitted_at = db.Column(db.DateTime, nullable=True)
    financial_approved_at = db.Column(db.DateTime, nullable=True)
    financial_approved_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    financial_notes = db.Column(db.Text, nullable=True)

    # Phase 3: Decision Status
    decision_status = db.Column(db.String(20), default="not_started", nullable=False)  # not_started, pending, approved, rejected
    final_decision = db.Column(db.String(20), nullable=True)  # accepted, rejected
    decision_made_at = db.Column(db.DateTime, nullable=True)
    decision_made_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    decision_notes = db.Column(db.Text, nullable=True)

    # Personal Information (from Phase 1 - KYC)
    full_name = db.Column(db.String(200), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    nationality = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    national_id_number = db.Column(db.String(50), nullable=True)

    # Loan Request Details (from Phase 2 - Financial)
    loan_amount_requested = db.Column(db.Float, nullable=True)
    loan_purpose = db.Column(db.Text, nullable=True)
    loan_duration_months = db.Column(db.Integer, nullable=True)

    # Financial Information (from Phase 2)
    monthly_income = db.Column(db.Float, nullable=True)
    employment_status = db.Column(db.String(100), nullable=True)
    employer_name = db.Column(db.String(200), nullable=True)
    has_other_loans = db.Column(db.Boolean, default=False)
    other_loans_amount = db.Column(db.Float, nullable=True)

    # Approved Loan Terms (from Phase 3 - Decision)
    approved_amount = db.Column(db.Float, nullable=True)
    approved_duration = db.Column(db.Integer, nullable=True)
    interest_rate = db.Column(db.Float, nullable=True)
    monthly_payment = db.Column(db.Float, nullable=True)

    # Admin Review (Legacy - kept for compatibility)
    reviewed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    user = db.relationship("User", foreign_keys=[user_id], overlaps="applicant,loan_applications")
    reviewer = db.relationship("User", foreign_keys=[reviewed_by], backref="reviewed_loan_applications")
    kyc_approver = db.relationship("User", foreign_keys=[kyc_approved_by], backref="kyc_approved_applications")
    financial_approver = db.relationship("User", foreign_keys=[financial_approved_by], backref="financial_approved_applications")
    decision_maker = db.relationship("User", foreign_keys=[decision_made_by], backref="decision_made_applications")
    documents = db.relationship("LoanDocument", backref="loan_application", lazy=True, cascade="all, delete-orphan")

    def can_proceed_to_phase_2(self):
        """Check if application can move to Phase 2 (Financial)"""
        return self.kyc_status == "approved"

    def can_proceed_to_phase_3(self):
        """Check if application can move to Phase 3 (Decision)"""
        return self.kyc_status == "approved" and self.financial_status == "approved"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status,
            "current_phase": self.current_phase,
            "overall_status": self.overall_status,
            "kyc_status": self.kyc_status,
            "financial_status": self.financial_status,
            "decision_status": self.decision_status,
            "final_decision": self.final_decision,
            "full_name": self.full_name,
            "loan_amount_requested": self.loan_amount_requested,
            "loan_purpose": self.loan_purpose,
            "loan_duration_months": self.loan_duration_months,
            "monthly_income": self.monthly_income,
            "employment_status": self.employment_status,
            "approved_amount": self.approved_amount,
            "approved_duration": self.approved_duration,
            "interest_rate": self.interest_rate,
            "monthly_payment": self.monthly_payment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<LoanApplication {self.id} - {self.status}>"


class LoanDocument(db.Model):
    """Model for storing loan application documents (KYC + Financial)"""
    __tablename__ = "loan_documents"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("loan_applications.id"), nullable=False)
    phase = db.Column(db.Integer, nullable=False, default=1)  # 1=KYC, 2=Financial
    document_type = db.Column(db.String(100), nullable=False)  # national_id, proof_of_address, selfie, bank_statement, proof_of_income, etc.
    document_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=True)
    mime_type = db.Column(db.String(100), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "application_id": self.application_id,
            "document_type": self.document_type,
            "document_name": self.document_name,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None
        }

    def __repr__(self):
        return f"<LoanDocument {self.document_type} - Application {self.application_id}>"

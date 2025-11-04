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
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Personal Information Fields
    full_name = db.Column(db.String(200), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    address = db.Column(db.Text, nullable=True)
    gender = db.Column(db.String(20), nullable=True)  # 'male', 'female', 'other'
    phone_number = db.Column(db.String(20), nullable=True)
    profile_completed = db.Column(db.Boolean, default=False, nullable=False)

    # Relationship with loans
    loans = db.relationship(
        "Loan", backref="user", lazy=True, foreign_keys="Loan.user_id"
    )
    approved_loans = db.relationship(
        "Loan", backref="approver", lazy=True, foreign_keys="Loan.approved_by"
    )

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

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

    def __repr__(self):
        return f"<Loan {self.id} - ${self.amount}>"

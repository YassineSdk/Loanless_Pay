from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # Relationship with loans
    loans = db.relationship('Loan', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Loan(db.Model):
    """Loan model for storing loan subscriptions"""
    __tablename__ = 'loans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    work_years = db.Column(db.Integer, nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    payment_period = db.Column(db.Integer, nullable=False)  # in months
    monthly_payment = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='draft')  # 'draft' or 'accepted'
    
    def __repr__(self):
        return f'<Loan {self.id} - ${self.amount}>'



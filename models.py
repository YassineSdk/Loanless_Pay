from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_premium = db.Column(db.Boolean, default=False)
    advances = db.relationship('Advance', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Advance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    commission = db.Column(db.Float, nullable=False)
    total_repayment = db.Column(db.Float, nullable=False)
    installments = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    contract_id = db.Column(db.String(50), unique=True)
    payments = db.relationship('Payment', backref='advance', lazy=True)

    def __repr__(self):
        return f'<Advance {self.id} - ${self.amount}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advance_id = db.Column(db.Integer, db.ForeignKey('advance.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    paid_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue
    reminder_sent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Payment {self.id} - ${self.amount}>'

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    contact_name = db.Column(db.String(100))
    subscription_type = db.Column(db.String(20), default='basic')  # basic, premium
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Subscription {self.company_name}>'
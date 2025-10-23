from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login_manager
from models import User, Advance, Payment, Subscription
from datetime import datetime, timedelta
import uuid
from simulation import calculate_advance_details
import os
from contract_generator import generate_contract

# Add current datetime to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        
        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    advances = Advance.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', advances=advances)

@app.route('/simulate', methods=['GET', 'POST'])
@login_required
def simulate():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        installments = int(request.form.get('installments'))
        
        simulation_result = calculate_advance_details(amount, installments)
        
        return render_template('simulate.html', simulation=simulation_result)
    
    return render_template('simulate.html')

@app.route('/request_advance', methods=['GET', 'POST'])
@login_required
def request_advance():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        installments = int(request.form.get('installments'))
        
        # Calculate advance details
        advance_details = calculate_advance_details(amount, installments)
        
        # Create new advance
        new_advance = Advance(
            user_id=current_user.id,
            amount=amount,
            commission=advance_details['commission'],
            total_repayment=advance_details['total_repayment'],
            installments=installments,
            contract_id=str(uuid.uuid4())
        )
        
        db.session.add(new_advance)
        db.session.commit()
        
        # Create payment schedule
        for i, payment_date in enumerate(advance_details['payment_dates']):
            payment = Payment(
                advance_id=new_advance.id,
                amount=advance_details['installment_amount'],
                due_date=payment_date,
                status='pending'
            )
            db.session.add(payment)
        
        db.session.commit()
        
        # Generate contract
        contract_path = generate_contract(new_advance, current_user, advance_details)
        
        flash('Advance request submitted successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('request_advance.html')

@app.route('/advance/<int:advance_id>')
@login_required
def advance_details(advance_id):
    advance = Advance.query.get_or_404(advance_id)
    
    # Ensure user can only view their own advances
    if advance.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('dashboard'))
    
    payments = Payment.query.filter_by(advance_id=advance_id).all()
    
    return render_template('advance_details.html', advance=advance, payments=payments)

@app.route('/admin/subscriptions', methods=['GET', 'POST'])
@login_required
def manage_subscriptions():
    # Admin only route
    if not current_user.is_admin:
        flash('Unauthorized access')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        contact_email = request.form.get('contact_email')
        contact_name = request.form.get('contact_name')
        subscription_type = request.form.get('subscription_type')
        
        # Create new subscription
        new_subscription = Subscription(
            company_name=company_name,
            contact_email=contact_email,
            contact_name=contact_name,
            subscription_type=subscription_type,
            end_date=datetime.utcnow() + timedelta(days=365)  # 1 year subscription
        )
        
        db.session.add(new_subscription)
        db.session.commit()
        
        flash('Subscription added successfully!')
        return redirect(url_for('manage_subscriptions'))
    
    subscriptions = Subscription.query.all()
    return render_template('admin/subscriptions.html', subscriptions=subscriptions)
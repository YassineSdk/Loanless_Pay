from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Loan
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'loanless-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


@app.route('/')
def index():
    """Main/home page"""
    if current_user.is_authenticated:
        return render_template('main.html')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Login successful!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('login.html', register=True)
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('login.html', register=True)
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('login.html', register=True)
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('login.html', register=True)


@app.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/main')
@login_required
def main():
    """Main dashboard page after login"""
    return render_template('main.html')


@app.route('/simulate', methods=['GET', 'POST'])
@login_required
def simulate():
    """Loan simulation page"""
    if request.method == 'POST':
        # Handle form submission
        if request.form.get('action') == 'subscribe':
            # Save to database
            amount = float(request.form.get('amount'))
            work_years = int(request.form.get('work_years'))
            sector = request.form.get('sector')
            payment_period = int(request.form.get('payment_period'))
            monthly_payment = float(request.form.get('monthly_payment'))
            
            loan = Loan(
                user_id=current_user.id,
                amount=amount,
                work_years=work_years,
                sector=sector,
                payment_period=payment_period,
                monthly_payment=monthly_payment,
                status='draft'
            )
            
            db.session.add(loan)
            db.session.commit()
            
            flash('Loan subscription saved successfully!', 'success')
            return redirect(url_for('dashboard'))
        elif request.form.get('action') == 'cancel':
            return redirect(url_for('main'))
    
    return render_template('simulate.html')


@app.route('/calculate', methods=['POST'])
@login_required
def calculate():
    """Calculate monthly payment via AJAX"""
    try:
        amount = float(request.json.get('amount', 0))
        payment_period = int(request.json.get('payment_period', 1))
        
        # Calculate: (amount + amount * 0.02) / payment_period
        monthly_payment = (amount + (amount * 0.02)) / payment_period
        
        return jsonify({
            'success': True,
            'monthly_payment': round(monthly_payment, 2)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing their loans"""
    loans = Loan.query.filter_by(user_id=current_user.id).order_by(Loan.id.desc()).all()
    return render_template('dashboard.html', loans=loans)


@app.route('/loan/delete/<int:loan_id>', methods=['POST'])
@login_required
def delete_loan(loan_id):
    """Delete a loan"""
    loan = Loan.query.get_or_404(loan_id)
    
    # Ensure user owns the loan
    if loan.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    db.session.delete(loan)
    db.session.commit()
    
    flash('Loan deleted successfully', 'success')
    return redirect(url_for('dashboard'))


def init_db():
    """Initialize database and create tables"""
    with app.app_context():
        db.create_all()
        
        # Create a demo user if it doesn't exist
        if not User.query.filter_by(username='demo').first():
            demo_user = User(username='demo', email='demo@loanless.com')
            demo_user.set_password('demo123')
            db.session.add(demo_user)
            db.session.commit()
            print("Demo user created: username='demo', password='demo123'")
        
        print("Database initialized successfully!")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)



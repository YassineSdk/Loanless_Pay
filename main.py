from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loanless.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    loans = db.relationship('Loan', backref='user', lazy=True)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in months
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/simulate', methods=['GET', 'POST'])
def simulate():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        duration = int(request.form['duration'])
        commission = amount * 0.02  # 2% commission
        monthly_payment = amount / duration
        return render_template('simulate.html', 
                             amount=amount,
                             duration=duration,
                             commission=commission,
                             monthly_payment=monthly_payment)
    return render_template('simulate.html')

@app.route('/apply', methods=['POST'])
def apply_loan():
    # Add loan application logic here
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


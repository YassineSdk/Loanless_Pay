from flask import Flask, request, jsonify, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from models import db, User, Loan, FundingParty
from admin import admin
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask_cors import CORS
import os
import json
import calendar

app = Flask(__name__)
app.config["SECRET_KEY"] = "loanless-secret-key-2024"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Enable CORS
CORS(app, supports_credentials=True)

# File upload configuration
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = "login" # Not needed for API, we handle 401 manually or let default handle it

# Register admin blueprint
app.register_blueprint(admin)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def add_months(start_date, months):
    """
    Add months to a date safely, handling month/year rollover.
    If the target day doesn't exist in the target month, uses the last day of that month.
    """
    # Calculate target month and year
    month = start_date.month - 1 + months
    year = start_date.year + month // 12
    month = month % 12 + 1

    # Get the last day of the target month
    last_day = calendar.monthrange(year, month)[1]

    # Use the original day or the last day of month, whichever is smaller
    day = min(start_date.day, last_day)

    return start_date.replace(year=year, month=month, day=day)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Unauthorized", "message": "Please log in to access this resource"}), 401


@app.route("/api/auth/status")
def auth_status():
    if current_user.is_authenticated:
        return jsonify({
            "is_authenticated": True,
            "user": current_user.to_dict()
        })
    return jsonify({"is_authenticated": False})


@app.route("/api/login", methods=["POST"])
def login():
    """Login API"""
    if current_user.is_authenticated:
        return jsonify({"success": True, "message": "Already logged in", "user": current_user.to_dict()})

    data = request.json
    username = data.get("username")
    password = data.get("password")
    remember = data.get("remember", False)

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        if not user.is_active:
            return jsonify({"success": False, "message": "Account deactivated"}), 403

        login_user(user, remember=remember)
        return jsonify({"success": True, "message": "Login successful", "user": user.to_dict()})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401


@app.route("/api/register", methods=["POST"])
def register():
    """Registration API"""
    if current_user.is_authenticated:
        return jsonify({"success": False, "message": "Already logged in"})

    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "Username already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"success": True, "message": "Registration successful"})


@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    """Logout API"""
    logout_user()
    return jsonify({"success": True, "message": "Logged out successfully"})


@app.route("/api/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User profile API"""
    if request.method == "GET":
        return jsonify({
            "success": True, 
            "user": current_user.to_dict(),
            "profile_completed": current_user.profile_completed
            # Add specific fields if they are not in to_dict() or if you want to be explicit
        })
    
    # POST
    data = request.json
    current_user.email = data.get("email", current_user.email)
    current_user.full_name = data.get("full_name", current_user.full_name)

    dob_str = data.get("date_of_birth")
    if dob_str:
        try:
            current_user.date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            pass # Handle error appropriately

    current_user.gender = data.get("gender", current_user.gender)
    current_user.phone_number = data.get("phone_number", current_user.phone_number)
    current_user.address = data.get("address", current_user.address)

    if all([
        current_user.full_name,
        current_user.date_of_birth,
        current_user.gender,
        current_user.phone_number,
        current_user.address,
    ]):
        current_user.profile_completed = True

    db.session.commit()
    return jsonify({"success": True, "message": "Profile updated", "user": current_user.to_dict()})


@app.route("/api/simulate", methods=["POST"])
@login_required
def simulate():
    """Loan simulation and application API"""
    if not current_user.profile_completed:
        return jsonify({"success": False, "message": "Profile incomplete"}), 403

    # Handle file uploads (Form Data)
    # Since files are involved, this endpoint expects multipart/form-data, not JSON
    
    amount = float(request.form.get("amount"))
    work_years = int(request.form.get("work_years"))
    sector = request.form.get("sector")
    payment_period = int(request.form.get("payment_period"))
    monthly_payment = float(request.form.get("monthly_payment"))
    
    job_title = request.form.get("job_title")
    salary_range = request.form.get("salary_range")
    has_other_debts = request.form.get("has_other_debts") == "true"
    owns_house = request.form.get("owns_house") == "true"
    number_of_children = int(request.form.get("number_of_children", 0))

    id_document_path = None
    payment_statements_paths = []

    if "id_document" in request.files:
        id_file = request.files["id_document"]
        if id_file and id_file.filename and allowed_file(id_file.filename):
            filename = secure_filename(
                f"{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_id_{id_file.filename}"
            )
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            id_file.save(filepath)
            id_document_path = filename # Store relative path or filename

    if "payment_statements" in request.files:
        files = request.files.getlist("payment_statements")
        for idx, file in enumerate(files):
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(
                    f"{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_statement_{idx}_{file.filename}"
                )
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                payment_statements_paths.append(filename)

    loan = Loan(
        user_id=current_user.id,
        amount=amount,
        work_years=work_years,
        sector=sector,
        payment_period=payment_period,
        monthly_payment=monthly_payment,
        status="pending",
        job_title=job_title,
        salary_range=salary_range,
        has_other_debts=has_other_debts,
        owns_house=owns_house,
        number_of_children=number_of_children,
        id_document=id_document_path,
        payment_statements=json.dumps(payment_statements_paths) if payment_statements_paths else None,
    )

    db.session.add(loan)
    db.session.commit()

    return jsonify({"success": True, "message": "Loan application submitted"})


@app.route("/api/calculate", methods=["POST"])
def calculate():
    """Calculate monthly payment API"""
    try:
        amount = float(request.json.get("amount", 0))
        payment_period = int(request.json.get("payment_period", 1))

        monthly_payment = (amount + (amount * 0.02)) / payment_period

        return jsonify({"success": True, "monthly_payment": round(monthly_payment, 2)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/dashboard")
@login_required
def dashboard():
    """User dashboard data API"""
    loans = Loan.query.filter_by(user_id=current_user.id).order_by(Loan.id.desc()).all()
    loans_data = []
    
    for loan in loans:
        loan_dict = loan.to_dict()
        loan_dict["schedule"] = []
        
        if loan.status in ["approved", "active"]:
            for month in range(1, loan.payment_period + 1):
                due_date = add_months(loan.created_at, month)
                payment_data = {
                    "month": month,
                    "amount": loan.monthly_payment,
                    "due_date": due_date.strftime("%b %d, %Y"),
                    "status": "paid" if month <= 3 else "pending", 
                }
                loan_dict["schedule"].append(payment_data)
        
        loans_data.append(loan_dict)

    return jsonify({"success": True, "loans": loans_data})

# --- Funding Party Endpoints ---

@app.route("/api/funding-inquiry", methods=["POST"])
def funding_inquiry():
    """Public endpoint for potential investors"""
    data = request.json
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    capital = float(data.get("capital_available", 0))

    if not name or not email:
        return jsonify({"success": False, "message": "Name and Email are required"}), 400

    party = FundingParty(
        name=name,
        contact_email=email,
        phone=phone,
        capital_available=capital
    )
    db.session.add(party)
    db.session.commit()

    return jsonify({"success": True, "message": "Inquiry received. We will contact you soon."})


@app.route("/api/admin/funding-parties", methods=["GET"])
@login_required
def admin_funding_parties():
    """Admin endpoint to list funding parties"""
    if not current_user.is_admin:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
        
    parties = FundingParty.query.order_by(FundingParty.created_at.desc()).all()
    return jsonify({"success": True, "parties": [p.to_dict() for p in parties]})


def init_db():
    """Initialize database and create tables"""
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(username="demo").first():
            demo_user = User(username="demo", email="demo@loanless.com")
            demo_user.set_password("demo123")
            db.session.add(demo_user)
            db.session.commit()
            print("Demo user created")

        if not User.query.filter_by(username="admin").first():
            admin_user = User(
                username="admin", email="admin@loanless.com", is_admin=True
            )
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created")
            
        print("Database initialized successfully!")


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)

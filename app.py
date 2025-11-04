from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from models import db, User, Loan
from admin import admin
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json
import calendar

app = Flask(__name__)
app.config["SECRET_KEY"] = "loanless-secret-key-2024"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

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


@app.template_filter("from_json")
def from_json_filter(value):
    """Convert JSON string to Python object"""
    if value:
        try:
            return json.loads(value)
        except:
            return []
    return []


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


@app.route("/")
def index():
    """Landing page / Main page"""
    if current_user.is_authenticated:
        # Redirect admin users to admin dashboard
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return render_template("main.html")
    # Show landing page for non-authenticated users
    return render_template("landing.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for("main"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = request.form.get("remember")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # Check if user account is active
            if not user.is_active:
                flash(
                    "Your account has been deactivated. Please contact support.",
                    "error",
                )
                return render_template("login.html")

            login_user(user, remember=remember)
            flash("Login successful!", "success")

            # Smart redirect based on user role
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)

            if user.is_admin:
                return redirect(url_for("admin.dashboard"))
            else:
                return redirect(url_for("main"))
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration page"""
    if current_user.is_authenticated:
        return redirect(url_for("main"))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validation
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template("login.html", register=True)

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "error")
            return render_template("login.html", register=True)

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return render_template("login.html", register=True)

        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("login.html", register=True)


@app.route("/logout")
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("login"))


@app.route("/main")
@login_required
def main():
    """Main dashboard page after login"""
    return render_template("main.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User profile page"""
    if request.method == "POST":
        # Update user profile
        current_user.email = request.form.get("email")
        current_user.full_name = request.form.get("full_name")

        # Parse date of birth
        dob_str = request.form.get("date_of_birth")
        if dob_str:
            current_user.date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()

        current_user.gender = request.form.get("gender")
        current_user.phone_number = request.form.get("phone_number")
        current_user.address = request.form.get("address")

        # Mark profile as completed if all required fields are filled
        if all(
            [
                current_user.full_name,
                current_user.date_of_birth,
                current_user.gender,
                current_user.phone_number,
                current_user.address,
            ]
        ):
            current_user.profile_completed = True

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html")


@app.route("/simulate", methods=["GET", "POST"])
@login_required
def simulate():
    """Loan simulation page with professional info and documents"""
    if request.method == "POST":
        # Handle form submission
        if request.form.get("action") == "subscribe":
            # Check if profile is completed
            if not current_user.profile_completed:
                flash(
                    "Please complete your profile before applying for a loan.", "error"
                )
                return redirect(url_for("profile"))

            # Save basic loan info
            amount = float(request.form.get("amount"))
            work_years = int(request.form.get("work_years"))
            sector = request.form.get("sector")
            payment_period = int(request.form.get("payment_period"))
            monthly_payment = float(request.form.get("monthly_payment"))

            # Professional information
            job_title = request.form.get("job_title")
            salary_range = request.form.get("salary_range")
            has_other_debts = request.form.get("has_other_debts") == "true"
            owns_house = request.form.get("owns_house") == "true"
            number_of_children = int(request.form.get("number_of_children", 0))

            # Handle file uploads
            id_document_path = None
            payment_statements_paths = []

            # Upload ID document
            if "id_document" in request.files:
                id_file = request.files["id_document"]
                if id_file and id_file.filename and allowed_file(id_file.filename):
                    filename = secure_filename(
                        f"{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_id_{id_file.filename}"
                    )
                    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                    id_file.save(filepath)
                    id_document_path = filepath

            # Upload payment statements (multiple files)
            if "payment_statements" in request.files:
                files = request.files.getlist("payment_statements")
                for idx, file in enumerate(files):
                    if file and file.filename and allowed_file(file.filename):
                        filename = secure_filename(
                            f"{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_statement_{idx}_{file.filename}"
                        )
                        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                        file.save(filepath)
                        payment_statements_paths.append(filepath)

            # Create loan record
            loan = Loan(
                user_id=current_user.id,
                amount=amount,
                work_years=work_years,
                sector=sector,
                payment_period=payment_period,
                monthly_payment=monthly_payment,
                status="pending",
                # Professional info
                job_title=job_title,
                salary_range=salary_range,
                has_other_debts=has_other_debts,
                owns_house=owns_house,
                number_of_children=number_of_children,
                # Documents
                id_document=id_document_path,
                payment_statements=json.dumps(payment_statements_paths)
                if payment_statements_paths
                else None,
            )

            db.session.add(loan)
            db.session.commit()

            flash(
                "Loan application submitted successfully! You will be notified once reviewed.",
                "success",
            )
            return redirect(url_for("dashboard"))
        elif request.form.get("action") == "cancel":
            return redirect(url_for("main"))

    return render_template("simulate.html")


@app.route("/calculate", methods=["POST"])
@login_required
def calculate():
    """Calculate monthly payment via AJAX"""
    try:
        amount = float(request.json.get("amount", 0))
        payment_period = int(request.json.get("payment_period", 1))

        # Calculate: (amount + amount * 0.02) / payment_period
        monthly_payment = (amount + (amount * 0.02)) / payment_period

        return jsonify({"success": True, "monthly_payment": round(monthly_payment, 2)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/dashboard")
@login_required
def dashboard():
    """User dashboard showing their loans with payment schedules"""
    loans = Loan.query.filter_by(user_id=current_user.id).order_by(Loan.id.desc()).all()

    # Calculate payment schedules for approved/active loans
    loans_with_schedules = []
    for loan in loans:
        loan_data = {"loan": loan, "schedule": []}

        # Generate payment schedule only for approved or active loans
        if loan.status in ["approved", "active"]:
            for month in range(1, loan.payment_period + 1):
                # Calculate due date safely
                due_date = add_months(loan.created_at, month)

                payment_data = {
                    "month": month,
                    "amount": loan.monthly_payment,
                    "due_date": due_date.strftime("%b %d, %Y"),
                    "status": "paid" if month <= 3 else "pending",  # Mock: first 3 paid
                }
                loan_data["schedule"].append(payment_data)

        loans_with_schedules.append(loan_data)

    return render_template("dashboard.html", loans_with_schedules=loans_with_schedules)


@app.route("/uploads/<path:filename>")
@login_required
def uploaded_file(filename):
    """Serve uploaded files - only to file owner or admins"""
    from flask import send_from_directory

    # Check if user is admin or owns the file
    if current_user.is_admin:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    # Check if the file belongs to the current user
    user_id_str = str(current_user.id)
    if filename.startswith(user_id_str + "_"):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    # Unauthorized
    flash("Unauthorized access to file", "error")
    return redirect(url_for("dashboard"))


@app.route("/loan/delete/<int:loan_id>", methods=["POST"])
@login_required
def delete_loan(loan_id):
    """Delete a loan"""
    loan = Loan.query.get_or_404(loan_id)

    # Ensure user owns the loan
    if loan.user_id != current_user.id:
        flash("Unauthorized access", "error")
        return redirect(url_for("dashboard"))

    db.session.delete(loan)
    db.session.commit()

    flash("Loan deleted successfully", "success")
    return redirect(url_for("dashboard"))


def init_db():
    """Initialize database and create tables"""
    with app.app_context():
        db.create_all()

        # Create a demo user if it doesn't exist
        if not User.query.filter_by(username="demo").first():
            demo_user = User(username="demo", email="demo@loanless.com")
            demo_user.set_password("demo123")
            db.session.add(demo_user)
            db.session.commit()
            print("Demo user created: username='demo', password='demo123'")

        # Create an admin user if it doesn't exist
        if not User.query.filter_by(username="admin").first():
            admin_user = User(
                username="admin", email="admin@loanless.com", is_admin=True
            )
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created: username='admin', password='admin123'")

        print("Database initialized successfully!")


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)

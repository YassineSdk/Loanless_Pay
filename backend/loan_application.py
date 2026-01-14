import os
from datetime import datetime

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import current_user, login_required
from models import LoanApplication, LoanDocument, User, db
from werkzeug.utils import secure_filename

loan_app = Blueprint("loan_app", __name__, url_prefix="/loan-application")

# File upload configuration
UPLOAD_FOLDER = os.path.join("static", "loan_documents")
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "doc", "docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_size(file):
    """Get file size in bytes"""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size


def check_kyc_approved():
    """Check if current user has approved KYC"""
    if current_user.kyc_status != "approved":
        return False
    return True


# ============================================================================
# USER-FACING ROUTES - Loan Applications
# ============================================================================


@loan_app.route("/")
@login_required
def index():
    """Loan application dashboard"""
    # Check KYC status
    if current_user.kyc_status != "approved":
        flash(
            "You must complete KYC verification before applying for a loan.", "warning"
        )
        return redirect(url_for("kyc.index"))

    # Get user's most recent active loan application
    application = (
        LoanApplication.query.filter_by(user_id=current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .first()
    )

    return render_template(
        "loan_application/index.html", application=application, user=current_user
    )


@loan_app.route("/phase1-kyc")
@login_required
def phase1_kyc():
    """Phase 1: KYC Verification page"""
    # Get user's most recent application
    application = (
        LoanApplication.query.filter_by(user_id=current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .first()
    )

    if not application:
        flash("Please start a loan application first.", "warning")
        return redirect(url_for("loan_app.apply"))

    # Verify ownership
    if application.user_id != current_user.id:
        flash("Unauthorized access", "error")
        return redirect(url_for("loan_app.index"))

    return render_template(
        "loan_application/phase1_kyc.html", application=application, user=current_user
    )


@loan_app.route("/phase2-financial")
@login_required
def phase2_financial():
    """Phase 2: Financial Documents page"""
    # Get user's most recent application
    application = (
        LoanApplication.query.filter_by(user_id=current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .first()
    )

    if not application:
        flash("Please start a loan application first.", "warning")
        return redirect(url_for("loan_app.apply"))

    # Verify ownership
    if application.user_id != current_user.id:
        flash("Unauthorized access", "error")
        return redirect(url_for("loan_app.index"))

    # Check if can proceed to phase 2
    if not application.can_proceed_to_phase_2():
        flash("You must complete Phase 1 (KYC) first.", "warning")
        return redirect(url_for("loan_app.phase1_kyc"))

    # Get documents
    documents = LoanDocument.query.filter_by(application_id=application.id).all()

    return render_template(
        "loan_application/phase2_financial.html",
        application=application,
        documents=documents,
        user=current_user,
    )


@loan_app.route("/phase3-decision")
@login_required
def phase3_decision():
    """Phase 3: Loan Decision page"""
    # Get user's most recent application
    application = (
        LoanApplication.query.filter_by(user_id=current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .first()
    )

    if not application:
        flash("Please start a loan application first.", "warning")
        return redirect(url_for("loan_app.apply"))

    # Verify ownership
    if application.user_id != current_user.id:
        flash("Unauthorized access", "error")
        return redirect(url_for("loan_app.index"))

    # Check if can proceed to phase 3
    if not application.can_proceed_to_phase_3():
        flash("You must complete Phase 2 (Financial Documents) first.", "warning")
        return redirect(url_for("loan_app.phase2_financial"))

    return render_template(
        "loan_application/phase3_decision.html",
        application=application,
        user=current_user,
    )


@loan_app.route("/submit-phase1", methods=["POST"])
@login_required
def submit_phase1():
    """Submit Phase 1 (KYC) personal information"""
    # Get user's most recent application
    application = (
        LoanApplication.query.filter_by(user_id=current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .first()
    )

    if not application:
        flash("Please start a loan application first.", "warning")
        return redirect(url_for("loan_app.apply"))

    try:
        # Update application with KYC info
        application.full_name = request.form.get("full_name")
        application.date_of_birth = request.form.get("date_of_birth")
        application.nationality = request.form.get("nationality")
        application.national_id_number = request.form.get("national_id_number")
        application.phone_number = request.form.get("phone_number")
        application.address = request.form.get("address")
        application.kyc_submitted_at = datetime.utcnow()
        application.kyc_status = "pending"

        db.session.commit()

        flash("KYC information saved successfully!", "success")
        return redirect(url_for("loan_app.phase1_kyc"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error saving KYC information: {str(e)}", "error")
        return redirect(url_for("loan_app.phase1_kyc"))


@loan_app.route("/submit-phase2", methods=["POST"])
@login_required
def submit_phase2():
    """Submit Phase 2 (Financial) information"""
    # Get user's most recent application
    application = (
        LoanApplication.query.filter_by(user_id=current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .first()
    )

    if not application:
        flash("Please start a loan application first.", "warning")
        return redirect(url_for("loan_app.apply"))

    if not application.can_proceed_to_phase_2():
        flash("You must complete Phase 1 (KYC) first.", "warning")
        return redirect(url_for("loan_app.phase1_kyc"))

    try:
        # Update application with financial info
        application.monthly_income = float(request.form.get("monthly_income", 0))
        application.employment_status = request.form.get("employment_status")
        application.employer_name = request.form.get("employer_name")
        application.financial_submitted_at = datetime.utcnow()
        application.financial_status = "pending"

        db.session.commit()

        flash("Financial information saved successfully!", "success")
        return redirect(url_for("loan_app.phase2_financial"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error saving financial information: {str(e)}", "error")
        return redirect(url_for("loan_app.phase2_financial"))


@loan_app.route("/upload-kyc-document", methods=["POST"])
@login_required
def upload_kyc_document():
    """Upload KYC document via AJAX"""
    # Get user's most recent application
    application = (
        LoanApplication.query.filter_by(user_id=current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .first()
    )

    if not application:
        return jsonify({"success": False, "message": "No application found"}), 404

    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file provided"}), 400

    file = request.files["file"]
    document_type = request.form.get("document_type", "kyc_document")

    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "File type not allowed"}), 400

    # Check file size
    file_size = get_file_size(file)
    if file_size > MAX_FILE_SIZE:
        return jsonify(
            {"success": False, "message": "File size exceeds 10MB limit"}
        ), 400

    try:
        # Save file
        filename = secure_filename(
            f"{current_user.id}_{application.id}_{document_type}_{datetime.utcnow().timestamp()}_{file.filename}"
        )
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Create document record
        document = LoanDocument(
            application_id=application.id,
            document_type=document_type,
            document_name=file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type,
        )
        db.session.add(document)
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "Document uploaded successfully",
                "document": {
                    "id": document.id,
                    "name": document.document_name,
                    "type": document.document_type,
                    "size": document.file_size,
                },
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


@loan_app.route("/upload-financial-document", methods=["POST"])
@login_required
def upload_financial_document():
    """Upload financial document via AJAX"""
    # Get user's most recent application
    application = (
        LoanApplication.query.filter_by(user_id=current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .first()
    )

    if not application:
        return jsonify({"success": False, "message": "No application found"}), 404

    if not application.can_proceed_to_phase_2():
        return jsonify({"success": False, "message": "Complete Phase 1 first"}), 403

    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file provided"}), 400

    file = request.files["file"]
    document_type = request.form.get("document_type", "financial_document")

    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "File type not allowed"}), 400

    # Check file size
    file_size = get_file_size(file)
    if file_size > MAX_FILE_SIZE:
        return jsonify(
            {"success": False, "message": "File size exceeds 10MB limit"}
        ), 400

    try:
        # Save file
        filename = secure_filename(
            f"{current_user.id}_{application.id}_{document_type}_{datetime.utcnow().timestamp()}_{file.filename}"
        )
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Create document record
        document = LoanDocument(
            application_id=application.id,
            document_type=document_type,
            document_name=file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type,
        )
        db.session.add(document)
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "Document uploaded successfully",
                "document": {
                    "id": document.id,
                    "name": document.document_name,
                    "type": document.document_type,
                    "size": document.file_size,
                },
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


@loan_app.route("/accept-loan-offer", methods=["POST"])
@login_required
def accept_loan_offer():
    """Accept loan offer in Phase 3"""
    # Get user's most recent application
    application = (
        LoanApplication.query.filter_by(user_id=current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .first()
    )

    if not application:
        return jsonify({"success": False, "message": "No application found"}), 404

    if not application.can_proceed_to_phase_3():
        return jsonify(
            {"success": False, "message": "Complete previous phases first"}
        ), 403

    if application.final_decision != "accepted":
        return jsonify({"success": False, "message": "Loan offer not available"}), 400

    try:
        # Mark as accepted by user
        application.user_accepted = True
        application.user_accepted_at = datetime.utcnow()
        application.status = "accepted"

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "Loan offer accepted successfully!",
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


@loan_app.route("/apply")
@login_required
def apply():
    """New loan application form"""
    # Check KYC status
    if not check_kyc_approved():
        flash(
            "You must complete KYC verification before applying for a loan.", "warning"
        )
        return redirect(url_for("kyc.index"))

    return render_template("loan_application/apply.html", user=current_user)


@loan_app.route("/submit", methods=["POST"])
@login_required
def submit():
    """Submit loan application"""
    # Check KYC status
    if not check_kyc_approved():
        return jsonify({"success": False, "message": "KYC not approved"}), 403

    try:
        # Create loan application
        application = LoanApplication(
            user_id=current_user.id,
            loan_amount_requested=float(request.form.get("loan_amount_requested")),
            loan_purpose=request.form.get("loan_purpose"),
            loan_duration_months=int(request.form.get("loan_duration_months")),
            monthly_income=float(request.form.get("monthly_income")),
            employment_status=request.form.get("employment_status"),
            employer_name=request.form.get("employer_name"),
            has_other_loans=request.form.get("has_other_loans") == "true",
            other_loans_amount=float(request.form.get("other_loans_amount", 0)),
            status="pending",
            submitted_at=datetime.utcnow(),
        )

        db.session.add(application)
        db.session.commit()

        flash(
            "Loan application submitted successfully! Please upload your financial documents.",
            "success",
        )
        return redirect(url_for("loan_app.detail", application_id=application.id))

    except Exception as e:
        db.session.rollback()
        flash(f"Error submitting application: {str(e)}", "error")
        return redirect(url_for("loan_app.apply"))


@loan_app.route("/<int:application_id>")
@login_required
def detail(application_id):
    """View loan application details"""
    application = LoanApplication.query.get_or_404(application_id)

    # Verify ownership
    if application.user_id != current_user.id:
        flash("Unauthorized access", "error")
        return redirect(url_for("loan_app.index"))

    # Get documents
    documents = LoanDocument.query.filter_by(application_id=application_id).all()

    return render_template(
        "loan_application/detail.html", application=application, documents=documents
    )


@loan_app.route("/<int:application_id>/upload-document", methods=["POST"])
@login_required
def upload_document(application_id):
    """Upload financial document"""
    application = LoanApplication.query.get_or_404(application_id)

    # Verify ownership
    if application.user_id != current_user.id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    # Check if application is still pending
    if application.status != "pending":
        return jsonify(
            {
                "success": False,
                "message": "Cannot upload documents to non-pending application",
            }
        ), 400

    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file provided"}), 400

    file = request.files["file"]
    document_type = request.form.get("document_type")

    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "File type not allowed"}), 400

    # Check file size
    file_size = get_file_size(file)
    if file_size > MAX_FILE_SIZE:
        return jsonify(
            {"success": False, "message": "File size exceeds 10MB limit"}
        ), 400

    # Save file
    filename = secure_filename(
        f"{current_user.id}_{application_id}_{document_type}_{datetime.utcnow().timestamp()}_{file.filename}"
    )
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Create document record
    document = LoanDocument(
        application_id=application_id,
        document_type=document_type,
        document_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type,
    )
    db.session.add(document)
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "message": "Document uploaded successfully",
            "document": document.to_dict(),
        }
    )


@loan_app.route("/document/<int:document_id>/delete", methods=["POST"])
@login_required
def delete_document(document_id):
    """Delete a document"""
    document = LoanDocument.query.get_or_404(document_id)
    application = LoanApplication.query.get(document.application_id)

    # Verify ownership
    if application.user_id != current_user.id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    # Check if application is still pending
    if application.status != "pending":
        return jsonify(
            {
                "success": False,
                "message": "Cannot delete documents from non-pending application",
            }
        ), 400

    # Delete file from filesystem
    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    # Delete from database
    db.session.delete(document)
    db.session.commit()

    return jsonify({"success": True, "message": "Document deleted successfully"})


@loan_app.route("/document/<int:document_id>/download")
@login_required
def download_document(document_id):
    """Download a document"""
    document = LoanDocument.query.get_or_404(document_id)
    application = LoanApplication.query.get(document.application_id)

    # Verify ownership or admin
    if application.user_id != current_user.id and not current_user.is_admin:
        flash("Unauthorized access", "error")
        return redirect(url_for("loan_app.index"))

    return send_file(
        document.file_path, as_attachment=True, download_name=document.document_name
    )


@loan_app.route("/<int:application_id>/cancel", methods=["POST"])
@login_required
def cancel(application_id):
    """Cancel loan application"""
    application = LoanApplication.query.get_or_404(application_id)

    # Verify ownership
    if application.user_id != current_user.id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    # Can only cancel pending applications
    if application.status != "pending":
        return jsonify(
            {"success": False, "message": "Can only cancel pending applications"}
        ), 400

    application.status = "cancelled"
    db.session.commit()

    flash("Loan application cancelled successfully.", "info")
    return redirect(url_for("loan_app.index"))


# ============================================================================
# API ENDPOINTS
# ============================================================================


@loan_app.route("/api/check-eligibility")
@login_required
def check_eligibility():
    """Check if user is eligible to apply for loans"""
    return jsonify(
        {
            "success": True,
            "eligible": current_user.kyc_status == "approved",
            "kyc_status": current_user.kyc_status,
            "message": "KYC approved"
            if current_user.kyc_status == "approved"
            else "KYC verification required",
        }
    )


@loan_app.route("/api/applications")
@login_required
def get_applications():
    """Get user's loan applications"""
    applications = (
        LoanApplication.query.filter_by(user_id=current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .all()
    )

    return jsonify(
        {"success": True, "applications": [app.to_dict() for app in applications]}
    )


@loan_app.route("/api/<int:application_id>/status")
@login_required
def get_status(application_id):
    """Get loan application status"""
    application = LoanApplication.query.get_or_404(application_id)

    # Verify ownership
    if application.user_id != current_user.id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    documents = LoanDocument.query.filter_by(application_id=application_id).all()

    return jsonify(
        {
            "success": True,
            "application": application.to_dict(),
            "documents_count": len(documents),
            "has_bank_statement": any(
                doc.document_type == "bank_statement" for doc in documents
            ),
            "has_proof_of_income": any(
                doc.document_type == "proof_of_income" for doc in documents
            ),
        }
    )

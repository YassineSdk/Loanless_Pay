import os
from datetime import datetime, timedelta

from decorators import admin_required
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
from models import (
    AdminReview,
    FundingTransaction,
    KYCDocument,
    Loan,
    LoanApplication,
    LoanDocument,
    User,
    db,
)
from sqlalchemy import desc, func, or_

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
@admin.route("/dashboard")
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    # Get statistics for Loan Applications
    total_users = User.query.filter_by(is_admin=False).count()
    total_applications = LoanApplication.query.count()

    # Count applications by phase
    phase1_pending = LoanApplication.query.filter_by(
        current_phase=1, kyc_status="pending"
    ).count()
    phase2_pending = LoanApplication.query.filter_by(
        current_phase=2, financial_status="pending"
    ).count()
    phase3_pending = LoanApplication.query.filter_by(
        current_phase=3, decision_status="pending"
    ).count()
    pending_applications = phase1_pending + phase2_pending + phase3_pending

    # Count by final decision
    approved_applications = LoanApplication.query.filter_by(
        final_decision="accepted"
    ).count()
    rejected_applications = LoanApplication.query.filter_by(
        final_decision="rejected"
    ).count()

    # Count by overall status
    active_applications = LoanApplication.query.filter_by(
        overall_status="in_progress"
    ).count()
    completed_applications = LoanApplication.query.filter_by(
        overall_status="completed"
    ).count()

    # Calculate total loan amount requested and approved
    total_amount_requested = (
        db.session.query(func.sum(LoanApplication.loan_amount_requested)).scalar() or 0
    )
    approved_amount = (
        db.session.query(func.sum(LoanApplication.approved_amount))
        .filter(LoanApplication.final_decision == "accepted")
        .scalar()
        or 0
    )

    # Get recent loan applications (last 5)
    recent_applications = (
        LoanApplication.query.order_by(desc(LoanApplication.created_at)).limit(5).all()
    )

    # Get recent users (last 5)
    recent_users = (
        User.query.filter_by(is_admin=False)
        .order_by(desc(User.created_at))
        .limit(5)
        .all()
    )

    # Calculate approval rate
    total_decided = approved_applications + rejected_applications
    approval_rate = (
        (approved_applications / total_decided * 100) if total_decided > 0 else 0
    )

    # Applications by phase
    applications_by_phase = {
        "Phase 1 - KYC": LoanApplication.query.filter_by(current_phase=1).count(),
        "Phase 2 - Financial": LoanApplication.query.filter_by(current_phase=2).count(),
        "Phase 3 - Decision": LoanApplication.query.filter_by(current_phase=3).count(),
    }

    # Funding Party Statistics
    total_funding_partners = User.query.filter_by(user_role="funding_party").count()
    active_funding_partners = User.query.filter_by(
        user_role="funding_party", is_active=True
    ).count()

    # Calculate total funds available
    total_funds_deposited = (
        db.session.query(func.sum(FundingTransaction.amount))
        .filter(FundingTransaction.transaction_type == "deposit")
        .scalar()
        or 0
    )

    total_funds_withdrawn = (
        db.session.query(func.sum(FundingTransaction.amount))
        .filter(FundingTransaction.transaction_type == "withdrawal")
        .scalar()
        or 0
    )

    available_funds = total_funds_deposited - total_funds_withdrawn

    # Get recent funding partners (last 5)
    recent_funding_partners = (
        User.query.filter_by(user_role="funding_party")
        .order_by(desc(User.created_at))
        .limit(5)
        .all()
    )

    # Get top funders by total deposits
    top_funders = (
        db.session.query(
            User.username,
            User.company_name,
            func.sum(FundingTransaction.amount).label("total_contributed"),
        )
        .join(FundingTransaction, User.id == FundingTransaction.funder_id)
        .filter(FundingTransaction.transaction_type == "deposit")
        .group_by(User.id, User.username, User.company_name)
        .order_by(desc("total_contributed"))
        .limit(5)
        .all()
    )

    stats = {
        "total_users": total_users,
        "total_loans": total_applications,
        "pending_loans": pending_applications,
        "total_amount": approved_amount,
        "approved_loans": approved_applications,
        "rejected_loans": rejected_applications,
        "active_loans": active_applications,
        "approval_rate": round(approval_rate, 1),
        "recent_loans": recent_applications,
        "recent_users": recent_users,
        "loans_by_sector": applications_by_phase,
        "phase1_pending": phase1_pending,
        "phase2_pending": phase2_pending,
        "phase3_pending": phase3_pending,
        # Funding statistics
        "total_funding_partners": total_funding_partners,
        "active_funding_partners": active_funding_partners,
        "total_funds_deposited": total_funds_deposited,
        "available_funds": available_funds,
        "recent_funding_partners": recent_funding_partners,
        "top_funders": top_funders,
    }

    return render_template("admin/dashboard.html", stats=stats)


@admin.route("/funding-partners")
@login_required
@admin_required
def funding_partners():
    """Manage funding partners"""
    # Get filter parameters
    status_filter = request.args.get("status", "")
    kyc_filter = request.args.get("kyc", "")
    search_query = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    # Build query
    query = User.query.filter_by(user_role="funding_party")

    if status_filter:
        if status_filter == "active":
            query = query.filter_by(is_active=True)
        elif status_filter == "inactive":
            query = query.filter_by(is_active=False)

    if kyc_filter:
        query = query.filter_by(kyc_status=kyc_filter)

    if search_query:
        query = query.filter(
            (User.username.contains(search_query))
            | (User.email.contains(search_query))
            | (User.company_name.contains(search_query))
        )

    # Paginate results
    pagination = query.order_by(desc(User.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Get statistics
    total_partners = User.query.filter_by(user_role="funding_party").count()
    active_partners = User.query.filter_by(
        user_role="funding_party", is_active=True
    ).count()
    kyc_pending = User.query.filter_by(
        user_role="funding_party", kyc_status="pending", kyc_submitted=True
    ).count()
    kyc_approved = User.query.filter_by(
        user_role="funding_party", kyc_status="approved"
    ).count()

    # Calculate total contributions
    total_contributed = (
        db.session.query(func.sum(FundingTransaction.amount))
        .filter(FundingTransaction.transaction_type == "deposit")
        .scalar()
        or 0
    )

    stats = {
        "total_partners": total_partners,
        "active_partners": active_partners,
        "kyc_pending": kyc_pending,
        "kyc_approved": kyc_approved,
        "total_contributed": total_contributed,
    }

    return render_template(
        "admin/funding_partners.html",
        partners=pagination.items,
        pagination=pagination,
        stats=stats,
        status_filter=status_filter,
        kyc_filter=kyc_filter,
        search_query=search_query,
    )


@admin.route("/loans")
@login_required
@admin_required
def loans():
    """View all loans with filters"""
    # Get filter parameters
    status_filter = request.args.get("status", "")
    sector_filter = request.args.get("sector", "")
    search_query = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    # Build query
    query = Loan.query

    if status_filter:
        query = query.filter_by(status=status_filter)

    if sector_filter:
        query = query.filter_by(sector=sector_filter)

    if search_query:
        query = query.join(User).filter(
            (User.username.contains(search_query))
            | (User.email.contains(search_query))
            | (Loan.id == int(search_query) if search_query.isdigit() else False)
        )

    # Paginate results
    loans_pagination = query.order_by(desc(Loan.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Get unique sectors for filter dropdown
    sectors = db.session.query(Loan.sector).distinct().all()
    sectors = [s[0] for s in sectors]

    return render_template(
        "admin/loans.html",
        loans=loans_pagination.items,
        pagination=loans_pagination,
        sectors=sectors,
        status_filter=status_filter,
        sector_filter=sector_filter,
        search_query=search_query,
    )


@admin.route("/loans/<int:loan_id>")
@login_required
@admin_required
def loan_detail(loan_id):
    """View detailed information about a specific loan"""
    loan = Loan.query.get_or_404(loan_id)
    return render_template("admin/loan_detail.html", loan=loan)


@admin.route("/loans/<int:loan_id>/approve", methods=["POST"])
@login_required
@admin_required
def approve_loan(loan_id):
    """Approve a loan"""
    loan = Loan.query.get_or_404(loan_id)

    if loan.status == "approved":
        flash("This loan is already approved.", "info")
    else:
        loan.status = "approved"
        loan.approved_by = current_user.id
        loan.updated_at = datetime.utcnow()

        admin_notes = request.form.get("admin_notes", "")
        if admin_notes:
            loan.admin_notes = admin_notes

        db.session.commit()
        flash(f"Loan #{loan.id} has been approved successfully.", "success")

    # Return to previous page or loan detail
    next_page = request.form.get("next") or url_for(
        "admin.loan_detail", loan_id=loan_id
    )
    return redirect(next_page)


@admin.route("/loans/<int:loan_id>/reject", methods=["POST"])
@login_required
@admin_required
def reject_loan(loan_id):
    """Reject a loan"""
    loan = Loan.query.get_or_404(loan_id)

    if loan.status == "rejected":
        flash("This loan is already rejected.", "info")
    else:
        loan.status = "rejected"
        loan.approved_by = current_user.id
        loan.updated_at = datetime.utcnow()

        admin_notes = request.form.get("admin_notes", "")
        if admin_notes:
            loan.admin_notes = admin_notes

        db.session.commit()
        flash(f"Loan #{loan.id} has been rejected.", "warning")

    # Return to previous page or loan detail
    next_page = request.form.get("next") or url_for(
        "admin.loan_detail", loan_id=loan_id
    )
    return redirect(next_page)


@admin.route("/loans/<int:loan_id>/update-status", methods=["POST"])
@login_required
@admin_required
def update_loan_status(loan_id):
    """Update loan status"""
    loan = Loan.query.get_or_404(loan_id)

    new_status = request.form.get("status")
    valid_statuses = ["pending", "approved", "rejected", "active", "completed"]

    if new_status not in valid_statuses:
        flash("Invalid status.", "error")
    else:
        loan.status = new_status
        loan.updated_at = datetime.utcnow()

        admin_notes = request.form.get("admin_notes", "")
        if admin_notes:
            loan.admin_notes = admin_notes

        db.session.commit()
        flash(f"Loan #{loan.id} status updated to {new_status}.", "success")

    return redirect(url_for("admin.loan_detail", loan_id=loan_id))


@admin.route("/loans/<int:loan_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_loan(loan_id):
    """Delete a loan (admin only)"""
    loan = Loan.query.get_or_404(loan_id)

    db.session.delete(loan)
    db.session.commit()

    flash(f"Loan #{loan.id} has been deleted.", "success")
    return redirect(url_for("admin.loans"))


@admin.route("/users")
@login_required
@admin_required
def users():
    """View all users"""
    search_query = request.args.get("search", "")
    status_filter = request.args.get("status", "")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    # Build query (exclude admin users from list)
    query = User.query.filter_by(is_admin=False)

    if search_query:
        query = query.filter(
            (User.username.contains(search_query)) | (User.email.contains(search_query))
        )

    if status_filter == "active":
        query = query.filter_by(is_active=True)
    elif status_filter == "inactive":
        query = query.filter_by(is_active=False)

    # Paginate results
    users_pagination = query.order_by(desc(User.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Get loan counts for each user
    users_with_stats = []
    for user in users_pagination.items:
        total_loans = Loan.query.filter_by(user_id=user.id).count()
        active_loans = Loan.query.filter_by(user_id=user.id, status="active").count()
        users_with_stats.append(
            {"user": user, "total_loans": total_loans, "active_loans": active_loans}
        )

    return render_template(
        "admin/users.html",
        users=users_with_stats,
        pagination=users_pagination,
        search_query=search_query,
        status_filter=status_filter,
    )


@admin.route("/users/<int:user_id>")
@login_required
@admin_required
def user_detail(user_id):
    """View detailed information about a specific user"""
    user = User.query.get_or_404(user_id)

    # Get user's loans
    loans = Loan.query.filter_by(user_id=user_id).order_by(desc(Loan.created_at)).all()

    # Calculate user statistics
    total_loans = len(loans)
    total_amount = sum(loan.amount for loan in loans)
    approved_loans = len([l for l in loans if l.status == "approved"])
    active_loans = len([l for l in loans if l.status == "active"])

    user_stats = {
        "total_loans": total_loans,
        "total_amount": total_amount,
        "approved_loans": approved_loans,
        "active_loans": active_loans,
    }

    return render_template(
        "admin/user_detail.html", user=user, loans=loans, stats=user_stats
    )


@admin.route("/users/<int:user_id>/toggle-status", methods=["POST"])
@login_required
@admin_required
def toggle_user_status(user_id):
    """Activate or deactivate a user"""
    user = User.query.get_or_404(user_id)

    # Prevent deactivating yourself
    if user.id == current_user.id:
        flash("You cannot deactivate your own account.", "error")
        return redirect(url_for("admin.user_detail", user_id=user_id))

    # Prevent modifying other admin accounts
    if user.is_admin:
        flash("You cannot modify other admin accounts.", "error")
        return redirect(url_for("admin.user_detail", user_id=user_id))

    user.is_active = not user.is_active
    db.session.commit()

    status = "activated" if user.is_active else "deactivated"
    flash(f"User {user.username} has been {status}.", "success")

    return redirect(url_for("admin.user_detail", user_id=user_id))


@admin.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user and their loans"""
    user = User.query.get_or_404(user_id)

    # Prevent deleting yourself
    if user.id == current_user.id:
        flash("You cannot delete your own account.", "error")
        return redirect(url_for("admin.users"))

    # Prevent deleting other admins
    if user.is_admin:
        flash("You cannot delete other admin accounts.", "error")
        return redirect(url_for("admin.users"))

    username = user.username

    # Delete user's loans first
    Loan.query.filter_by(user_id=user_id).delete()

    # Delete user
    db.session.delete(user)
    db.session.commit()

    flash(f"User {username} and all their loans have been deleted.", "success")
    return redirect(url_for("admin.users"))


@admin.route("/statistics")
@login_required
@admin_required
def statistics():
    """View detailed statistics and analytics"""
    # Overall statistics
    total_users = User.query.filter_by(is_admin=False).count()
    total_loans = Loan.query.count()

    # Loan statistics
    pending_loans = Loan.query.filter_by(status="pending").count()
    approved_loans = Loan.query.filter_by(status="approved").count()
    rejected_loans = Loan.query.filter_by(status="rejected").count()
    active_loans = Loan.query.filter_by(status="active").count()
    completed_loans = Loan.query.filter_by(status="completed").count()

    # Financial statistics
    total_amount = db.session.query(func.sum(Loan.amount)).scalar() or 0
    avg_loan_amount = db.session.query(func.avg(Loan.amount)).scalar() or 0
    avg_payment_period = db.session.query(func.avg(Loan.payment_period)).scalar() or 0

    # Approved/Active loan amounts
    approved_amount = (
        db.session.query(func.sum(Loan.amount))
        .filter(Loan.status.in_(["approved", "active"]))
        .scalar()
        or 0
    )

    # Loans by sector
    loans_by_sector = (
        db.session.query(Loan.sector, func.count(Loan.id), func.sum(Loan.amount))
        .group_by(Loan.sector)
        .all()
    )

    # Loans by status
    loans_by_status = {
        "pending": pending_loans,
        "approved": approved_loans,
        "rejected": rejected_loans,
        "active": active_loans,
        "completed": completed_loans,
    }

    # Calculate approval rate
    total_reviewed = approved_loans + rejected_loans
    approval_rate = (approved_loans / total_reviewed * 100) if total_reviewed > 0 else 0

    # Loans over time (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    loans_last_30_days = Loan.query.filter(Loan.created_at >= thirty_days_ago).count()

    # Users over time (last 30 days)
    users_last_30_days = User.query.filter(
        User.created_at >= thirty_days_ago, User.is_admin == False
    ).count()

    stats = {
        "total_users": total_users,
        "total_loans": total_loans,
        "total_amount": total_amount,
        "avg_loan_amount": avg_loan_amount,
        "avg_payment_period": avg_payment_period,
        "approved_amount": approved_amount,
        "approval_rate": round(approval_rate, 1),
        "loans_by_sector": loans_by_sector,
        "loans_by_status": loans_by_status,
        "loans_last_30_days": loans_last_30_days,
        "users_last_30_days": users_last_30_days,
    }

    return render_template("admin/statistics.html", stats=stats)


@admin.route("/api/chart-data")
@login_required
@admin_required
def chart_data():
    """API endpoint for chart data"""
    chart_type = request.args.get("type", "status")

    if chart_type == "status":
        # Loans by status
        data = {
            "pending": Loan.query.filter_by(status="pending").count(),
            "approved": Loan.query.filter_by(status="approved").count(),
            "rejected": Loan.query.filter_by(status="rejected").count(),
            "active": Loan.query.filter_by(status="active").count(),
            "completed": Loan.query.filter_by(status="completed").count(),
        }
    elif chart_type == "sector":
        # Loans by sector
        result = (
            db.session.query(Loan.sector, func.count(Loan.id))
            .group_by(Loan.sector)
            .all()
        )
        data = dict(result)
    else:
        data = {}

    return jsonify(data)


# ============================================================================
# LOAN APPLICATION MANAGEMENT (3-PHASE SYSTEM)
# ============================================================================


@admin.route("/loan-applications")
@login_required
@admin_required
def loan_applications():
    """View all loan applications with filters"""
    # Get filter parameters
    phase_filter = request.args.get("phase", "")
    status_filter = request.args.get("status", "")
    search_query = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    # Build query
    query = LoanApplication.query

    if phase_filter:
        query = query.filter_by(current_phase=int(phase_filter))

    if status_filter:
        if status_filter == "kyc_pending":
            query = query.filter_by(kyc_status="pending")
        elif status_filter == "kyc_approved":
            query = query.filter_by(kyc_status="approved")
        elif status_filter == "financial_pending":
            query = query.filter_by(financial_status="pending")
        elif status_filter == "financial_approved":
            query = query.filter_by(financial_status="approved")
        elif status_filter == "decision_pending":
            query = query.filter_by(decision_status="pending")
        elif status_filter == "completed":
            query = query.filter_by(overall_status="completed")

    if search_query:
        search_conditions = [
            User.username.contains(search_query),
            User.email.contains(search_query),
            LoanApplication.full_name.contains(search_query),
        ]

        # Only add ID search if search_query is a valid integer
        if search_query.isdigit():
            search_conditions.append(LoanApplication.id == int(search_query))

        query = query.join(User).filter(or_(*search_conditions))

    # Paginate results
    applications_pagination = query.order_by(desc(LoanApplication.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Get statistics for dashboard
    total_applications = LoanApplication.query.count()
    kyc_pending = LoanApplication.query.filter_by(kyc_status="pending").count()
    financial_pending = LoanApplication.query.filter_by(
        financial_status="pending"
    ).count()
    decision_pending = LoanApplication.query.filter_by(
        decision_status="pending"
    ).count()

    stats = {
        "total_applications": total_applications,
        "kyc_pending": kyc_pending,
        "financial_pending": financial_pending,
        "decision_pending": decision_pending,
        "pending_loans": kyc_pending + financial_pending + decision_pending,
    }

    return render_template(
        "admin/loan_applications.html",
        applications=applications_pagination.items,
        pagination=applications_pagination,
        phase_filter=phase_filter,
        status_filter=status_filter,
        search_query=search_query,
        stats=stats,
    )


@admin.route("/loan-applications/<int:application_id>")
@login_required
@admin_required
def loan_application_detail(application_id):
    """View detailed information about a specific loan application"""
    application = LoanApplication.query.get_or_404(application_id)

    # Get all documents grouped by phase
    kyc_documents = LoanDocument.query.filter_by(
        application_id=application_id, phase=1
    ).all()

    financial_documents = LoanDocument.query.filter_by(
        application_id=application_id, phase=2
    ).all()

    # Get admin reviews
    reviews = (
        AdminReview.query.filter_by(application_id=application_id)
        .order_by(desc(AdminReview.created_at))
        .all()
    )

    return render_template(
        "admin/loan_application_detail.html",
        application=application,
        kyc_documents=kyc_documents,
        financial_documents=financial_documents,
        reviews=reviews,
    )


@admin.route("/loan-applications/<int:application_id>/approve-kyc", methods=["POST"])
@login_required
@admin_required
def approve_kyc(application_id):
    """Approve KYC verification (Phase 1)"""
    application = LoanApplication.query.get_or_404(application_id)

    if application.kyc_status == "approved":
        flash("KYC is already approved.", "info")
    else:
        # Update application
        application.kyc_status = "approved"
        application.updated_at = datetime.utcnow()

        # Create admin review record
        notes = request.form.get("notes", "")
        review = AdminReview()
        review.application_id = application_id
        review.reviewer_id = current_user.id
        review.action = "kyc_approved"
        review.notes = notes
        db.session.add(review)

        db.session.commit()
        flash("KYC verification approved successfully.", "success")

    return redirect(
        url_for("admin.loan_application_detail", application_id=application_id)
    )


@admin.route("/loan-applications/<int:application_id>/reject-kyc", methods=["POST"])
@login_required
@admin_required
def reject_kyc(application_id):
    """Reject KYC verification (Phase 1)"""
    application = LoanApplication.query.get_or_404(application_id)

    # Update application
    application.kyc_status = "rejected"
    application.overall_status = "cancelled"
    application.updated_at = datetime.utcnow()

    # Create admin review record
    notes = request.form.get("notes", "")
    review = AdminReview()
    review.application_id = application_id
    review.reviewer_id = current_user.id
    review.action = "kyc_rejected"
    review.notes = notes
    db.session.add(review)

    db.session.commit()
    flash("KYC verification rejected.", "warning")

    return redirect(
        url_for("admin.loan_application_detail", application_id=application_id)
    )


@admin.route(
    "/loan-applications/<int:application_id>/approve-financial", methods=["POST"]
)
@login_required
@admin_required
def approve_financial(application_id):
    """Approve financial documents (Phase 2)"""
    application = LoanApplication.query.get_or_404(application_id)

    if not application.can_proceed_to_phase_2():
        flash("KYC must be approved first.", "error")
        return redirect(
            url_for("admin.loan_application_detail", application_id=application_id)
        )

    if application.financial_status == "approved":
        flash("Financial documents are already approved.", "info")
    else:
        # Update application
        application.financial_status = "approved"
        application.updated_at = datetime.utcnow()

        # Create admin review record
        notes = request.form.get("notes", "")
        review = AdminReview()
        review.application_id = application_id
        review.reviewer_id = current_user.id
        review.action = "financial_approved"
        review.notes = notes
        db.session.add(review)

        db.session.commit()
        flash("Financial documents approved successfully.", "success")

    return redirect(
        url_for("admin.loan_application_detail", application_id=application_id)
    )


@admin.route(
    "/loan-applications/<int:application_id>/reject-financial", methods=["POST"]
)
@login_required
@admin_required
def reject_financial(application_id):
    """Reject financial documents (Phase 2)"""
    application = LoanApplication.query.get_or_404(application_id)

    # Update application
    application.financial_status = "rejected"
    application.overall_status = "cancelled"
    application.updated_at = datetime.utcnow()

    # Create admin review record
    notes = request.form.get("notes", "")
    review = AdminReview()
    review.application_id = application_id
    review.reviewer_id = current_user.id
    review.action = "financial_rejected"
    review.notes = notes
    db.session.add(review)

    db.session.commit()
    flash("Financial documents rejected.", "warning")

    return redirect(
        url_for("admin.loan_application_detail", application_id=application_id)
    )


@admin.route("/loan-applications/<int:application_id>/make-decision", methods=["POST"])
@login_required
@admin_required
def make_loan_decision(application_id):
    """Make final loan decision (Phase 3)"""
    application = LoanApplication.query.get_or_404(application_id)

    if not application.can_proceed_to_phase_3():
        flash("Both KYC and Financial documents must be approved first.", "error")
        return redirect(
            url_for("admin.loan_application_detail", application_id=application_id)
        )

    # Get decision data
    decision = request.form.get("decision")  # accepted or rejected

    if decision not in ["accepted", "rejected"]:
        flash("Invalid decision.", "error")
        return redirect(
            url_for("admin.loan_application_detail", application_id=application_id)
        )

    # Update application
    application.final_decision = decision
    application.decision_status = decision
    application.decision_date = datetime.utcnow()
    application.decision_by = current_user.id
    application.current_phase = 3
    application.updated_at = datetime.utcnow()

    if decision == "accepted":
        # Set loan terms
        approved_amount = (
            request.form.get("approved_amount") or application.loan_amount_requested
        )
        approved_duration = (
            request.form.get("approved_duration") or application.loan_duration_months
        )
        interest_rate = request.form.get("interest_rate") or 5.0

        application.approved_amount = float(approved_amount) if approved_amount else 0
        application.approved_duration = (
            int(approved_duration) if approved_duration else 12
        )
        application.interest_rate = float(interest_rate)

        # Calculate monthly payment
        if application.approved_amount and application.approved_duration:
            monthly_interest = application.interest_rate / 100 / 12
            num_payments = application.approved_duration
            if monthly_interest > 0:
                application.monthly_payment = (
                    application.approved_amount
                    * (monthly_interest * (1 + monthly_interest) ** num_payments)
                    / ((1 + monthly_interest) ** num_payments - 1)
                )
            else:
                application.monthly_payment = application.approved_amount / num_payments
    else:
        application.overall_status = "cancelled"

    # Create admin review record
    notes = request.form.get("notes", "")
    review = AdminReview()
    review.application_id = application_id
    review.reviewer_id = current_user.id
    review.action = f"decision_{decision}"
    review.notes = notes
    db.session.add(review)

    db.session.commit()

    if decision == "accepted":
        flash(
            "Loan application approved! User can now review and accept the offer.",
            "success",
        )
    else:
        flash("Loan application rejected.", "warning")

    return redirect(
        url_for("admin.loan_application_detail", application_id=application_id)
    )


@admin.route("/loan-applications/<int:application_id>/add-note", methods=["POST"])
@login_required
@admin_required
def add_application_note(application_id):
    """Add an admin note to an application"""
    application = LoanApplication.query.get_or_404(application_id)

    notes = request.form.get("notes", "")
    if not notes:
        flash("Note cannot be empty.", "error")
        return redirect(
            url_for("admin.loan_application_detail", application_id=application_id)
        )

    # Create admin review record
    review = AdminReview()
    review.application_id = application_id
    review.reviewer_id = current_user.id
    review.action = "note_added"
    review.notes = notes
    db.session.add(review)
    db.session.commit()

    flash("Note added successfully.", "success")
    return redirect(
        url_for("admin.loan_application_detail", application_id=application_id)
    )


@admin.route("/loan-applications/document/<int:document_id>/download")
@login_required
@admin_required
def download_application_document(document_id):
    """Download a loan application document"""
    document = LoanDocument.query.get_or_404(document_id)

    if not os.path.exists(document.file_path):
        flash("Document file not found.", "error")
        return redirect(url_for("admin.loan_applications"))

    return send_file(
        document.file_path, as_attachment=True, download_name=document.document_name
    )


@admin.route("/loan-applications/<int:application_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_loan_application(application_id):
    """Delete a loan application and all associated data"""
    application = LoanApplication.query.get_or_404(application_id)

    # Delete all associated documents from filesystem
    documents = LoanDocument.query.filter_by(application_id=application_id).all()
    for doc in documents:
        if os.path.exists(doc.file_path):
            try:
                os.remove(doc.file_path)
            except Exception as e:
                print(f"Error deleting file {doc.file_path}: {e}")

    # Delete application (cascades to documents, reviews, phases)
    db.session.delete(application)
    db.session.commit()

    flash(f"Loan application #{application_id} has been deleted.", "success")
    return redirect(url_for("admin.loan_applications"))


# ============================================================================
# KYC USER VERIFICATION MANAGEMENT
# ============================================================================


@admin.route("/kyc-verifications")
@login_required
@admin_required
def kyc_verifications():
    """View all user KYC verifications"""
    # Get filter parameters
    status_filter = request.args.get("status", "")
    search_query = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    # Build query - only non-admin users
    query = User.query.filter_by(is_admin=False)

    if status_filter:
        query = query.filter_by(kyc_status=status_filter)

    if search_query:
        query = query.filter(
            (User.username.contains(search_query))
            | (User.email.contains(search_query))
            | (User.full_name.contains(search_query))
        )

    # Order by KYC submission date
    query = query.order_by(desc(User.kyc_submitted_at))

    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    users = pagination.items

    # Get statistics
    total_users = User.query.filter_by(is_admin=False).count()
    kyc_pending = User.query.filter_by(
        is_admin=False, kyc_status="pending", kyc_submitted=True
    ).count()
    kyc_approved = User.query.filter_by(is_admin=False, kyc_status="approved").count()
    kyc_rejected = User.query.filter_by(is_admin=False, kyc_status="rejected").count()
    not_submitted = User.query.filter_by(is_admin=False, kyc_submitted=False).count()

    stats = {
        "total_users": total_users,
        "kyc_pending": kyc_pending,
        "kyc_approved": kyc_approved,
        "kyc_rejected": kyc_rejected,
        "not_submitted": not_submitted,
    }

    return render_template(
        "admin/kyc_verifications.html",
        users=users,
        pagination=pagination,
        stats=stats,
        status_filter=status_filter,
        search_query=search_query,
    )


@admin.route("/kyc-verifications/<int:user_id>")
@login_required
@admin_required
def kyc_verification_detail(user_id):
    """View detailed KYC information for a specific user"""
    user = User.query.get_or_404(user_id)

    # Get user's KYC documents
    documents = KYCDocument.query.filter_by(user_id=user_id).all()

    # Get user's loan applications (to show history)
    loan_applications = (
        LoanApplication.query.filter_by(user_id=user_id)
        .order_by(desc(LoanApplication.created_at))
        .all()
    )

    return render_template(
        "admin/kyc_verification_detail.html",
        user=user,
        documents=documents,
        loan_applications=loan_applications,
    )


@admin.route("/kyc-verifications/<int:user_id>/approve", methods=["POST"])
@login_required
@admin_required
def approve_user_kyc(user_id):
    """Approve user's KYC verification"""
    user = User.query.get_or_404(user_id)

    if user.kyc_status == "approved":
        flash(f"{user.username}'s KYC is already approved.", "info")
    else:
        user.kyc_status = "approved"
        user.kyc_approved_at = datetime.utcnow()
        user.kyc_approved_by = current_user.id

        db.session.commit()
        flash(
            f"{user.username}'s KYC verification has been approved successfully!",
            "success",
        )

    return redirect(url_for("admin.kyc_verification_detail", user_id=user_id))


@admin.route("/kyc-verifications/<int:user_id>/reject", methods=["POST"])
@login_required
@admin_required
def reject_user_kyc(user_id):
    """Reject user's KYC verification"""
    user = User.query.get_or_404(user_id)

    rejection_reason = request.form.get("rejection_reason", "")

    user.kyc_status = "rejected"
    user.kyc_approved_at = None
    user.kyc_approved_by = None

    # Auto-deactivate account when KYC is rejected
    user.is_active = False

    db.session.commit()
    flash(
        f"{user.username}'s KYC verification has been rejected and account has been deactivated.",
        "warning",
    )

    return redirect(url_for("admin.kyc_verification_detail", user_id=user_id))


@admin.route("/kyc-verifications/<int:user_id>/document/<int:document_id>")
@login_required
@admin_required
def download_kyc_document(user_id, document_id):
    """Download a user's KYC document"""
    document = KYCDocument.query.get_or_404(document_id)

    # Verify document belongs to the specified user
    if document.user_id != user_id:
        flash("Invalid document access.", "error")
        return redirect(url_for("admin.kyc_verifications"))

    if not os.path.exists(document.file_path):
        flash("Document file not found.", "error")
        return redirect(url_for("admin.kyc_verification_detail", user_id=user_id))

    return send_file(
        document.file_path, as_attachment=True, download_name=document.document_name
    )

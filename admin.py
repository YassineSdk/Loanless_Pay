from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from decorators import admin_required
from models import db, User, Loan
from sqlalchemy import func, desc
from datetime import datetime, timedelta

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
@admin.route("/dashboard")
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    # Get statistics
    total_users = User.query.filter_by(is_admin=False).count()
    total_loans = Loan.query.count()
    pending_loans = Loan.query.filter_by(status="pending").count()
    approved_loans = Loan.query.filter_by(status="approved").count()
    rejected_loans = Loan.query.filter_by(status="rejected").count()
    active_loans = Loan.query.filter_by(status="active").count()

    # Calculate total loan amount
    total_amount = db.session.query(func.sum(Loan.amount)).scalar() or 0
    approved_amount = (
        db.session.query(func.sum(Loan.amount))
        .filter(Loan.status.in_(["approved", "active"]))
        .scalar()
        or 0
    )

    # Get recent loans (last 5)
    recent_loans = Loan.query.order_by(desc(Loan.created_at)).limit(5).all()

    # Get recent users (last 5)
    recent_users = (
        User.query.filter_by(is_admin=False)
        .order_by(desc(User.created_at))
        .limit(5)
        .all()
    )

    # Calculate approval rate
    total_reviewed = approved_loans + rejected_loans
    approval_rate = (approved_loans / total_reviewed * 100) if total_reviewed > 0 else 0

    # Loans by sector
    loans_by_sector = (
        db.session.query(Loan.sector, func.count(Loan.id)).group_by(Loan.sector).all()
    )

    stats = {
        "total_users": total_users,
        "total_loans": total_loans,
        "pending_loans": pending_loans,
        "approved_loans": approved_loans,
        "rejected_loans": rejected_loans,
        "active_loans": active_loans,
        "total_amount": total_amount,
        "approved_amount": approved_amount,
        "approval_rate": round(approval_rate, 1),
        "recent_loans": recent_loans,
        "recent_users": recent_users,
        "loans_by_sector": dict(loans_by_sector),
    }

    return render_template("admin/dashboard.html", stats=stats)


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

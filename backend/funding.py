from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, FundingTransaction, FundingUsage, Loan
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from functools import wraps

funding = Blueprint("funding", __name__, url_prefix="/funding")


def funding_party_required(f):
    """Decorator to ensure user is a funding party"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login"))
        if current_user.user_role != "funding_party":
            flash("Access denied. This area is for funding partners only.", "error")
            return redirect(url_for("main"))
        return f(*args, **kwargs)
    return decorated_function


@funding.route("/")
@funding.route("/dashboard")
@login_required
@funding_party_required
def dashboard():
    """Funding party dashboard with overview"""

    # Calculate total funding provided
    total_deposits = db.session.query(func.sum(FundingTransaction.amount)).filter(
        FundingTransaction.funder_id == current_user.id,
        FundingTransaction.transaction_type == "deposit",
        FundingTransaction.status == "completed"
    ).scalar() or 0.0

    total_withdrawals = db.session.query(func.sum(FundingTransaction.amount)).filter(
        FundingTransaction.funder_id == current_user.id,
        FundingTransaction.transaction_type == "withdrawal",
        FundingTransaction.status == "completed"
    ).scalar() or 0.0

    total_funding_provided = total_deposits - total_withdrawals

    # Calculate total funding consumed (all approved/active loans)
    total_consumed = db.session.query(func.sum(Loan.amount)).filter(
        Loan.status.in_(["approved", "active"])
    ).scalar() or 0.0

    # Calculate available funding
    available_funding = total_funding_provided - total_consumed

    # Calculate utilization rate
    utilization_rate = (total_consumed / total_funding_provided * 100) if total_funding_provided > 0 else 0

    # Get recent transactions
    recent_transactions = FundingTransaction.query.filter_by(
        funder_id=current_user.id
    ).order_by(desc(FundingTransaction.created_at)).limit(10).all()

    # Get active loans consuming funding
    active_loans = Loan.query.filter(
        Loan.status.in_(["approved", "active"])
    ).order_by(desc(Loan.created_at)).limit(10).all()

    # Calculate monthly statistics for last 6 months
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    monthly_stats = db.session.query(
        func.strftime('%Y-%m', Loan.created_at).label('month'),
        func.sum(Loan.amount).label('total_amount'),
        func.count(Loan.id).label('loan_count')
    ).filter(
        Loan.created_at >= six_months_ago,
        Loan.status.in_(["approved", "active", "completed"])
    ).group_by('month').all()

    # Funding growth over time
    funding_growth = db.session.query(
        func.strftime('%Y-%m', FundingTransaction.created_at).label('month'),
        func.sum(FundingTransaction.amount).label('total_deposited')
    ).filter(
        FundingTransaction.funder_id == current_user.id,
        FundingTransaction.created_at >= six_months_ago,
        FundingTransaction.transaction_type == "deposit"
    ).group_by('month').all()

    # Loan status breakdown
    loan_status_breakdown = db.session.query(
        Loan.status,
        func.count(Loan.id).label('count'),
        func.sum(Loan.amount).label('total_amount')
    ).filter(
        Loan.status.in_(["approved", "active", "completed", "rejected"])
    ).group_by(Loan.status).all()

    # Calculate return metrics
    total_loans_funded = db.session.query(func.count(Loan.id)).filter(
        Loan.status.in_(["approved", "active", "completed"])
    ).scalar() or 0

    completed_loans = db.session.query(func.count(Loan.id)).filter(
        Loan.status == "completed"
    ).scalar() or 0

    completion_rate = (completed_loans / total_loans_funded * 100) if total_loans_funded > 0 else 0

    stats = {
        "total_funding_provided": total_funding_provided,
        "total_consumed": total_consumed,
        "available_funding": available_funding,
        "utilization_rate": utilization_rate,
        "recent_transactions": recent_transactions,
        "active_loans": active_loans,
        "monthly_stats": monthly_stats,
        "funding_growth": funding_growth,
        "loan_status_breakdown": loan_status_breakdown,
        "total_loans_funded": total_loans_funded,
        "completion_rate": completion_rate,
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals
    }

    return render_template("funding/dashboard.html", stats=stats)


@funding.route("/add-funding", methods=["GET", "POST"])
@login_required
@funding_party_required
def add_funding():
    """Add new funding (top-up)"""
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount", 0))
            notes = request.form.get("notes", "")

            if amount <= 0:
                flash("Please enter a valid funding amount.", "error")
                return redirect(url_for("funding.add_funding"))

            # Create funding transaction
            transaction = FundingTransaction(
                funder_id=current_user.id,
                amount=amount,
                transaction_type="deposit",
                status="completed",
                notes=notes
            )

            db.session.add(transaction)
            db.session.commit()

            flash(f"Successfully added ${amount:,.2f} to your funding pool!", "success")
            return redirect(url_for("funding.dashboard"))

        except ValueError:
            flash("Invalid amount entered.", "error")
            return redirect(url_for("funding.add_funding"))
        except Exception as e:
            flash(f"Error processing funding: {str(e)}", "error")
            return redirect(url_for("funding.add_funding"))

    return render_template("funding/add_funding.html")


@funding.route("/transactions")
@login_required
@funding_party_required
def transactions():
    """View all funding transactions"""
    page = request.args.get("page", 1, type=int)
    per_page = 20

    transaction_query = FundingTransaction.query.filter_by(
        funder_id=current_user.id
    ).order_by(desc(FundingTransaction.created_at))

    transactions_paginated = transaction_query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        "funding/transactions.html",
        transactions=transactions_paginated
    )


@funding.route("/analytics")
@login_required
@funding_party_required
def analytics():
    """Detailed analytics for funding party"""

    # Get comprehensive statistics
    total_funding = db.session.query(func.sum(FundingTransaction.amount)).filter(
        FundingTransaction.funder_id == current_user.id,
        FundingTransaction.transaction_type == "deposit",
        FundingTransaction.status == "completed"
    ).scalar() or 0.0

    total_consumed = db.session.query(func.sum(Loan.amount)).filter(
        Loan.status.in_(["approved", "active"])
    ).scalar() or 0.0

    # Sector-wise breakdown
    sector_breakdown = db.session.query(
        Loan.sector,
        func.count(Loan.id).label('count'),
        func.sum(Loan.amount).label('total_amount')
    ).filter(
        Loan.status.in_(["approved", "active", "completed"])
    ).group_by(Loan.sector).all()

    # Loan duration analysis
    duration_breakdown = db.session.query(
        Loan.payment_period,
        func.count(Loan.id).label('count'),
        func.avg(Loan.amount).label('avg_amount')
    ).filter(
        Loan.status.in_(["approved", "active", "completed"])
    ).group_by(Loan.payment_period).all()

    # Monthly funding performance (last 12 months)
    twelve_months_ago = datetime.utcnow() - timedelta(days=365)
    monthly_performance = db.session.query(
        func.strftime('%Y-%m', Loan.created_at).label('month'),
        func.count(Loan.id).label('loans_count'),
        func.sum(Loan.amount).label('total_disbursed'),
        func.avg(Loan.amount).label('avg_loan_size')
    ).filter(
        Loan.created_at >= twelve_months_ago,
        Loan.status.in_(["approved", "active", "completed"])
    ).group_by('month').order_by('month').all()

    # Risk metrics
    total_loans = Loan.query.filter(
        Loan.status.in_(["approved", "active", "completed", "rejected"])
    ).count()

    approved_loans = Loan.query.filter(
        Loan.status.in_(["approved", "active", "completed"])
    ).count()

    approval_rate = (approved_loans / total_loans * 100) if total_loans > 0 else 0

    analytics_data = {
        "total_funding": total_funding,
        "total_consumed": total_consumed,
        "available": total_funding - total_consumed,
        "sector_breakdown": sector_breakdown,
        "duration_breakdown": duration_breakdown,
        "monthly_performance": monthly_performance,
        "approval_rate": approval_rate,
        "total_loans": total_loans
    }

    return render_template("funding/analytics.html", analytics=analytics_data)


@funding.route("/loans")
@login_required
@funding_party_required
def funded_loans():
    """View all loans funded by the platform"""
    status_filter = request.args.get("status", "")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    # Build query
    query = Loan.query

    # Apply filters
    if status_filter:
        query = query.filter_by(status=status_filter)
    else:
        query = query.filter(Loan.status.in_(["approved", "active", "completed"]))

    # Paginate
    loans_paginated = query.order_by(desc(Loan.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        "funding/loans.html",
        loans=loans_paginated,
        status_filter=status_filter
    )


@funding.route("/profile", methods=["GET", "POST"])
@login_required
@funding_party_required
def profile():
    """Funding party profile management"""
    if request.method == "POST":
        current_user.company_name = request.form.get("company_name", current_user.company_name)
        current_user.company_registration = request.form.get("company_registration", current_user.company_registration)
        current_user.email = request.form.get("email", current_user.email)
        current_user.phone_number = request.form.get("phone_number", current_user.phone_number)
        current_user.address = request.form.get("address", current_user.address)

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("funding.profile"))

    return render_template("funding/profile.html")


# API Endpoints for AJAX/Charts

@funding.route("/api/funding-stats")
@login_required
@funding_party_required
def api_funding_stats():
    """API endpoint for real-time funding statistics"""

    total_deposits = db.session.query(func.sum(FundingTransaction.amount)).filter(
        FundingTransaction.funder_id == current_user.id,
        FundingTransaction.transaction_type == "deposit",
        FundingTransaction.status == "completed"
    ).scalar() or 0.0

    total_consumed = db.session.query(func.sum(Loan.amount)).filter(
        Loan.status.in_(["approved", "active"])
    ).scalar() or 0.0

    return jsonify({
        "success": True,
        "total_funding": total_deposits,
        "consumed": total_consumed,
        "available": total_deposits - total_consumed,
        "utilization_rate": (total_consumed / total_deposits * 100) if total_deposits > 0 else 0
    })


@funding.route("/api/chart-data")
@login_required
@funding_party_required
def api_chart_data():
    """API endpoint for chart data"""
    chart_type = request.args.get("type", "monthly")

    if chart_type == "monthly":
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        data = db.session.query(
            func.strftime('%Y-%m', Loan.created_at).label('month'),
            func.sum(Loan.amount).label('total')
        ).filter(
            Loan.created_at >= six_months_ago,
            Loan.status.in_(["approved", "active", "completed"])
        ).group_by('month').order_by('month').all()

        return jsonify({
            "success": True,
            "labels": [item.month for item in data],
            "values": [float(item.total) for item in data]
        })

    elif chart_type == "sector":
        data = db.session.query(
            Loan.sector,
            func.sum(Loan.amount).label('total')
        ).filter(
            Loan.status.in_(["approved", "active", "completed"])
        ).group_by(Loan.sector).all()

        return jsonify({
            "success": True,
            "labels": [item.sector for item in data],
            "values": [float(item.total) for item in data]
        })

    elif chart_type == "status":
        data = db.session.query(
            Loan.status,
            func.count(Loan.id).label('count')
        ).group_by(Loan.status).all()

        return jsonify({
            "success": True,
            "labels": [item.status.title() for item in data],
            "values": [item.count for item in data]
        })

    return jsonify({"success": False, "message": "Invalid chart type"})

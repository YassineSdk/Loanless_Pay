from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """
    Decorator to require admin privileges for a route.
    Returns 403 Forbidden if user is not an admin.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login"))

        if not current_user.is_admin:
            flash("You do not have permission to access this page.", "error")
            abort(403)

        if not current_user.is_active:
            flash("Your account has been deactivated.", "error")
            return redirect(url_for("logout"))

        return f(*args, **kwargs)

    return decorated_function

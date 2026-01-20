"""
Decorators for role-based access control.

This module provides decorators to protect routes based on user roles.
- @admin_required: Restricts access to admin users only (role == 1)
"""

from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """Decorator to restrict access to admin users only.
    
    Usage:
        @app.route('/admin/dashboard')
        @login_required
        @admin_required
        def admin_dashboard():
            ...
    
    If the user is not authenticated, Flask-Login's @login_required will handle it.
    If the user is authenticated but not an admin (role != 1), they get a 403 flash
    and are redirected to the home page.
    
    Args:
        f: The view function to decorate.
        
    Returns:
        The decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated and has admin role
        if not current_user.is_authenticated:
            flash("Vui lòng đăng nhập để tiếp tục.", "error")
            return redirect(url_for("auth.show_sign_in_page"))
        
        if not current_user.is_admin:
            flash("Bạn không có quyền truy cập trang này.", "error")
            return redirect(url_for("main.show_home_page"))
        
        return f(*args, **kwargs)
    
    return decorated_function

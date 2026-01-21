"""
Các decorator cho kiểm soát truy cập dựa trên vai trò.

Module này cung cấp các decorator để bảo vệ các route dựa trên vai trò người dùng.
- @admin_required: Chỉ cho phép người dùng admin truy cập (role == 1)
"""

from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """Decorator để chỉ cho phép người dùng admin truy cập.
    
    Cách sử dụng:
        @app.route('/admin/dashboard')
        @login_required
        @admin_required
        def admin_dashboard():
            ...
    
    Nếu người dùng chưa xác thực, Flask-Login's @login_required sẽ xử lý.
    Nếu người dùng đã xác thực nhưng không phải admin (role != 1), họ sẽ nhận
    thông báo lỗi và được chuyển hướng về trang chủ.
    
    Args:
        f: Hàm view cần được trang trí.
        
    Returns:
        Hàm đã được trang trí.
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

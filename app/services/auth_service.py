from datetime import datetime
import re
from typing import List, Optional, Tuple

from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from app.extensions import db
from app.models.account import Account


GENERIC_LOGIN_ERROR = "Thông tin đăng nhập không đúng hoặc tài khoản bị khóa."
REGISTRATION_DUPLICATE_ERROR = "Thông tin đăng ký không hợp lệ hoặc đã được sử dụng."
REGISTRATION_GENERIC_ERROR = "Không thể tạo tài khoản. Vui lòng thử lại."
PASSWORD_MIN_LENGTH = 8
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_login_input(identifier: str, password: str) -> List[str]:
    errors = []
    if not identifier or not identifier.strip():
        errors.append("Vui lòng nhập email hoặc tên đăng nhập.")
    if not password or not password.strip():
        errors.append("Vui lòng nhập mật khẩu.")
    return errors


def find_account_by_identifier(identifier: str) -> Optional[Account]:
    if not identifier:
        return None
    normalized = identifier.strip().lower()
    return (
        Account.query.filter(
            or_(
                func.lower(Account.email) == normalized,
                func.lower(Account.ten_tai_khoan) == normalized,
            )
        )
        .limit(1)
        .first()
    )


def authenticate_user(identifier: str, password: str) -> Tuple[Optional[Account], str]:
    validation_errors = validate_login_input(identifier, password)
    if validation_errors:
        return None, validation_errors[0]

    account = find_account_by_identifier(identifier)
    if not account:
        return None, GENERIC_LOGIN_ERROR

    if not check_password_hash(account.password_hash, password):
        return None, GENERIC_LOGIN_ERROR

    if not account.is_active:
        return None, GENERIC_LOGIN_ERROR

    return account, ""


def validate_registration_input(
    username: str,
    email: str,
    password: str,
    confirm_password: str,
    full_name: str,
    phone: str,
) -> List[str]:
    errors = []
    if not username or not username.strip():
        errors.append("Vui lòng nhập tên đăng nhập.")
    if not email or not email.strip():
        errors.append("Vui lòng nhập email.")
    elif not EMAIL_REGEX.match(email.strip()):
        errors.append("Email không hợp lệ.")
    if not password or not password.strip():
        errors.append("Vui lòng nhập mật khẩu.")
    elif len(password) < PASSWORD_MIN_LENGTH:
        errors.append(f"Mật khẩu phải có ít nhất {PASSWORD_MIN_LENGTH} ký tự.")
    if password and confirm_password and password != confirm_password:
        errors.append("Mật khẩu xác nhận không khớp.")
    if not full_name or not full_name.strip():
        errors.append("Vui lòng nhập họ và tên.")
    if not phone or not phone.strip():
        errors.append("Vui lòng nhập số điện thoại.")
    return errors


def find_account_by_username(username: str) -> Optional[Account]:
    if not username:
        return None
    normalized = username.strip().lower()
    return (
        Account.query.filter(func.lower(Account.ten_tai_khoan) == normalized)
        .limit(1)
        .first()
    )


def find_account_by_email(email: str) -> Optional[Account]:
    if not email:
        return None
    normalized = email.strip().lower()
    return (
        Account.query.filter(func.lower(Account.email) == normalized)
        .limit(1)
        .first()
    )


def register_user(
    username: str,
    email: str,
    password: str,
    confirm_password: str,
    full_name: str,
    phone: str,
) -> Tuple[Optional[Account], str]:
    validation_errors = validate_registration_input(
        username, email, password, confirm_password, full_name, phone
    )
    if validation_errors:
        return None, validation_errors[0]

    if find_account_by_username(username) or find_account_by_email(email):
        return None, REGISTRATION_DUPLICATE_ERROR

    account = Account(
        ten_tai_khoan=username.strip(),
        email=email.strip().lower(),
        ho_ten=full_name.strip(),
        so_dien_thoai=phone.strip(),
        dia_chi="Chưa cập nhật",
        ngay_sinh=datetime.utcnow(),
        gioi_tinh=0,
        trang_thai=1,
        role=0,
    )
    account.set_password(password)

    db.session.add(account)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None, REGISTRATION_DUPLICATE_ERROR
    except Exception:
        db.session.rollback()
        return None, REGISTRATION_GENERIC_ERROR

    return account, ""

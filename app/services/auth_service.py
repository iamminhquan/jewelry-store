from typing import List, Optional, Tuple

from sqlalchemy import func, or_
from werkzeug.security import check_password_hash

from app.models.account import Account


GENERIC_LOGIN_ERROR = "Thông tin đăng nhập không đúng hoặc tài khoản bị khóa."


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

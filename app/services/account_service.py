"""
Service layer for Account management.

This module contains business logic for managing user accounts.
NO Flask request/response handling - only pure business logic.
"""

from typing import List, Optional

from sqlalchemy import or_, cast
from sqlalchemy.types import String

from app.extensions import db
from app.models.account import Account


class AccountServiceError(Exception):
    """Base exception for account service errors."""
    pass


class AccountNotFoundError(AccountServiceError):
    """Raised when an account is not found."""
    pass


class DuplicateAccountError(AccountServiceError):
    """Raised when attempting to create a duplicate account."""
    pass


class ValidationError(AccountServiceError):
    """Raised when validation fails."""
    pass


def get_all_accounts() -> List[Account]:
    """Fetch all user accounts ordered by ID descending.

    Returns:
        List[Account]: List of all accounts.
    """
    return Account.query.order_by(Account.ma_tai_khoan.desc()).all()


def get_account_page(keyword: str, page: int, per_page: int = 10):
    """Get paginated accounts with optional search filter.

    Args:
        keyword (str): Search keyword for filtering.
        page (int): Current page number.
        per_page (int, optional): Items per page. Defaults to 10.

    Returns:
        tuple: (pagination, accounts, total_accounts)
    """
    query = build_account_query(keyword)

    pagination = db.paginate(
        query.order_by(Account.ma_tai_khoan.desc()),
        page=page,
        per_page=per_page,
        error_out=False,
    )

    total_accounts = Account.query.count()

    return (
        pagination,
        pagination.items,
        total_accounts,
    )


def build_account_query(keyword: str):
    """Build account query with search filter.

    Args:
        keyword (str): Search keyword.

    Returns:
        BaseQuery: Query with applied filters.
    """
    query = Account.query

    if keyword:
        keyword = keyword.strip()
        query = query.filter(
            or_(
                cast(Account.ma_tai_khoan, String).like(f"%{keyword}%"),
                Account.ten_tai_khoan.ilike(f"%{keyword}%"),
                Account.email.ilike(f"%{keyword}%"),
                Account.ho_ten.ilike(f"%{keyword}%"),
                Account.so_dien_thoai.ilike(f"%{keyword}%"),
            )
        )

    return query


def search_accounts(keyword: str) -> List[Account]:
    """Search accounts by username, email, full name, or phone.

    Args:
        keyword (str): Search keyword.

    Returns:
        List[Account]: List of matching accounts.
    """
    if not keyword or not keyword.strip():
        return get_all_accounts()

    query = build_account_query(keyword)
    return query.order_by(Account.ma_tai_khoan.desc()).all()


def get_account_by_id(account_id: int) -> Optional[Account]:
    """Fetch account by ID.

    Args:
        account_id (int): Account ID.

    Returns:
        Optional[Account]: Account if found, None otherwise.
    """
    return Account.query.get(account_id)


def get_account_or_404(account_id: int) -> Account:
    """Fetch account by ID or raise 404.

    Args:
        account_id (int): Account ID.

    Returns:
        Account: Found account.

    Raises:
        AccountNotFoundError: If account not found.
    """
    account = Account.query.get_or_404(account_id)
    return account


def create_account(
    ten_tai_khoan: str,
    email: str,
    password: str,
    ho_ten: str,
    ngay_sinh,
    gioi_tinh: int,
    so_dien_thoai: str,
    dia_chi: str,
    role: int = 0,
    trang_thai: int = 1,
) -> Account:
    """Create a new user account.

    Args:
        ten_tai_khoan (str): Username.
        email (str): Email address.
        password (str): Plain text password.
        ho_ten (str): Full name.
        ngay_sinh: Date of birth.
        gioi_tinh (int): Gender (0 or 1).
        so_dien_thoai (str): Phone number.
        dia_chi (str): Address.
        role (int, optional): User role (0=user, 1=admin). Defaults to 0.
        trang_thai (int, optional): Account status (0=inactive, 1=active). Defaults to 1.

    Returns:
        Account: Newly created account.

    Raises:
        ValidationError: If required fields are missing.
        DuplicateAccountError: If username or email already exists.
    """
    # Validate required fields
    if not ten_tai_khoan or not ten_tai_khoan.strip():
        raise ValidationError("Tên tài khoản không được để trống.")
    
    if not email or not email.strip():
        raise ValidationError("Email không được để trống.")
    
    if not password or not password.strip():
        raise ValidationError("Mật khẩu không được để trống.")
    
    if not ho_ten or not ho_ten.strip():
        raise ValidationError("Họ tên không được để trống.")

    # Check for duplicate username
    existing_username = Account.query.filter_by(
        ten_tai_khoan=ten_tai_khoan.strip()
    ).first()
    if existing_username:
        raise DuplicateAccountError("Tên tài khoản đã tồn tại.")

    # Check for duplicate email
    existing_email = Account.query.filter_by(email=email.strip()).first()
    if existing_email:
        raise DuplicateAccountError("Email đã được sử dụng.")

    # Create new account
    account = Account(
        ten_tai_khoan=ten_tai_khoan.strip(),
        email=email.strip(),
        ho_ten=ho_ten.strip(),
        ngay_sinh=ngay_sinh,
        gioi_tinh=gioi_tinh,
        so_dien_thoai=so_dien_thoai.strip() if so_dien_thoai else "",
        dia_chi=dia_chi.strip() if dia_chi else "",
        role=role,
        trang_thai=trang_thai,
    )
    account.set_password(password)

    db.session.add(account)
    db.session.commit()

    return account


def update_account(
    account: Account,
    ten_tai_khoan: str,
    email: str,
    ho_ten: str,
    ngay_sinh,
    gioi_tinh: int,
    so_dien_thoai: str,
    dia_chi: str,
    role: int,
    trang_thai: int,
    password: Optional[str] = None,
) -> Account:
    """Update an existing account.

    Args:
        account (Account): Account to update.
        ten_tai_khoan (str): New username.
        email (str): New email.
        ho_ten (str): New full name.
        ngay_sinh: New date of birth.
        gioi_tinh (int): New gender.
        so_dien_thoai (str): New phone number.
        dia_chi (str): New address.
        role (int): New role.
        trang_thai (int): New status.
        password (Optional[str], optional): New password. Defaults to None.

    Returns:
        Account: Updated account.

    Raises:
        ValidationError: If required fields are missing.
        DuplicateAccountError: If username or email conflicts with another account.
    """
    # Validate required fields
    if not ten_tai_khoan or not ten_tai_khoan.strip():
        raise ValidationError("Tên tài khoản không được để trống.")
    
    if not email or not email.strip():
        raise ValidationError("Email không được để trống.")
    
    if not ho_ten or not ho_ten.strip():
        raise ValidationError("Họ tên không được để trống.")

    # Check for duplicate username (excluding current account)
    existing_username = Account.query.filter(
        Account.ten_tai_khoan == ten_tai_khoan.strip(),
        Account.ma_tai_khoan != account.ma_tai_khoan
    ).first()
    if existing_username:
        raise DuplicateAccountError("Tên tài khoản đã tồn tại.")

    # Check for duplicate email (excluding current account)
    existing_email = Account.query.filter(
        Account.email == email.strip(),
        Account.ma_tai_khoan != account.ma_tai_khoan
    ).first()
    if existing_email:
        raise DuplicateAccountError("Email đã được sử dụng.")

    # Update account fields
    account.ten_tai_khoan = ten_tai_khoan.strip()
    account.email = email.strip()
    account.ho_ten = ho_ten.strip()
    account.ngay_sinh = ngay_sinh
    account.gioi_tinh = gioi_tinh
    account.so_dien_thoai = so_dien_thoai.strip() if so_dien_thoai else ""
    account.dia_chi = dia_chi.strip() if dia_chi else ""
    account.role = role
    account.trang_thai = trang_thai

    # Update password only if provided
    if password and password.strip():
        account.set_password(password.strip())

    db.session.commit()

    return account


def get_account_stats() -> dict:
    """Get account statistics.

    Returns:
        dict: Statistics including total accounts, active accounts, admin count.
    """
    total = Account.query.count()
    active = Account.query.filter_by(trang_thai=1).count()
    admins = Account.query.filter_by(role=1).count()
    users = Account.query.filter_by(role=0).count()

    return {
        "total": total,
        "active": active,
        "inactive": total - active,
        "admins": admins,
        "users": users,
    }

"""Service layer for Comment management.

This module contains business logic for managing comments/reviews.
No Flask request/response handling - only data access and domain logic.
"""

from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import or_, cast
from sqlalchemy.types import String

from app.extensions import db
from app.models.account import Account
from app.models.comment import Comment
from app.models.product import Product


class CommentServiceError(Exception):
    """Base exception for comment service errors."""


class CommentNotFoundError(CommentServiceError):
    """Raised when a comment cannot be found."""


class CommentStatusError(CommentServiceError):
    """Raised when a comment status is invalid."""


class CommentStatus:
    """Comment status constants for admin display."""

    PENDING = 0  # Chờ duyệt
    APPROVED = 1  # Đã duyệt
    HIDDEN = 2  # Ẩn

    ALL = [PENDING, APPROVED, HIDDEN]

    LABELS = {
        PENDING: "Chờ duyệt",
        APPROVED: "Đã duyệt",
        HIDDEN: "Ẩn",
    }

    BADGE_CLASSES = {
        PENDING: "bg-amber-50 text-amber-700 ring-1 ring-amber-200",
        APPROVED: "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-200",
        HIDDEN: "bg-slate-100 text-slate-700 ring-1 ring-slate-200",
    }

    @classmethod
    def get_label(cls, status: Optional[int]) -> str:
        """Get display label for a status."""
        if status is None:
            return cls.LABELS.get(cls.PENDING, "Không xác định")
        return cls.LABELS.get(status, "Không xác định")

    @classmethod
    def get_badge_class(cls, status: Optional[int]) -> str:
        """Get Tailwind CSS classes for a status badge."""
        if status is None:
            status = cls.PENDING
        return cls.BADGE_CLASSES.get(
            status, "bg-slate-100 text-slate-700 ring-1 ring-slate-200"
        )


def _parse_int(value) -> Optional[int]:
    """Parse an integer from a string-like value."""
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _normalize_status(status) -> Optional[int]:
    """Normalize status filter input to a valid status or None."""
    status_int = _parse_int(status)
    if status_int in CommentStatus.ALL:
        return status_int
    return None


def _build_comment_query(
    keyword: Optional[str],
    product_id: Optional[int],
    user_id: Optional[int],
    status: Optional[int],
):
    """Build query for comment search with optional filters."""
    query = db.session.query(Comment, Product, Account).outerjoin(
        Product, Comment.ma_san_pham == Product.ma_san_pham
    ).outerjoin(Account, Comment.nguoi_danh_gia == Account.ma_tai_khoan)

    if status is not None:
        query = query.filter(Comment.trang_thai == status)

    if product_id is not None:
        query = query.filter(Comment.ma_san_pham == product_id)

    if user_id is not None:
        query = query.filter(Comment.nguoi_danh_gia == user_id)

    if keyword:
        keyword = keyword.strip()
        like_value = f"%{keyword}%"
        query = query.filter(
            or_(
                cast(Comment.ma_danh_gia, String).like(like_value),
                Comment.noi_dung.ilike(like_value),
                Product.ten_san_pham.ilike(like_value),
                Account.ho_ten.ilike(like_value),
                Account.ten_tai_khoan.ilike(like_value),
                Account.email.ilike(like_value),
            )
        )

    return query


def _format_comment_records(records) -> List[dict]:
    """Convert query results to list of dictionaries for templates."""
    result = []
    for comment, product, account in records:
        result.append(
            {
                "comment": comment,
                "product": product,
                "account": account,
            }
        )
    return result


def get_all_comments() -> List[dict]:
    """Fetch all comments ordered by newest first."""
    query = _build_comment_query(None, None, None, None)
    records = query.order_by(Comment.ma_danh_gia.desc()).all()
    return _format_comment_records(records)


def search_comments(
    keyword: Optional[str] = None,
    product_id: Optional[int] = None,
    user_id: Optional[int] = None,
    status: Optional[int] = None,
) -> List[dict]:
    """Search comments by keyword, product, user, and status."""
    product_id_int = _parse_int(product_id)
    user_id_int = _parse_int(user_id)
    status_int = _normalize_status(status)

    query = _build_comment_query(keyword, product_id_int, user_id_int, status_int)
    records = query.order_by(Comment.ma_danh_gia.desc()).all()
    return _format_comment_records(records)


def get_comment_by_id(comment_id: int) -> Optional[Comment]:
    """Fetch a comment by id."""
    return Comment.query.get(comment_id)


def get_comment_detail(comment_id: int) -> Optional[dict]:
    """Fetch a single comment with product and account info."""
    record = (
        db.session.query(Comment, Product, Account)
        .outerjoin(Product, Comment.ma_san_pham == Product.ma_san_pham)
        .outerjoin(Account, Comment.nguoi_danh_gia == Account.ma_tai_khoan)
        .filter(Comment.ma_danh_gia == comment_id)
        .first()
    )

    if not record:
        return None

    comment, product, account = record
    return {"comment": comment, "product": product, "account": account}


def update_comment_status(comment_id: int, status: int) -> Comment:
    """Update comment status.

    Raises:
        CommentNotFoundError: When comment does not exist.
        CommentStatusError: When status is invalid.
    """
    comment = Comment.query.get(comment_id)
    if not comment:
        raise CommentNotFoundError("Không tìm thấy đánh giá.")

    status_int = _parse_int(status)
    if status_int not in CommentStatus.ALL:
        raise CommentStatusError("Trạng thái đánh giá không hợp lệ.")

    comment.trang_thai = status_int
    comment.ngay_chinh_sua = datetime.utcnow()
    db.session.commit()
    return comment


def delete_comment(comment_id: int) -> None:
    """Delete a comment permanently.

    Raises:
        CommentNotFoundError: When comment does not exist.
    """
    comment = Comment.query.get(comment_id)
    if not comment:
        raise CommentNotFoundError("Không tìm thấy đánh giá.")

    db.session.delete(comment)
    db.session.commit()


def get_comment_filters() -> Tuple[List[Product], List[Account]]:
    """Fetch products and accounts for filter dropdowns."""
    products = Product.query.order_by(Product.ten_san_pham.asc()).all()
    accounts = Account.query.order_by(Account.ho_ten.asc()).all()
    return products, accounts

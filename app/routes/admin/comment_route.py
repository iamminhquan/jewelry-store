"""Admin Comment Management Routes."""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.decorators import admin_required
from app.services.comment_service import (
    CommentNotFoundError,
    CommentStatus,
    CommentStatusError,
    delete_comment,
    get_all_comments,
    get_comment_detail,
    get_comment_filters,
    search_comments,
    update_comment_status,
)


comment_bp = Blueprint(
    "comment",
    __name__,
    url_prefix="/admin",
)


@comment_bp.route("/comments", methods=["GET"])
@login_required
@admin_required
def show_comment_page():
    """Display list of all comments."""
    comments = get_all_comments()

    return render_template(
        "admin/comment/comment.html",
        comments=comments,
        CommentStatus=CommentStatus,
    )


@comment_bp.route("/comments/search", methods=["GET"])
@login_required
@admin_required
def search_comments_page():
    """Search comments by keyword, status, product, or user."""
    keyword = request.args.get("keyword", "").strip()
    status = request.args.get("status")
    product_id = request.args.get("product_id")
    user_id = request.args.get("user_id")

    comments = search_comments(keyword, product_id, user_id, status)
    products, accounts = get_comment_filters()

    return render_template(
        "admin/comment/comment_search.html",
        comments=comments,
        products=products,
        accounts=accounts,
        keyword=keyword,
        status=status,
        product_id=product_id,
        user_id=user_id,
        total_results=len(comments),
        CommentStatus=CommentStatus,
    )


@comment_bp.route("/comments/<int:comment_id>", methods=["GET"])
@login_required
@admin_required
def show_comment_detail_page(comment_id: int):
    """Display detail of a single comment."""
    comment_data = get_comment_detail(comment_id)
    if not comment_data:
        abort(404)

    return render_template(
        "admin/comment/comment_detail.html",
        comment_data=comment_data,
        CommentStatus=CommentStatus,
    )


@comment_bp.route("/comments/<int:comment_id>/update-status", methods=["POST"])
@login_required
@admin_required
def update_comment_status_route(comment_id: int):
    """Update comment status (approve/hide/pending)."""
    new_status = request.form.get("status")
    next_url = (
        request.form.get("next")
        or request.referrer
        or url_for("comment.show_comment_page")
    )

    try:
        update_comment_status(comment_id, new_status)
        flash("Cập nhật trạng thái đánh giá thành công.", "success")
    except CommentNotFoundError:
        abort(404)
    except CommentStatusError as exc:
        flash(str(exc), "error")

    return redirect(next_url)


@comment_bp.route("/comments/<int:comment_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_comment_route(comment_id: int):
    """Delete a comment permanently."""
    next_url = (
        request.form.get("next")
        or request.referrer
        or url_for("comment.show_comment_page")
    )

    try:
        delete_comment(comment_id)
        flash("Đã xoá đánh giá thành công.", "success")
    except CommentNotFoundError:
        abort(404)

    return redirect(next_url)


@comment_bp.route("/danhgia/", methods=["GET"])
@login_required
@admin_required
def legacy_comment_page():
    """Redirect legacy route to the new admin comments page."""
    return redirect(url_for("comment.show_comment_page"), code=301)

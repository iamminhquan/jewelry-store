from flask import Blueprint, render_template, request
from app.models.product import Product


search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/search",
)


@search_bp.route("/", methods=["GET"])
def search_products():
    keyword = request.args.get("keyword", "").strip()
    page = request.args.get("page", 1, type=int)
    query = Product.query.filter(Product.trang_thai == 1)

    if keyword:
        query = query.filter(Product.ten_san_pham.ilike(f"%{keyword}%"))

    pagination = query.order_by(Product.ngay_tao.desc()).paginate(page=page, per_page=6)

    return render_template(
        "user/search_results.html",
        products=pagination.items,
        pagination=pagination,
        keyword=keyword,
    )

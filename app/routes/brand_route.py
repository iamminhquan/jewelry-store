from flask import Blueprint, render_template, request, redirect, url_for
from app.models.brand import Brand
from app.extensions import db
from sqlalchemy import or_, cast
from sqlalchemy.types import String

# người chỉnh sửa: Nguyễn Thái Nguyên
# thời gian chỉnh sửa: 17/01/2025
# nội dung: viết các route quản lý thương hiệu (theo đúng CSDL hiện tại)

brand_bp = Blueprint(
    "brand",
    __name__,
    url_prefix="/admin/brand"
)


@brand_bp.route("/", strict_slashes=False)
def show_all_brand():
    # # kiểm tra login admin
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # # kiểm tra quyền admin role = 1
    # if user.get("role") != 1:
    #     abort(403)

    keyword = request.args.get("keyword", "").strip()
    page = request.args.get("page", 1, type=int)

    query = Brand.query

    if keyword:
        query = query.filter(
            or_(
                cast(Brand.ma_thuong_hieu, String).like(f"%{keyword}%"),
                Brand.ten_thuong_hieu.ilike(f"%{keyword}%")
            )
        )

    pagination = query.order_by(
        Brand.ma_thuong_hieu.desc()
    ).paginate(
        page=page,
        per_page=3,
        error_out=False
    )

    brands = pagination.items
    total_brands = Brand.query.count()

    return render_template(
        "admin/brand.html",
        brands=brands,
        pagination=pagination,
        total_brands=total_brands
    )


@brand_bp.route("/create", methods=["GET", "POST"])
def create_brand():
    # # kiểm tra login admin
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # # kiểm tra quyền admin role = 1
    # if user.get("role") != 1:
    #     abort(403)

    if request.method == "POST":
        brand = Brand(
            ten_thuong_hieu=request.form.get("ten_thuong_hieu"),
            so_dien_thoai=request.form.get("so_dien_thoai"),
            email=request.form.get("email"),
            dia_chi=request.form.get("dia_chi")
        )
        db.session.add(brand)
        db.session.commit()
        return redirect(url_for("brand.show_all_brand"))

    return render_template("admin/brand_create.html")


@brand_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_brand(id):
    # # kiểm tra login admin
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # # kiểm tra quyền admin role = 1
    # if user.get("role") != 1:
    #     abort(403)

    brand = Brand.query.get_or_404(id)

    if request.method == "POST":
        brand.ten_thuong_hieu = request.form.get("ten_thuong_hieu")
        brand.so_dien_thoai = request.form.get("so_dien_thoai")
        brand.email = request.form.get("email")
        brand.dia_chi = request.form.get("dia_chi")

        db.session.commit()
        return redirect(url_for("brand.show_all_brand"))

    return render_template(
        "admin/brand_edit.html",
        brand=brand
    )


@brand_bp.route("/delete/<int:id>", methods=["POST"])
def delete_brand(id):
    # # kiểm tra login admin
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # # kiểm tra quyền admin role = 1
    # if user.get("role") != 1:
    #     abort(403)

    brand = Brand.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    return redirect(url_for("brand.show_all_brand"))

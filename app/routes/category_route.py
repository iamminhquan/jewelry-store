from flask import Blueprint, render_template, request, session, abort, redirect, url_for
from app.models.category import Category
from app.extensions import db
from sqlalchemy import func
from sqlalchemy.types import String
from sqlalchemy import or_, cast

# người chỉnh sửa: Nguyễn Thái Nguyên
# thời gian chỉnh sửa: 17/01/2025
# nội dung: viết các route quản lý danh mục sản phẩm lưu ý xoá mềm, khi nào login bật các comment kiểm tra login và quyền admin

category_bp = Blueprint(
    "category",
    __name__,
    url_prefix="/admin/category"
)

@category_bp.route("/", strict_slashes=False, methods=["GET"])
def show_all_category():
    # #kiem tra login admin 
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # #kiem tra quyen admin role = 1 
    # if user.get("role") != 1:
    #     abort(403)

    keyword = request.args.get("keyword", "").strip()
    status = request.args.get("status") 
    page = request.args.get("page", 1, type=int)

    query = Category.query

    if status == "1":
        query = query.filter(Category.trang_thai == 1)
    elif status == "2":
        query = query.filter(Category.trang_thai == 2)
    elif status == "3":
        query = query.filter(Category.trang_thai == 3)
    else:
        #nút tất cả hiển thị còn hàng hết hàng
        query = query.filter(Category.trang_thai != 3)

    if keyword:
        query = query.filter(
            or_(
                cast(Category.ma_danh_muc, String).like(f"%{keyword}%"),
                Category.ten_danh_muc.ilike(f"%{keyword}%")
            )
        )

    categories = query.all()

    pagination = query.order_by(Category.ma_danh_muc.desc()).paginate(
        page=page,
        per_page=3,
        error_out=False
    )
    categories = pagination.items

    total_categories = Category.query.filter(Category.trang_thai != 3).count()
    con_hang = Category.query.filter_by(trang_thai=1).count()
    het_hang = Category.query.filter_by(trang_thai=2).count()

    danh_muc_noi_bat = Category.query.filter(Category.trang_thai != 3).limit(3).all()
    ten_dm_noi_bat = ", ".join(dm.ten_danh_muc for dm in danh_muc_noi_bat)

    return render_template(
        "admin/category.html",
        categories=categories,
        pagination=pagination,
        total_categories=total_categories,
        con_hang=con_hang,
        het_hang=het_hang,
        ten_dm_noi_bat=ten_dm_noi_bat
    )


@category_bp.route("/delete/<int:id>", methods=["POST"])
def delete_category(id):
    # #kiem tra login admin 
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # #kiem tra quyen admin role = 1 
    # if user.get("role") != 1:
    #     abort(403)

    category = Category.query.get_or_404(id)

    # xoá mềm chuyển trang thái về 3
    category.trang_thai = 3
    db.session.commit()
    return redirect(url_for("category.show_all_category"))

@category_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_category(id):
    # #kiem tra login admin 
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # #kiem tra quyen admin role = 1 
    # if user.get("role") != 1:
    #     abort(403)
    category = Category.query.get_or_404(id)

    if request.method == "POST":
        category.ten_danh_muc = request.form.get("ten_danh_muc")
        category.mo_ta = request.form.get("mo_ta")

        new_status = int(request.form.get("trang_thai"))

        # xoá mềm / khôi phục / cập nhật trạng thái
        if new_status == 3:
            category.trang_thai = 3
        else:
            category.trang_thai = new_status

        db.session.commit()
        return redirect(url_for("category.show_all_category"))

    return render_template(
        "admin/category_edit.html",
        category=category
    )


@category_bp.route("/create", methods=["GET", "POST"])
def create_category():
        # #kiem tra login admin 
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # #kiem tra quyen admin role = 1 
    # if user.get("role") != 1:
    #     abort(403)
    if request.method == "POST":
        ten_danh_muc = request.form.get("ten_danh_muc")
        mo_ta = request.form.get("mo_ta")
        trang_thai = int(request.form.get("trang_thai"))

        category = Category(
            ten_danh_muc=ten_danh_muc,
            mo_ta=mo_ta,
            trang_thai=trang_thai
        )

        db.session.add(category)
        db.session.commit()

        return redirect(url_for("category.show_all_category"))

    return render_template("admin/category_create.html")


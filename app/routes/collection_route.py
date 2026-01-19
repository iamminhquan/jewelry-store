from flask import Blueprint, render_template, request, redirect, url_for
from app.models.collection import Collection
from app.extensions import db
from sqlalchemy import or_, cast
from sqlalchemy.types import String

# người chỉnh sửa: Nguyễn Thái Nguyên
# thời gian chỉnh sửa: 17/01/2025
# nội dung: viết các route quản lý bộ sưu tập sản phẩm lưu ý xoá mềm, khi nào login bật các comment kiểm tra login và quyền admin
collection_bp = Blueprint(
    "collection",
    __name__,
    url_prefix="/admin/collection"
)


@collection_bp.route("/", strict_slashes=False)
def show_all_collection():
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

    query = Collection.query

    if status == "1":
        query = query.filter(Collection.trang_thai == 1)
    elif status == "2":
        query = query.filter(Collection.trang_thai == 2)
    elif status == "3":
        query = query.filter(Collection.trang_thai == 3)
    else:
        query = query.filter(Collection.trang_thai != 3)

    if keyword:
        query = query.filter(
            or_(
                cast(Collection.ma_bo_suu_tap, String).like(f"%{keyword}%"),
                Collection.ten_bo_suu_tap.ilike(f"%{keyword}%")
            )
        )

    pagination = query.order_by(
        Collection.ma_bo_suu_tap.desc()
    ).paginate(
        page=page,
        per_page=3,
        error_out=False
    )

    collections = pagination.items

    total_collections = Collection.query.filter(
        Collection.trang_thai != 3
    ).count()

    con_hang = Collection.query.filter_by(trang_thai=1).count()
    het_hang = Collection.query.filter_by(trang_thai=2).count()

    noi_bat = Collection.query.filter(
        Collection.trang_thai != 3
    ).limit(3).all()

    ten_noi_bat = ", ".join(c.ten_bo_suu_tap for c in noi_bat)

    return render_template(
        "admin/collection.html",
        collections=collections,
        pagination=pagination,
        total_collections=total_collections,
        con_hang=con_hang,
        het_hang=het_hang,
        ten_noi_bat=ten_noi_bat
    )


@collection_bp.route("/create", methods=["GET", "POST"])
def create_collection():
        # #kiem tra login admin 
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # #kiem tra quyen admin role = 1 
    # if user.get("role") != 1:
    #     abort(403)

    if request.method == "POST":
        collection = Collection(
            ten_bo_suu_tap=request.form.get("ten_bo_suu_tap"),
            mo_ta=request.form.get("mo_ta"),
            trang_thai=int(request.form.get("trang_thai"))
        )
        db.session.add(collection)
        db.session.commit()
        return redirect(url_for("collection.show_all_collection"))

    return render_template("admin/collection_create.html")


@collection_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_collection(id):
        # #kiem tra login admin 
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # #kiem tra quyen admin role = 1 
    # if user.get("role") != 1:
    #     abort(403)

    collection = Collection.query.get_or_404(id)

    if request.method == "POST":
        collection.ten_bo_suu_tap = request.form.get("ten_bo_suu_tap")
        collection.mo_ta = request.form.get("mo_ta")
        collection.trang_thai = int(request.form.get("trang_thai"))

        db.session.commit()
        return redirect(url_for("collection.show_all_collection"))

    return render_template(
        "admin/collection_edit.html",
        collection=collection
    )


@collection_bp.route("/delete/<int:id>", methods=["POST"])
def delete_collection(id):
        # #kiem tra login admin 
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # #kiem tra quyen admin role = 1 
    # if user.get("role") != 1:
    #     abort(403)
    collection = Collection.query.get_or_404(id)
    collection.trang_thai = 3
    db.session.commit()
    return redirect(url_for("collection.show_all_collection"))

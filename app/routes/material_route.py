from flask import Blueprint, render_template, request, redirect, url_for
from app.models.material import Material as ChatLieu
from app.extensions import db
from sqlalchemy import or_, cast
from sqlalchemy.types import String

# editor: Nguyễn Thái Nguyên
# edited date: 17/01/2025
# nội dung: viết các route quản lý chất liệu sản phẩm lưu ý xoá mềm, khi nào login bật các comment kiểm tra login và quyền admin
material_bp = Blueprint(
    "material",
    __name__,
    url_prefix="/admin/material"
)


@material_bp.route("/", strict_slashes=False)
def show_all_material():
        # # check admin login
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # # check admin role = 1
    # if user.get("role") != 1:
    #     abort(403)

    keyword = request.args.get("keyword", "").strip()
    page = request.args.get("page", 1, type=int)

    query = ChatLieu.query

    if keyword:
        query = query.filter(
            or_(
                cast(ChatLieu.ma_chat_lieu, String).like(f"%{keyword}%"),
                ChatLieu.ten_chat_lieu.ilike(f"%{keyword}%")
            )
        )

    pagination = query.order_by(
        ChatLieu.ma_chat_lieu.desc()
    ).paginate(
        page=page,
        per_page=3,
        error_out=False
    )

    materials = pagination.items

    total_materials = ChatLieu.query.count()

    return render_template(
        "admin/material.html",
        materials=materials,
        pagination=pagination,
        total_materials=total_materials
    )


@material_bp.route("/create", methods=["GET", "POST"])
def create_material():
        # # check admin login
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # # check admin role = 1
    # if user.get("role") != 1:
    #     abort(403)

    if request.method == "POST":
        material = ChatLieu(
            ten_chat_lieu=request.form.get("ten_chat_lieu")
        )
        db.session.add(material)
        db.session.commit()
        return redirect(url_for("material.show_all_material"))

    return render_template("admin/material_create.html")


@material_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_material(id):
        # # check admin login
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # # check admin role = 1
    # if user.get("role") != 1:
    #     abort(403)

    material = ChatLieu.query.get_or_404(id)

    if request.method == "POST":
        material.ten_chat_lieu = request.form.get("ten_chat_lieu")
        db.session.commit()
        return redirect(url_for("material.show_all_material"))

    return render_template(
        "admin/material_edit.html",
        material=material
    )


@material_bp.route("/delete/<int:id>", methods=["POST"])
def delete_material(id):
        # # check admin login
    # user = session.get("user")
    # if not user:
    #     abort(401)

    # # check admin role = 1
    # if user.get("role") != 1:
    #     abort(403)

    material = ChatLieu.query.get_or_404(id)
    db.session.delete(material)
    db.session.commit()
    return redirect(url_for("material.show_all_material"))

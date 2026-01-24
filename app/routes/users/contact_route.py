from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from app.extensions import db
from app.models.contact import Contact

contact_bp = Blueprint(
    "contact",
    __name__,
    url_prefix="/",
)


@contact_bp.route("/contact", methods=["GET", "POST"])
def show_contact_page():
    if request.method == "POST":
        ten_khach_hang = request.form.get("ten_khach_hang")
        email = request.form.get("email")
        so_dien_thoai = request.form.get("so_dien_thoai")
        noi_dung = request.form.get("noi_dung")

        if not ten_khach_hang or not email or not so_dien_thoai or not noi_dung:
            flash("Vui lòng nhập đầy đủ thông tin!", "error")
            return redirect(url_for("user.show_contact_page"))

        ma_tai_khoan = (
            current_user.ma_tai_khoan if current_user.is_authenticated else None
        )

        lien_he = Contact(
            customer_name=ten_khach_hang,
            email=email,
            phone=so_dien_thoai,
            content=noi_dung,
            account_id=ma_tai_khoan,
        )

        db.session.add(lien_he)
        db.session.commit()

        flash("Gửi liên hệ thành công!", "success")
        return redirect(url_for("contact.show_contact_page"))

    return render_template("user/contact.html")

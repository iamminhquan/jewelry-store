from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models.order_detail import OrderDetail as DonHang

admin_order_detail = Blueprint(
    "admin_order_detail", __name__, url_prefix="/admin/orders"
)

@admin_order_detail.route("/<int:id>")
def view(id):
    order = DonHang.query.get_or_404(id)
    return render_template("admin/order_detail.html", order=order)

@admin_order_detail.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    order = DonHang.query.get_or_404(id)

    if request.method == "POST":
        order.trang_thai = request.form["trang_thai"]
        db.session.commit()
        return redirect(url_for("admin_order.index"))

    return render_template("admin/order_edit.html", order=order)

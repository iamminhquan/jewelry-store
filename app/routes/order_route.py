from flask import Blueprint, render_template, request, redirect, url_for, send_file, session
from app.extensions import db
from app.models.order import Order as DonHang
from app.models.order_detail import OrderDetail
from app.models.product import Product
from datetime import datetime
import io

admin_order = Blueprint("admin_order", __name__, url_prefix="/admin/orders")

#hiển thị danh sách đơn hàng
@admin_order.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    keyword = request.args.get("keyword")

    query = DonHang.query.filter(DonHang.trang_thai != 0)
    if keyword:
        query = query.filter(DonHang.ma_don_hang.like(f"%{keyword}%"))
    pagination = query.order_by(DonHang.ngay_tao.desc()) \
                      .paginate(page=page, per_page=3)
    return render_template("admin/orders.html", pagination=pagination)


#them đơn hàng
@admin_order.route("/create", methods=["GET", "POST"])
def create():
    # Khởi tạo giỏ hàng tạm
    if "order_items" not in session:
        session["order_items"] = []

    if request.method == "POST" and "add_product" in request.form:
        ma_tai_khoan = request.form["ma_tai_khoan"]
        ma_san_pham = int(request.form["ma_san_pham"])
        so_luong = int(request.form["so_luong"])
        ngay_dat_hang = request.form["ngay_dat_hang"]
        trang_thai = int(request.form["trang_thai"])

        product = Product.query.get(ma_san_pham)
        if not product:
            return redirect(url_for("admin_order.create"))

        don_gia = float(product.gia_xuat)
        thanh_tien = don_gia * so_luong

        session["order_items"].append({
            "ma_don_hang": "Tự động",
            "ma_tai_khoan": ma_tai_khoan,
            "ma_san_pham": ma_san_pham,
            "so_luong": so_luong,
            "don_gia": don_gia,
            "thanh_tien": thanh_tien,
            "ngay_dat_hang": ngay_dat_hang,
            "trang_thai": trang_thai
        })

        session.modified = True
        return redirect(url_for("admin_order.create"))

    if request.method == "POST" and "create_order" in request.form:
        if not session["order_items"]:
            return redirect(url_for("admin_order.create"))

        tong_tien = sum(i["thanh_tien"] for i in session["order_items"])

        order = DonHang(
            ma_tai_khoan=session["order_items"][0]["ma_tai_khoan"],
            tong_tien_tam_tinh=tong_tien,
            ngay_tao=datetime.utcnow(),
            ngay_dat_hang=session["order_items"][0]["ngay_dat_hang"],
            trang_thai=session["order_items"][0]["trang_thai"]
        )
        db.session.add(order)
        db.session.commit()

        for i in session["order_items"]:
            detail = OrderDetail(
                ma_don_hang=order.ma_don_hang,
                ma_san_pham=i["ma_san_pham"],
                so_luong=i["so_luong"],
                don_gia=i["don_gia"],
                thanh_tien=i["thanh_tien"],
                ngay_tao=datetime.utcnow()
            )
            db.session.add(detail)

        db.session.commit()
        session.pop("order_items")

        return redirect(url_for("admin_order.index"))

    tong_tien = sum(i["thanh_tien"] for i in session["order_items"])

    return render_template(
        "admin/order_create.html",
        products=session["order_items"],
        tong_tien=tong_tien
    )

# xoá đơn hàng
@admin_order.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    order = DonHang.query.get_or_404(id)
    order.trang_thai = 0
    db.session.commit()
    return redirect(url_for("admin_order.index"))

# xuất pdf hoặc excel
@admin_order.route("/export")
def export():
    export_type = request.args.get("type")

    if export_type == "pdf":
        return send_file(
            io.BytesIO(b"PDF DATA"),
            mimetype="application/pdf",
            download_name="orders.pdf"
        )

    if export_type == "excel":
        return send_file(
            io.BytesIO(b"EXCEL DATA"),
            download_name="orders.xlsx"
        )

    return redirect(url_for("admin_order.index"))

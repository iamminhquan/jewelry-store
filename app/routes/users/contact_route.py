from flask import Blueprint, render_template


user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/user/",
)


@user_bp.route("/contact")
def show_contact_page():
    return render_template("user/contact.html")

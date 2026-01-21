from flask import Blueprint, render_template

account_bp = Blueprint(
    'account',
    __name__,
    url_prefix='/account',
)


@account_bp.route("/", methods=["GET"])
def show_account_page():
    return render_template('admin/account/account.html')

from flask import Flask

from app.config import Config
from app.extensions import db
from app.extensions import login_manager
from app.extensions import migrate


def create_app():
    """Khởi tạo một ứng dụng Flask

    Returns:
        Flask: Trả về một đối tượng Flask.
    """
    # Khởi tạo Flask app.
    app = Flask(__name__, template_folder="templates")

    # Tải cấu hình từ đối tượng Config.
    app.config.from_object(Config)

    # Kết nối đến Cơ sở dữ liệu.
    db.init_app(app)

    # Manage migration.
    migrate.init_app(app, db)

    # Manage login/session.
    login_manager.init_app(app)
    login_manager.login_view = "auth.show_sign_in_page"

    # Import các Blueprint vào Factory function.
    from app.routes.main_route import main_bp
    from app.routes.admin.product_route import product_bp
    from app.routes.admin.category_route import category_bp
    from app.routes.admin.material_route import material_bp
    from app.routes.admin.brand_route import brand_bp
    from app.routes.admin.collection_route import collection_bp
    from app.routes.admin.product_type_route import product_type_bp
    from app.routes.admin.order_route import order_bp
    from app.routes.admin.invoice_route import invoice_bp
    from app.routes.admin.report_route import report_bp
    from app.routes.admin.comment_route import comment_bp
    from app.routes.auth_route import auth_bp
    from app.routes.admin.admin_route import admin_route

    # Đăng ký các Blueprint bên trên.
    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(material_bp)
    app.register_blueprint(brand_bp)
    app.register_blueprint(collection_bp)
    app.register_blueprint(product_type_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_route)

    return app

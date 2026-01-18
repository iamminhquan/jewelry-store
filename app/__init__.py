from flask import Flask
from app.config import Config
from app.extensions import db


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

    # Import các Blueprint vào Factory function.
    from app.routes.main_route import main_bp
    from app.routes.product_route import product_bp
    from app.routes.auth_route import auth_bp

    # Đăng ký các Blueprint bên trên.
    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(auth_bp)

    return app

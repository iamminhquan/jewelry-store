from flask import Flask
import os


def create_app():
    """Factory function để tạo Flask app"""
    app = Flask(__name__)

    # Cấu hình
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"
    )
    app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", "True") == "True"

    # Đăng ký blueprints
    from app.routes.main import main_bp

    app.register_blueprint(main_bp)

    return app

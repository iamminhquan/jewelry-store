from flask import Blueprint, render_template

from app.services.material_service import get_all_materials


material_bp = Blueprint(
    "material",
    __name__,
    url_prefix="/materials",
)


@material_bp.route("/", methods=["GET"])
def show_all_materials():
    materials = get_all_materials()

    return render_template(
        "product/material.html",
        materials=materials,
    )

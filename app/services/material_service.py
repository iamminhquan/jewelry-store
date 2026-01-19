from app.models.material import Material


def get_all_materials():
    return Material.query.all()

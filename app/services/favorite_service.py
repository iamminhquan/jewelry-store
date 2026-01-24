"""
Module service quản lý sản phẩm yêu thích.

Module này cung cấp logic nghiệp vụ cho các thao tác sản phẩm yêu thích của người dùng.
"""

from typing import Optional
from app.extensions import db
from app.models.favorite import Favorite
from app.models.product import Product


def get_user_favorites(user_id: int) -> list[dict]:
    """Lấy danh sách sản phẩm yêu thích của người dùng.

    Args:
        user_id (int): Mã tài khoản người dùng.

    Returns:
        list[dict]: Danh sách dict chứa thông tin sản phẩm yêu thích.
    """
    favorites = Favorite.query.filter_by(ma_tai_khoan=user_id).all()

    result = []
    for fav in favorites:
        product = Product.query.get(fav.ma_san_pham)
        if product:
            # Lấy ảnh đầu tiên nếu có
            image_url = None
            if product.hinh_anhs:
                # Ưu tiên ảnh chính
                main_imgs = [img for img in product.hinh_anhs if img.anh_chinh == 1]
                if main_imgs:
                    image_url = main_imgs[0].duong_dan
                else:
                    image_url = product.hinh_anhs[0].duong_dan

            result.append(
                {
                    "favorite_id": fav.ma_yeu_thich,
                    "product": product,
                    "image": image_url,
                    "ngay_tao": fav.ngay_tao,
                }
            )

    return result


def get_user_favorite_ids(user_id: int) -> list[int]:
    """Lấy danh sách ID sản phẩm yêu thích của người dùng.

    Args:
        user_id (int): Mã tài khoản người dùng.

    Returns:
        list[int]: Danh sách mã sản phẩm đã yêu thích.
    """
    favorites = Favorite.query.filter_by(ma_tai_khoan=user_id).all()
    return [fav.ma_san_pham for fav in favorites]


def is_product_favorited(user_id: int, product_id: int) -> bool:
    """Kiểm tra sản phẩm đã được yêu thích chưa.

    Args:
        user_id (int): Mã tài khoản người dùng.
        product_id (int): Mã sản phẩm.

    Returns:
        bool: True nếu đã yêu thích, False nếu chưa.
    """
    favorite = Favorite.query.filter_by(
        ma_tai_khoan=user_id, ma_san_pham=product_id
    ).first()
    return favorite is not None


def add_to_favorites(user_id: int, product_id: int) -> Optional[Favorite]:
    """Thêm sản phẩm vào danh sách yêu thích.

    Args:
        user_id (int): Mã tài khoản người dùng.
        product_id (int): Mã sản phẩm.

    Returns:
        Favorite: Đối tượng Favorite nếu thêm thành công, None nếu đã tồn tại.
    """
    # Kiểm tra đã yêu thích chưa
    if is_product_favorited(user_id, product_id):
        return None

    favorite = Favorite(user_id=user_id, product_id=product_id)
    db.session.add(favorite)
    db.session.commit()
    return favorite


def remove_from_favorites(user_id: int, product_id: int) -> bool:
    """Xóa sản phẩm khỏi danh sách yêu thích.

    Args:
        user_id (int): Mã tài khoản người dùng.
        product_id (int): Mã sản phẩm.

    Returns:
        bool: True nếu xóa thành công, False nếu không tìm thấy.
    """
    favorite = Favorite.query.filter_by(
        ma_tai_khoan=user_id, ma_san_pham=product_id
    ).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return True
    return False


def toggle_favorite(user_id: int, product_id: int) -> dict:
    """Toggle trạng thái yêu thích của sản phẩm.

    Args:
        user_id (int): Mã tài khoản người dùng.
        product_id (int): Mã sản phẩm.

    Returns:
        dict: {"action": "added" | "removed", "is_favorited": bool}
    """
    if is_product_favorited(user_id, product_id):
        remove_from_favorites(user_id, product_id)
        return {"action": "removed", "is_favorited": False}
    else:
        add_to_favorites(user_id, product_id)
        return {"action": "added", "is_favorited": True}

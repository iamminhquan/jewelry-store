from app.extensions import db
from app.models.collection import Collection
from sqlalchemy import or_, cast
from sqlalchemy.types import String


def build_collection_query(keyword: str, status: str):
    """Tạo truy vấn bộ sưu tập theo từ khoá và trạng thái.

    Args:
        keyword (str): Từ khoá tìm kiếm.
        status (str): Trạng thái lọc (1, 2, 3 hoặc None).

    Returns:
        BaseQuery: Truy vấn bộ sưu tập đã áp dụng điều kiện lọc.
    """
    query = Collection.query

    if status == "1":
        query = query.filter(Collection.trang_thai == 1)
    elif status == "2":
        query = query.filter(Collection.trang_thai == 2)
    elif status == "3":
        query = query.filter(Collection.trang_thai == 3)
    else:
        query = query.filter(Collection.trang_thai != 3)

    if keyword:
        query = query.filter(
            or_(
                cast(Collection.ma_bo_suu_tap, String).like(f"%{keyword}%"),
                Collection.ten_bo_suu_tap.ilike(f"%{keyword}%"),
            )
        )

    return query


def get_collection_page(keyword: str, status: str, page: int, per_page: int = 3):
    """Lấy dữ liệu bộ sưu tập theo trang kèm thống kê.

    Args:
        keyword (str): Từ khoá tìm kiếm.
        status (str): Trạng thái lọc (1, 2, 3 hoặc None).
        page (int): Trang hiện tại.
        per_page (int, optional): Số bản ghi mỗi trang. Defaults to 3.

    Returns:
        tuple: (pagination, collections, total_collections, con_hang, het_hang,
        ten_bst_noi_bat)
    """
    query = build_collection_query(keyword, status)

    pagination = db.paginate(
        query.order_by(Collection.ma_bo_suu_tap.desc()),
        page=page,
        per_page=per_page,
        error_out=False,
    )

    total_collections = Collection.query.filter(Collection.trang_thai != 3).count()
    con_hang = Collection.query.filter_by(trang_thai=1).count()
    het_hang = Collection.query.filter_by(trang_thai=2).count()

    bo_suu_tap_noi_bat = (
        Collection.query.filter(Collection.trang_thai != 3).limit(3).all()
    )
    ten_bst_noi_bat = ", ".join(bst.ten_bo_suu_tap for bst in bo_suu_tap_noi_bat)

    return (
        pagination,
        pagination.items,
        total_collections,
        con_hang,
        het_hang,
        ten_bst_noi_bat,
    )


def get_collection_or_404(collection_id: int):
    """Lấy bộ sưu tập theo id hoặc trả về 404.

    Args:
        collection_id (int): Mã bộ sưu tập.

    Returns:
        Collection: Bộ sưu tập tìm thấy.
    """
    return Collection.query.get_or_404(collection_id)


def create_collection(ten_bo_suu_tap: str, mo_ta: str, trang_thai: int):
    """Tạo mới bộ sưu tập và lưu vào cơ sở dữ liệu.

    Args:
        ten_bo_suu_tap (str): Tên bộ sưu tập.
        mo_ta (str): Mô tả bộ sưu tập.
        trang_thai (int): Trạng thái bộ sưu tập.

    Returns:
        Collection: Bộ sưu tập vừa tạo.
    """
    collection = Collection(
        collection_name=ten_bo_suu_tap,
        collection_description=mo_ta,
        status=trang_thai,
    )
    db.session.add(collection)
    db.session.commit()
    return collection


def update_collection(
    collection: Collection, ten_bo_suu_tap: str, mo_ta: str, new_status: int
):
    """Cập nhật thông tin bộ sưu tập và lưu thay đổi.

    Args:
        collection (Collection): Bộ sưu tập cần cập nhật.
        ten_bo_suu_tap (str): Tên bộ sưu tập mới.
        mo_ta (str): Mô tả mới.
        new_status (int): Trạng thái mới.

    Returns:
        Collection: Bộ sưu tập sau khi cập nhật.
    """
    collection.ten_bo_suu_tap = ten_bo_suu_tap
    collection.mo_ta = mo_ta
    collection.trang_thai = 3 if new_status == 3 else new_status
    db.session.commit()
    return collection


def soft_delete_collection(collection: Collection):
    """Xoá mềm bộ sưu tập bằng cách đặt trạng thái đã xoá.

    Args:
        collection (Collection): Bộ sưu tập cần xoá.
    """
    collection.trang_thai = 3
    db.session.commit()

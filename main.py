from pathlib import Path
import sys

from pupdb.core import PupDB


# Giúp terminal/cmd Windows hiển thị tiếng Việt có dấu tốt hơn.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# File JSON dùng để PupDB lưu trữ dữ liệu sinh viên.
DB_FILE = Path(__file__).with_name("students.json")
db = PupDB(str(DB_FILE))


def hien_thi_menu():
    """In menu chức năng ra màn hình."""
    print("\n" + "=" * 50)
    print(" HỆ THỐNG QUẢN LÝ SINH VIÊN SỬ DỤNG PUPDB")
    print("=" * 50)
    print("1. Thêm sinh viên")
    print("2. Xem sinh viên theo mã sinh viên")
    print("3. Cập nhật thông tin sinh viên")
    print("4. Xóa sinh viên")
    print("5. Liệt kê toàn bộ sinh viên")
    print("6. Xóa toàn bộ dữ liệu")
    print("0. Thoát chương trình")
    print("=" * 50)


def nhap_khong_de_trong(thong_bao):
    """Yêu cầu người dùng nhập dữ liệu bắt buộc."""
    while True:
        gia_tri = input(thong_bao).strip()
        if gia_tri:
            return gia_tri
        print("Lỗi: Không được để trống thông tin này.")


def nhap_gpa(thong_bao="Nhap GPA: ", cho_phep_bo_qua=False):
    """Nhập GPA và kiểm tra GPA phải là số."""
    while True:
        gia_tri = input(thong_bao).strip()

        if cho_phep_bo_qua and gia_tri == "":
            return None

        try:
            return float(gia_tri)
        except ValueError:
            print("Lỗi: GPA phải là số. Ví dụ: 3.2")


def in_thong_tin_sinh_vien(ma_sinh_vien, sinh_vien):
    """Hiển thị một sinh viên theo định dạng dễ đọc."""
    print("-" * 50)
    print(f"Mã sinh viên : {ma_sinh_vien}")
    print(f"Họ tên       : {sinh_vien['ho_ten']}")
    print(f"Lớp          : {sinh_vien['lop']}")
    print(f"GPA          : {sinh_vien['gpa']}")
    print("-" * 50)


def them_sinh_vien():
    """Thêm sinh viên mới vào PupDB."""
    print("\n--- THÊM SINH VIÊN ---")
    ma_sinh_vien = nhap_khong_de_trong("Nhập mã sinh viên: ")

    if db.get(ma_sinh_vien) is not None:
        print("Lỗi: Mã sinh viên đã tồn tại, không thể thêm trùng.")
        return

    ho_ten = nhap_khong_de_trong("Nhập họ tên: ")
    lop = nhap_khong_de_trong("Nhập lớp: ")
    gpa = nhap_gpa("Nhập GPA: ")

    # Mã sinh viên được dùng làm key, thông tin còn lại là value.
    sinh_vien = {
        "ho_ten": ho_ten,
        "lop": lop,
        "gpa": gpa,
    }

    db.set(ma_sinh_vien, sinh_vien)
    print("Thêm sinh viên thành công.")


def xem_sinh_vien():
    """Tìm và hiển thị sinh viên theo mã sinh viên."""
    print("\n--- XEM SINH VIÊN ---")
    ma_sinh_vien = nhap_khong_de_trong("Nhập mã sinh viên cần xem: ")
    sinh_vien = db.get(ma_sinh_vien)

    if sinh_vien is None:
        print("Lỗi: Không tìm thấy sinh viên.")
        return

    in_thong_tin_sinh_vien(ma_sinh_vien, sinh_vien)


def cap_nhat_sinh_vien():
    """Cập nhật thông tin sinh viên đã có trong PupDB."""
    print("\n--- CẬP NHẬT SINH VIÊN ---")
    ma_sinh_vien = nhap_khong_de_trong("Nhập mã sinh viên cần cập nhật: ")
    sinh_vien = db.get(ma_sinh_vien)

    if sinh_vien is None:
        print("Lỗi: Không tìm thấy sinh viên.")
        return

    print("Nhập thông tin mới. Bấm Enter để giữ nguyên giá trị cũ.")
    ho_ten_moi = input(f"Họ tên ({sinh_vien['ho_ten']}): ").strip()
    lop_moi = input(f"Lớp ({sinh_vien['lop']}): ").strip()
    gpa_moi = nhap_gpa(f"GPA ({sinh_vien['gpa']}): ", cho_phep_bo_qua=True)

    if ho_ten_moi:
        sinh_vien["ho_ten"] = ho_ten_moi
    if lop_moi:
        sinh_vien["lop"] = lop_moi
    if gpa_moi is not None:
        sinh_vien["gpa"] = gpa_moi

    db.set(ma_sinh_vien, sinh_vien)
    print("Cập nhật sinh viên thành công.")


def xoa_sinh_vien():
    """Xóa một sinh viên theo mã sinh viên."""
    print("\n--- XÓA SINH VIÊN ---")
    ma_sinh_vien = nhap_khong_de_trong("Nhập mã sinh viên cần xóa: ")

    if db.get(ma_sinh_vien) is None:
        print("Lỗi: Không tìm thấy sinh viên.")
        return

    xac_nhan = input("Bạn có chắc chắn muốn xóa? (y/n): ").strip().lower()
    if xac_nhan == "y":
        db.remove(ma_sinh_vien)
        print("Xóa sinh viên thành công.")
    else:
        print("Đã hủy thao tác xóa.")


def liet_ke_sinh_vien():
    """Liệt kê tất cả sinh viên đang có trong database."""
    print("\n--- DANH SÁCH SINH VIÊN ---")
    danh_sach = sorted(list(db.items()), key=lambda item: item[0])

    if not danh_sach:
        print("Chưa có sinh viên nào trong hệ thống.")
        return

    for ma_sinh_vien, sinh_vien in danh_sach:
        in_thong_tin_sinh_vien(ma_sinh_vien, sinh_vien)


def xoa_toan_bo_du_lieu():
    """Xóa tất cả dữ liệu trong file students.json."""
    print("\n--- XÓA TOÀN BỘ DỮ LIỆU ---")
    xac_nhan = input("Nhập 'YES' để xóa toàn bộ dữ liệu: ").strip()

    if xac_nhan == "YES":
        db.truncate_db()
        print("Đã xóa toàn bộ dữ liệu.")
    else:
        print("Đã hủy thao tác xóa toàn bộ dữ liệu.")


def main():
    """Hàm chính điều khiển chương trình."""
    while True:
        hien_thi_menu()
        lua_chon = input("Nhập lựa chọn của bạn: ").strip()

        if lua_chon == "1":
            them_sinh_vien()
        elif lua_chon == "2":
            xem_sinh_vien()
        elif lua_chon == "3":
            cap_nhat_sinh_vien()
        elif lua_chon == "4":
            xoa_sinh_vien()
        elif lua_chon == "5":
            liet_ke_sinh_vien()
        elif lua_chon == "6":
            xoa_toan_bo_du_lieu()
        elif lua_chon == "0":
            print("Cảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
            break
        else:
            print("Lỗi: Lựa chọn không hợp lệ, vui lòng chọn lại.")


if __name__ == "__main__":
    main()

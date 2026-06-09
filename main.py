import sys
import requests
import random

# Giúp terminal/cmd Windows hiển thị tiếng Việt có dấu tốt hơn.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

COORDINATOR_URL = "http://127.0.0.1:5050"

def hien_thi_menu():
    """In menu chức năng ra màn hình."""
    print("\n" + "=" * 60)
    print(" HỆ THỐNG QUẢN LÝ SINH VIÊN PHÂN TÁN PUPDB - NHÓM 21")
    print("=" * 60)
    print("1. Thêm sinh viên")
    print("2. Xem sinh viên theo mã sinh viên")
    print("3. Cập nhật thông tin sinh viên")
    print("4. Xóa sinh viên")
    print("5. Liệt kê toàn bộ sinh viên (Distributed Query)")
    print("6. Hiển thị trạng thái các shard")
    print("7. Kiểm tra replication")
    print("8. Giả lập lỗi shard chính")
    print("9. Kiểm tra failover")
    print("10. Tạo dữ liệu mẫu để test mở rộng")
    print("11. Thoát")
    print("=" * 60)


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


def in_thong_tin_sinh_vien(ma_sinh_vien, sinh_vien, used_replica=False):
    """Hiển thị một sinh viên theo định dạng dễ đọc."""
    print("-" * 50)
    print(f"Mã sinh viên : {ma_sinh_vien}")
    print(f"Họ tên       : {sinh_vien['ho_ten']}")
    print(f"Lớp          : {sinh_vien['lop']}")
    print(f"GPA          : {sinh_vien['gpa']}")
    if used_replica:
         print(f"TRẠNG THÁI   : LẤY TỪ REPLICA (FAILOVER THÀNH CÔNG)")
    print("-" * 50)


def them_sinh_vien():
    """Thêm sinh viên mới (Gửi POST request tới Coordinator)."""
    print("\n--- THÊM SINH VIÊN ---")
    ma_sinh_vien = nhap_khong_de_trong("Nhập mã sinh viên: ")

    # Kiểm tra xem mã sinh viên đã tồn tại chưa
    try:
        r = requests.get(f"{COORDINATOR_URL}/get/{ma_sinh_vien}")
        if r.status_code == 200:
            print("Lỗi: Mã sinh viên đã tồn tại, không thể thêm trùng.")
            return
    except requests.exceptions.RequestException:
        print("Lỗi: Không thể kết nối đến Coordinator.")
        return

    ho_ten = nhap_khong_de_trong("Nhập họ tên: ")
    lop = nhap_khong_de_trong("Nhập lớp: ")
    gpa = nhap_gpa("Nhập GPA: ")

    data = {
        "student_id": ma_sinh_vien,
        "ho_ten": ho_ten,
        "lop": lop,
        "gpa": gpa,
    }

    try:
        response = requests.post(f"{COORDINATOR_URL}/set", json=data)
        if response.status_code == 200:
            res_data = response.json()
            print(f"Thêm sinh viên thành công. Đã định tuyến đến: {res_data['target_node']}")
        else:
            print("Lỗi khi thêm sinh viên.")
    except requests.exceptions.RequestException:
         print("Lỗi: Không thể kết nối đến Coordinator.")

def xem_sinh_vien():
    """Tìm và hiển thị sinh viên theo mã (GET request tới Coordinator)."""
    print("\n--- XEM SINH VIÊN ---")
    ma_sinh_vien = nhap_khong_de_trong("Nhập mã sinh viên cần xem: ")
    
    try:
        response = requests.get(f"{COORDINATOR_URL}/get/{ma_sinh_vien}")
        if response.status_code == 200:
            data = response.json()
            student = data['response']['student']
            used_replica = data['response'].get('used_replica', False)
            print(f"Lấy dữ liệu từ Node: {data['target_node']}")
            in_thong_tin_sinh_vien(ma_sinh_vien, student, used_replica)
        else:
            print("Lỗi: Không tìm thấy sinh viên.")
    except requests.exceptions.RequestException:
         print("Lỗi: Không thể kết nối đến Coordinator.")

def cap_nhat_sinh_vien():
    """Cập nhật thông tin sinh viên."""
    print("\n--- CẬP NHẬT SINH VIÊN ---")
    ma_sinh_vien = nhap_khong_de_trong("Nhập mã sinh viên cần cập nhật: ")
    
    try:
        r = requests.get(f"{COORDINATOR_URL}/get/{ma_sinh_vien}")
        if r.status_code != 200:
             print("Lỗi: Không tìm thấy sinh viên.")
             return
             
        data = r.json()
        sinh_vien = data['response']['student']
    except requests.exceptions.RequestException:
         print("Lỗi: Không thể kết nối đến Coordinator.")
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

    sinh_vien["student_id"] = ma_sinh_vien

    try:
        response = requests.post(f"{COORDINATOR_URL}/set", json=sinh_vien)
        if response.status_code == 200:
            print("Cập nhật sinh viên thành công.")
        else:
            print("Lỗi cập nhật sinh viên.")
    except requests.exceptions.RequestException:
         print("Lỗi: Không thể kết nối đến Coordinator.")

def xoa_sinh_vien():
    """Xóa một sinh viên theo mã sinh viên."""
    print("\n--- XÓA SINH VIÊN ---")
    ma_sinh_vien = nhap_khong_de_trong("Nhập mã sinh viên cần xóa: ")

    try:
        r = requests.get(f"{COORDINATOR_URL}/get/{ma_sinh_vien}")
        if r.status_code != 200:
             print("Lỗi: Không tìm thấy sinh viên.")
             return
    except requests.exceptions.RequestException:
         print("Lỗi: Không thể kết nối đến Coordinator.")
         return

    xac_nhan = input("Bạn có chắc chắn muốn xóa? (y/n): ").strip().lower()
    if xac_nhan == "y":
        try:
            response = requests.delete(f"{COORDINATOR_URL}/delete/{ma_sinh_vien}")
            if response.status_code == 200:
                print("Xóa sinh viên thành công.")
            else:
                 print("Lỗi khi xóa sinh viên.")
        except requests.exceptions.RequestException:
            print("Lỗi: Không thể kết nối đến Coordinator.")
    else:
        print("Đã hủy thao tác xóa.")

def liet_ke_sinh_vien():
    """Liệt kê tất cả sinh viên từ tất cả các shard (Distributed Query)."""
    print("\n--- DANH SÁCH TOÀN BỘ SINH VIÊN (DISTRIBUTED QUERY) ---")
    try:
        response = requests.get(f"{COORDINATOR_URL}/all")
        if response.status_code == 200:
            res_data = response.json()
            nodes_data = res_data["data"]
            
            all_students = []
            for node_url, node_info in nodes_data.items():
                if "error" not in node_info:
                    for sid, sdata in node_info.get("data", {}).items():
                        all_students.append((sid, sdata, node_info.get("used_replica", False)))
                        
            all_students.sort(key=lambda x: x[0])
            
            if not all_students:
                 print("Chưa có sinh viên nào trong hệ thống.")
                 return
                 
            for sid, sdata, used_replica in all_students:
                in_thong_tin_sinh_vien(sid, sdata, used_replica)
            
            print(f"Tổng số sinh viên: {len(all_students)}")
        else:
            print("Lỗi lấy danh sách sinh viên.")
    except requests.exceptions.RequestException:
         print("Lỗi: Không thể kết nối đến Coordinator.")

def hien_thi_trang_thai_shard():
    """Hiển thị trạng thái các shard (Số lượng record và trạng thái lỗi)."""
    print("\n--- TRẠNG THÁI CÁC SHARD ---")
    try:
        response = requests.get(f"{COORDINATOR_URL}/status")
        if response.status_code == 200:
            data = response.json()["shards"]
            for shard_name, info in data.items():
                if "error" in info:
                    print(f"{shard_name} ({info['node_url']}): LỖI KẾT NỐI")
                else:
                    status = "LỖI - ĐANG DÙNG REPLICA" if info["primary_failed"] else "BÌNH THƯỜNG"
                    print(f"{shard_name} ({info['node_url']}): {info['record_count']} sinh viên - Trạng thái: {status}")
        else:
            print("Lỗi khi lấy trạng thái shard.")
    except requests.exceptions.RequestException:
         print("Lỗi: Không thể kết nối đến Coordinator.")

def kiem_tra_replication():
    """Mô tả việc replication đang hoạt động."""
    print("\n--- KIỂM TRA REPLICATION ---")
    print("Replication đã được thiết lập. Khi bạn thêm/sửa/xóa một sinh viên,")
    print("dữ liệu sẽ được tự động đồng bộ vào cả shard chính và shard replica.")
    print("Bạn có thể kiểm tra trực tiếp trong thư mục 'data/'.")
    print("Ví dụ: Mở file 'shard_0.json' và 'shard_0_replica.json' để xem dữ liệu có giống nhau không.")

def gia_lap_loi_shard():
    """Giả lập lỗi cho một shard."""
    print("\n--- GIẢ LẬP LỖI SHARD CHÍNH ---")
    print("0. Shard 0 (Port 5001)")
    print("1. Shard 1 (Port 5002)")
    print("2. Shard 2 (Port 5003)")
    print("3. Phục hồi tất cả Shard")
    
    lua_chon = input("Chọn shard để giả lập lỗi (hoặc 3 để phục hồi): ").strip()
    
    try:
        if lua_chon in ["0", "1", "2"]:
            response = requests.post(f"{COORDINATOR_URL}/simulate_error/{lua_chon}")
            print(response.json().get("message", "Đã gửi yêu cầu."))
        elif lua_chon == "3":
            for i in range(3):
                requests.post(f"{COORDINATOR_URL}/restore/{i}")
            print("Đã phục hồi toàn bộ shard về trạng thái bình thường.")
        else:
            print("Lựa chọn không hợp lệ.")
    except requests.exceptions.RequestException:
         print("Lỗi: Không thể kết nối đến Coordinator.")

def kiem_tra_failover():
    """Mô tả cách kiểm tra failover."""
    print("\n--- KIỂM TRA FAILOVER ---")
    print("Bước 1: Chọn chức năng (8) để giả lập lỗi một Shard (VD: Shard 0).")
    print("Bước 2: Dùng chức năng (2) để tìm một sinh viên thuộc Shard 0.")
    print("Bước 3: Hệ thống sẽ tự động chuyển sang đọc từ Replica.")
    print("Bước 4: Bạn sẽ thấy thông báo 'LẤY TỪ REPLICA' khi xem sinh viên.")
    print("Ghi chú: Nếu hệ thống không có Failover, bước 2 sẽ báo lỗi!")

def tao_du_lieu_mau():
    """Tạo ngẫu nhiên 50 sinh viên để test."""
    print("\n--- TẠO DỮ LIỆU MẪU (TEST MỞ RỘNG) ---")
    xac_nhan = input("Bạn có muốn tạo 50 sinh viên mẫu không? (y/n): ").strip().lower()
    
    if xac_nhan != 'y':
        return
        
    print("Đang tạo và phân phối dữ liệu vào các shard...")
    
    ho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng"]
    ten_dem = ["Văn", "Thị", "Ngọc", "Hữu", "Đức", "Thành", "Minh", "Hải", "Quang"]
    ten = ["Anh", "Bình", "Cường", "Dũng", "Em", "Hoa", "Lan", "Mai", "Tuấn", "Nam"]
    
    success_count = 0
    for i in range(1, 51):
        ma_sv = f"SV{str(i).zfill(3)}"
        ho_ten = f"{random.choice(ho)} {random.choice(ten_dem)} {random.choice(ten)}"
        lop = f"KTPM{random.randint(1, 5)}"
        gpa = round(random.uniform(2.0, 4.0), 2)
        
        data = {
            "student_id": ma_sv,
            "ho_ten": ho_ten,
            "lop": lop,
            "gpa": gpa,
        }
        
        try:
            r = requests.post(f"{COORDINATOR_URL}/set", json=data)
            if r.status_code == 200:
                success_count += 1
        except:
            pass
            
    print(f"Hoàn tất! Đã thêm thành công {success_count}/50 sinh viên.")
    print("Hãy dùng chức năng (6) để xem dữ liệu được phân phối (Sharding) như thế nào.")

def main():
    """Hàm chính điều khiển chương trình."""
    print("Đang kiểm tra kết nối tới Coordinator...")
    try:
        requests.get(COORDINATOR_URL)
    except:
        print(f"\nCẢNH BÁO: Không thể kết nối tới Coordinator tại {COORDINATOR_URL}")
        print("Vui lòng chạy file run_all.bat hoặc các file node/coordinator trước!\n")
        
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
            hien_thi_trang_thai_shard()
        elif lua_chon == "7":
            kiem_tra_replication()
        elif lua_chon == "8":
            gia_lap_loi_shard()
        elif lua_chon == "9":
            kiem_tra_failover()
        elif lua_chon == "10":
            tao_du_lieu_mau()
        elif lua_chon == "11" or lua_chon == "0":
            print("Cảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
            break
        else:
            print("Lỗi: Lựa chọn không hợp lệ, vui lòng chọn lại.")


if __name__ == "__main__":
    main()

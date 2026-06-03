# Student Management System using PupDB

## 1. Tên đề tài

**Student Management System using PupDB**

Đề tài demo thư viện **PupDB - A Simple File-Based Key-Value Database in Python** thông qua một chương trình quản lý sinh viên chạy trên terminal/cmd.

## 2. Thành viên nhóm 21

| STT | Họ tên | MSSV |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |

## 3. Mô tả PupDB

PupDB là một thư viện cơ sở dữ liệu key-value đơn giản, được viết bằng Python. Thư viện này lưu dữ liệu trực tiếp vào file JSON, vì vậy phù hợp với các chương trình nhỏ, bài demo hoặc các ứng dụng cần lưu dữ liệu đơn giản mà không muốn cài đặt hệ quản trị cơ sở dữ liệu phức tạp.

Trong dự án này, PupDB được dùng để lưu thông tin sinh viên vào file `students.json`.

## 4. Mô tả key-value database

Key-value database là kiểu cơ sở dữ liệu lưu dữ liệu theo cặp:

- **Key**: khóa định danh duy nhất dùng để tìm dữ liệu.
- **Value**: giá trị hoặc thông tin được lưu tương ứng với key.

Trong chương trình này:

- **Key** là mã sinh viên.
- **Value** là thông tin sinh viên gồm họ tên, lớp và GPA.

Ví dụ:

```json
{
  "SV001": {
    "ho_ten": "Nguyen Van A",
    "lop": "CNTT1",
    "gpa": 3.4
  }
}
```

## 5. Chức năng demo

Chương trình có các chức năng chính:

1. Thêm sinh viên.
2. Xem sinh viên theo mã sinh viên.
3. Cập nhật thông tin sinh viên.
4. Xóa sinh viên.
5. Liệt kê toàn bộ sinh viên.
6. Xóa toàn bộ dữ liệu.
7. Thoát chương trình.

Chương trình cũng có xử lý lỗi cơ bản:

- Không cho để trống mã sinh viên.
- Không cho thêm trùng mã sinh viên.
- GPA phải là số.
- Báo lỗi nếu tìm kiếm, cập nhật hoặc xóa sinh viên không tồn tại.

## 6. Cách cài đặt

Yêu cầu máy đã cài Python.

Bước 1: Clone repo về máy:

```bash
git clone https://github.com/<username>/group21-pupdb-student-management.git
cd group21-pupdb-student-management
```

Bước 2: Tạo môi trường ảo:

```bash
python -m venv .venv
```

Bước 3: Kích hoạt môi trường ảo.

Trên Windows:

```bash
.venv\Scripts\activate
```

Trên macOS/Linux:

```bash
source .venv/bin/activate
```

Bước 4: Cài thư viện cần thiết:

```bash
pip install -r requirements.txt
```

## 7. Cách chạy chương trình

Chạy lệnh:

```bash
python main.py
```

Sau đó chọn chức năng theo menu hiển thị trên terminal/cmd.

## 8. Cấu trúc thư mục

```text
group21-pupdb-student-management/
├── README.md
├── requirements.txt
├── main.py
├── students.json
├── docs/
│   └── bao-cao-tien-do.md
└── images/
```

## 9. Kết quả mong đợi

Sau khi chạy chương trình, người dùng có thể quản lý danh sách sinh viên bằng giao diện dòng lệnh. Dữ liệu sinh viên được lưu trong file `students.json`, trong đó mã sinh viên là key và thông tin sinh viên là value.

Chương trình phù hợp để demo trước giảng viên vì:

- Dễ cài đặt.
- Dễ chạy bằng terminal/cmd.
- Có menu tiếng Việt rõ ràng.
- Thể hiện được cách dùng PupDB để lưu dữ liệu key-value vào file JSON.

## 10. Link tham khảo

- Repo PupDB gốc: https://github.com/tuxmonk/pupdb
- Repo nhóm dự kiến: https://github.com/<username>/group21-pupdb-student-management

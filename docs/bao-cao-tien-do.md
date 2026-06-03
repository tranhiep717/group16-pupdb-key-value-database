# Báo cáo tiến độ thực hiện Bài tập lớn

## 1. Tên đề tài

**Student Management System using PupDB**

## 2. Thông tin sinh viên/nhóm

- Nhóm: 21
- Thành viên 1:
  - Họ tên:
  - MSSV:
- Thành viên 2:
  - Họ tên:
  - MSSV:
- Thành viên 3:
  - Họ tên:
  - MSSV:
- Thành viên 4:
  - Họ tên:
  - MSSV:

## 3. Link GitHub repo

Link GitHub repo:

## 4. Mô tả đề tài

Đề tài của nhóm là xây dựng chương trình **Student Management System using PupDB**. Đây là một chương trình quản lý sinh viên đơn giản, chạy bằng dòng lệnh terminal/cmd và sử dụng thư viện PupDB để lưu trữ dữ liệu.

PupDB là một thư viện cơ sở dữ liệu key-value được viết bằng Python. Thay vì dùng các hệ quản trị cơ sở dữ liệu lớn như MySQL, SQL Server hoặc PostgreSQL, PupDB lưu dữ liệu trực tiếp vào file JSON. Cách làm này phù hợp với các chương trình nhỏ, dễ demo và dễ quan sát dữ liệu sau khi chạy.

Trong chương trình của nhóm, mã sinh viên được sử dụng làm key. Thông tin sinh viên gồm họ tên, lớp và GPA được sử dụng làm value. Toàn bộ dữ liệu được lưu trong file `students.json`. Nhờ vậy, chương trình thể hiện được rõ cách hoạt động cơ bản của một cơ sở dữ liệu key-value.

## 5. Các công việc đã làm

Trong giai đoạn hiện tại, nhóm đã tìm hiểu thư viện PupDB và cách sử dụng các hàm cơ bản như `set`, `get`, `remove`, `items` và `truncate_db`. Đây là các thao tác quan trọng để thêm, đọc, xóa, liệt kê và xóa toàn bộ dữ liệu trong database.

Nhóm đã xây dựng cấu trúc thư mục ban đầu cho dự án gồm file mã nguồn `main.py`, file dữ liệu `students.json`, file cài đặt thư viện `requirements.txt`, tài liệu hướng dẫn `README.md`, thư mục `docs` để chứa báo cáo tiến độ và thư mục `images` để lưu hình ảnh minh họa nếu cần.

Về phần mã nguồn, nhóm đã xây dựng chương trình chạy trên terminal/cmd với menu tiếng Việt. Người dùng có thể chọn các chức năng như thêm sinh viên, xem sinh viên theo mã, cập nhật thông tin, xóa sinh viên, liệt kê toàn bộ sinh viên, xóa toàn bộ dữ liệu và thoát chương trình.

Nhóm cũng đã bổ sung xử lý lỗi cơ bản. Chương trình không cho để trống mã sinh viên, không cho thêm trùng mã sinh viên, kiểm tra GPA phải là số và thông báo lỗi khi người dùng tìm kiếm, cập nhật hoặc xóa sinh viên không tồn tại.

## 6. Tình hình demo mã nguồn

Mã nguồn hiện tại đã có thể chạy được bằng lệnh:

```bash
python main.py
```

Khi chạy chương trình, màn hình sẽ hiển thị menu chức năng. Người dùng nhập số tương ứng với chức năng muốn sử dụng. Sau khi thêm sinh viên, dữ liệu sẽ được PupDB lưu vào file `students.json`. Khi xem hoặc liệt kê sinh viên, chương trình đọc dữ liệu từ file này thông qua PupDB.

Nhìn chung, phần demo đã đáp ứng được mục tiêu chính là minh họa cách dùng PupDB như một cơ sở dữ liệu key-value đơn giản trong Python. Giao diện dòng lệnh chưa phức tạp nhưng rõ ràng, phù hợp để trình bày trước giảng viên trong buổi báo cáo.

## 7. Kế hoạch tiếp theo

Trong thời gian tiếp theo, nhóm sẽ tiếp tục kiểm thử chương trình với nhiều trường hợp dữ liệu khác nhau, ví dụ thêm nhiều sinh viên, nhập GPA sai định dạng, cập nhật thông tin và xóa dữ liệu. Nhóm cũng sẽ hoàn thiện phần README, bổ sung ảnh chụp màn hình demo vào thư mục `images` nếu cần.

Ngoài ra, nhóm sẽ rà soát lại nội dung báo cáo, điền đầy đủ thông tin thành viên, cập nhật link GitHub repo chính thức và chuẩn bị phần thuyết trình. Nếu còn thời gian, nhóm có thể cải thiện giao diện menu để chương trình dễ sử dụng hơn, nhưng vẫn giữ mục tiêu chính là đơn giản, dễ chạy và dễ hiểu.

## 8. Kết luận

Đến thời điểm hiện tại, nhóm đã hoàn thành phần khung dự án và mã nguồn demo cơ bản cho đề tài **Student Management System using PupDB**. Chương trình đã thể hiện được cách lưu trữ dữ liệu sinh viên theo mô hình key-value, trong đó mã sinh viên là key và thông tin sinh viên là value.

Đề tài có phạm vi vừa phải, phù hợp với yêu cầu bài tập lớn và giúp nhóm hiểu rõ hơn về cơ sở dữ liệu key-value, cách lưu dữ liệu vào file JSON, cũng như cách tổ chức một dự án Python đơn giản để nộp lên GitHub.

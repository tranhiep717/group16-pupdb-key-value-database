# Đề tài: PupDB - A Simple File-Based Key-Value Database in Python

## 1. Thông tin Nhóm 21

| STT | Họ và Tên | MSSV |
| :---: | :--- | :--- |
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |

## 2. Mục tiêu dự án
Dự án nhằm nghiên cứu và mở rộng một cơ sở dữ liệu Key-Value đơn giản (PupDB) thành một mô hình **Distributed Key-Value Database Mini**. Thông qua việc tự tay lập trình và mô phỏng, dự án giúp hiểu rõ bản chất hoạt động của các hệ thống phân tán như: định tuyến dữ liệu, phân mảnh (Sharding), sao chép (Replication), truy vấn phân tán (Distributed Query) và cơ chế chịu lỗi (Failover).

## 3. Công nghệ sử dụng
- **Ngôn ngữ lập trình:** Python 3
- **Thư viện chính:** PupDB (lưu trữ), Flask (tạo REST API cho mô hình phân tán), Requests (giao tiếp HTTP).
- **Môi trường hoạt động:** Windows/Linux Terminal.

---

## 4. Các khái niệm cốt lõi

### PupDB là gì?
PupDB là một thư viện cơ sở dữ liệu key-value rất nhỏ gọn, được viết bằng Python. PupDB lưu trữ toàn bộ dữ liệu trực tiếp vào một file văn bản định dạng JSON cục bộ. 

### Key-Value Database là gì?
Là mô hình lưu trữ phi quan hệ (NoSQL) trong đó dữ liệu được tổ chức dưới dạng cặp từ khóa - giá trị. Key là định danh duy nhất (ví dụ: Mã sinh viên), còn Value là dữ liệu tương ứng của định danh đó (ví dụ: object chứa Tên, Lớp, Điểm).

### Mô hình hệ thống dự án
Hệ thống chuyển từ mô hình Monolithic (1 file JSON duy nhất) sang mô hình Phân tán (Distributed) gồm:
- **Client (main.py):** Giao diện terminal cung cấp Menu thao tác cho người dùng.
- **Coordinator (coordinator.py):** Máy chủ trung tâm nhận Request từ Client và điều phối tới các Node.
- **Các Nodes (node.py):** Các Shard chạy độc lập ở các Port khác nhau, mỗi Node sở hữu một file JSON cục bộ để chứa một phần dữ liệu.

### Coordinator là gì?
Coordinator là thành phần đứng giữa Client và các Nodes. Nhiệm vụ chính là nhận yêu cầu, dùng thuật toán Hash (MD5) để quyết định xem Key (Mã SV) này sẽ thuộc về Node nào, sau đó định tuyến (route) request đến Node đó. Nó không trực tiếp lưu dữ liệu.

### Sharding là gì?
Sharding (Phân mảnh) là kỹ thuật chia nhỏ một cơ sở dữ liệu lớn ra thành nhiều phần nhỏ hơn (gọi là Shard). Trong dự án này, thay vì lưu toàn bộ sinh viên vào 1 file `students.json`, dữ liệu được chia nhỏ và phân tán lưu trên `shard_0.json`, `shard_1.json`, `shard_2.json`.

### Distributed Query là gì?
Distributed Query là việc gửi lệnh truy vấn từ Coordinator đến toàn bộ các Shard cùng một lúc. Sau khi các Shard trả kết quả về, Coordinator sẽ gom nhóm (aggregate) kết quả lại thành một danh sách duy nhất và trả cho Client.

### Replication là gì?
Replication (Sao chép) là cơ chế tạo ra nhiều bản sao (replica) cho mỗi Shard để chống mất dữ liệu. Trong hệ thống, mỗi khi có yêu cầu ghi vào file chính `shard_X.json`, Node sẽ đồng thời ghi một bản sao vào `shard_X_replica.json`.

### Failover là gì?
Failover là cơ chế tự động chuyển đổi sang hệ thống dự phòng khi hệ thống chính gặp sự cố. Nếu file `shard_X.json` bị lỗi hoặc mất mạng, Node sẽ tự động truy vấn dữ liệu từ file dự phòng `shard_X_replica.json` giúp ứng dụng tiếp tục hoạt động mà không bị sập (Crash).

---

## 5. Hướng dẫn sử dụng

### Cách cài đặt
1. Yêu cầu cài đặt sẵn Python (>= 3.7) trên máy tính.
2. Clone mã nguồn về và mở Terminal tại thư mục gốc của project.
3. Tạo môi trường ảo và kích hoạt:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

### Cách chạy chương trình
Vì đây là hệ thống phân tán nên cần chạy đồng thời Coordinator và các Nodes. Bạn có thể tự động bật toàn bộ bằng cách chạy file Batch (trên Windows):
```cmd
.\run_all.bat
```
*(File này sẽ tự động mở 4 cửa sổ ngầm: 1 Coordinator và 3 Shard)*

Sau khi hệ thống backend đã chạy, mở một cửa sổ Terminal mới, kích hoạt môi trường ảo (nếu chưa) và chạy Client UI:
```bash
python main.py
```

### Cách Test Demo trên Terminal
Chương trình cung cấp sẵn một Menu 11 chức năng. Để test các tính năng phân tán:
1. **Test Sharding:** Bấm số `10` để tạo tự động 50 sinh viên. Sau đó bấm số `6` để xem dữ liệu đã được chia đều cho 3 Shard.
2. **Test Replication:** Vào thư mục `data/` trong mã nguồn, mở file `shard_1.json` và `shard_1_replica.json` lên so sánh. Dữ liệu bên trong hoàn toàn giống nhau.
3. **Test Distributed Query:** Bấm số `5` để yêu cầu Coordinator lấy dữ liệu từ cả 3 Shard gộp lại thành danh sách 50 sinh viên.
4. **Test Failover:** Bấm số `8` để giả lập lỗi (Ví dụ chọn Shard 0). Tiếp theo bấm số `2` và nhập một sinh viên thuộc Shard 0. Hệ thống không lỗi mà hiện thông báo `TRẠNG THÁI: LẤY TỪ REPLICA (FAILOVER THÀNH CÔNG)`. Bấm lại `8` và chọn `3` để phục hồi.

---

## 6. Hình ảnh minh chứng

*(Chèn ảnh kết quả chạy Sharding vào đây)*
![Demo Sharding]()

*(Chèn ảnh kết quả test Distributed Query vào đây)*
![Demo Distributed Query]()

*(Chèn ảnh kết quả test Failover vào đây)*
![Demo Failover]()

---

## 7. Kết luận
Dự án đã thành công trong việc áp dụng thư viện siêu nhẹ PupDB để xây dựng và trực quan hóa các khái niệm cực kỳ phức tạp của Hệ thống Cơ sở dữ liệu phân tán. Mô hình không sử dụng các Database COTS (như MongoDB, Redis) mà hoàn toàn tự xây dựng logic điều hướng và phân mảnh trên Python thuần túy. Nó đáp ứng tốt tính trực quan, phục vụ cho việc học tập, nghiên cứu và báo cáo môn học.

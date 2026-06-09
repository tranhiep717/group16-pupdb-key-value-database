# CHƯƠNG 5. THỰC NGHIỆM VÀ ĐÁNH GIÁ HỆ THỐNG

## 5.1. Mục tiêu thực nghiệm
Mục tiêu của chương này là kiểm thử các tính năng phân tán của hệ thống quản lý sinh viên sử dụng PupDB vừa được xây dựng. Qua đó, chứng minh hệ thống hoạt động đúng với các lý thuyết về Sharding, Distributed Query, Replication và Failover.

## 5.2. Môi trường thực nghiệm
- **Hệ điều hành:** Windows 
- **Ngôn ngữ lập trình:** Python 3.x
- **Thư viện chính:** Flask, Requests, PupDB
- **Cấu trúc mạng:** Chạy mô phỏng Localhost với 4 cổng (Ports) giao tiếp độc lập:
  - Coordinator: Port 5050
  - Shard 0 (Node 1): Port 5001
  - Shard 1 (Node 2): Port 5002
  - Shard 2 (Node 3): Port 5003

## 5.3. Kịch bản thực nghiệm
Kịch bản thực nghiệm được thiết kế thành một luồng liên tục, đi từ việc chuẩn bị dữ liệu, kiểm tra phân mảnh, kiểm tra sao chép dữ liệu, đến việc mô phỏng sự cố và khả năng phục hồi. Người dùng sẽ thao tác trực tiếp trên giao diện Terminal (Client).

## 5.4. Thực nghiệm Sharding
**Thao tác:** 
Sử dụng chức năng số "10. Tạo dữ liệu mẫu để test mở rộng". Hệ thống sẽ tự động sinh ngẫu nhiên 50 sinh viên với mã SV, Họ tên, Lớp và Điểm GPA và gửi đồng loạt lên Coordinator.
**Kết quả mong đợi & Thực tế:**
Sau khi thêm 50 sinh viên, sử dụng chức năng số "6. Hiển thị trạng thái các shard", kết quả cho thấy dữ liệu không bị dồn vào một file duy nhất mà được phân tán tương đối đồng đều cho 3 Shard (Ví dụ: Shard 0: 16 SV, Shard 1: 17 SV, Shard 2: 17 SV) dựa trên thuật toán băm (MD5 Hash) mã sinh viên. Điều này chứng minh chức năng Sharding hoạt động chính xác.

## 5.5. Thực nghiệm Replication
**Thao tác:**
Sử dụng chức năng "7. Kiểm tra replication" sau khi đã tạo xong dữ liệu mẫu. Vào trực tiếp thư mục `data/` trong mã nguồn và mở cặp file `shard_0.json` và `shard_0_replica.json`.
**Kết quả mong đợi & Thực tế:**
Kích thước và nội dung (số dòng, số lượng sinh viên) của cả hai file đều hoàn toàn giống nhau. Bất kỳ thay đổi (cập nhật thông tin sinh viên hoặc xóa sinh viên) được thực hiện trên Client đều lập tức được phản ánh ở cả file chính và file sao chép. Tính năng Replication hoạt động ổn định.

## 5.6. Thực nghiệm Failover
**Thao tác:**
1. Chọn chức năng "8. Giả lập lỗi shard chính", nhập chọn Shard 0.
2. Dùng chức năng 6 để kiểm tra, Shard 0 sẽ báo trạng thái: `LỖI - ĐANG DÙNG REPLICA`.
3. Dùng chức năng 2 (Xem sinh viên), nhập một mã sinh viên mà theo hàm băm nó thuộc về Shard 0.
**Kết quả mong đợi & Thực tế:**
Hệ thống không bị đứng hay báo lỗi ứng dụng (Crash). Thay vào đó, dữ liệu sinh viên vẫn được hiển thị thành công kèm theo dòng thông báo đặc biệt: `TRẠNG THÁI: LẤY TỪ REPLICA (FAILOVER THÀNH CÔNG)`. Sau khi dùng chức năng phục hồi Shard, việc truy xuất trở lại bình thường.

## 5.7. Thực nghiệm Distributed Query
**Thao tác:**
Sử dụng chức năng "5. Liệt kê toàn bộ sinh viên (Distributed Query)".
**Kết quả mong đợi & Thực tế:**
Coordinator đã gửi lệnh đọc đến toàn bộ 3 Shard một cách song song. Kết quả trả về được tập hợp lại, sắp xếp theo mã sinh viên và hiển thị ra màn hình đầy đủ 50 sinh viên. Người dùng có cảm giác như đang truy vấn từ một Database tập trung duy nhất mà không cần biết dữ liệu thực chất đang nằm rải rác.

## 5.8. Đánh giá kết quả
Hệ thống đáp ứng hoàn toàn các yêu cầu đề ra. Các cơ chế cốt lõi của một hệ thống cơ sở dữ liệu phân tán như Sharding, Replication và Failover đều có thể được mô phỏng thành công bằng thư viện mã nguồn mở PupDB kết hợp với REST API của Flask.

## 5.9. Hạn chế của hệ thống
- **Thuật toán Hashing đơn giản:** Hiện dùng MD5 và chia lấy dư `% len(NODES)`. Nếu sau này muốn mở rộng thêm Shard 3, Shard 4 thì toàn bộ logic ánh xạ cũ sẽ bị sai lệch, cần có cơ chế Rebalancing (Phân bổ lại dữ liệu) hoặc sử dụng Consistent Hashing (Băm nhất quán).
- **Đồng bộ Replica cứng:** Trong thực tế, ghi vào Replica nên là quá trình bất đồng bộ (Asynchronous) để giảm độ trễ (Latency) cho Client.
- **PupDB chưa thiết kế cho Concurrency:** Việc nhiều Node/Thread cùng ghi vào một file JSON dễ dẫn đến lỗi lock file trên hệ điều hành.

## 5.10. Hướng phát triển tiếp theo
- Triển khai **Consistent Hashing** để dễ dàng scale-out (thêm node) hoặc scale-in (bớt node) mà không ảnh hưởng tới toàn bộ hệ thống.
- Viết giao diện Web UI bằng ReactJS hoặc VueJS thay vì sử dụng Terminal Command Line.
- Lưu lịch sử thao tác (Log Write-ahead) để tự động khôi phục dữ liệu từ đầu khi file bị hỏng nặng.

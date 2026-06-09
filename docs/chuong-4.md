# CHƯƠNG 4. PHÁT TRIỂN REPLICATION VÀ FAILOVER

## 4.1. Giới thiệu Replication
Replication (Sao chép dữ liệu) là kỹ thuật lưu trữ cùng một dữ liệu trên nhiều nút (node) hoặc nhiều cơ sở dữ liệu khác nhau. Thay vì chỉ có một bản gốc duy nhất, hệ thống sẽ duy trì nhiều bản sao (replica) để đảm bảo dữ liệu luôn sẵn sàng.

## 4.2. Mục đích của Replication trong hệ thống phân tán
Trong một hệ thống phân tán, Replication mang lại hai lợi ích chính:
1. **Tính sẵn sàng cao (High Availability) và Khả năng chịu lỗi (Fault Tolerance):** Nếu một node bị hỏng hoặc mất mạng, dữ liệu vẫn an toàn và có thể truy cập từ các bản sao khác. Không có hiện tượng mất mát dữ liệu do Single Point of Failure (SPOF).
2. **Tăng hiệu suất đọc (Read Scalability):** Hệ thống có thể phân bổ các yêu cầu đọc (read request) sang nhiều bản sao khác nhau, giảm tải cho node chính và tăng tốc độ phản hồi.

## 4.3. Cách nhóm triển khai Replication trong dự án
Trong dự án này, nhóm đã xây dựng cơ chế Replication đơn giản ở cấp độ Shard (Node). Cụ thể:
- Mỗi Node khi chạy sẽ khởi tạo đồng thời 2 file cơ sở dữ liệu PupDB: một file chính (`shard_X.json`) và một file sao chép (`shard_X_replica.json`).
- Khi có yêu cầu ghi dữ liệu (thêm, sửa, xóa) gửi từ Coordinator đến Node, Node sẽ thực hiện thao tác đó trên **cả hai file**. 
- Nhờ vậy, file `replica` luôn được đồng bộ (synchronous replication) theo thời gian thực với file chính. Nếu kiểm tra thư mục `data/`, người dùng sẽ luôn thấy dữ liệu ở hai file này hoàn toàn giống nhau.

## 4.4. Giới thiệu Failover
Failover (Chuyển đổi dự phòng) là cơ chế tự động chuyển hướng các yêu cầu từ một thành phần hệ thống đang bị lỗi sang một thành phần dự phòng khác (replica/backup) đã được chuẩn bị sẵn, mà không làm gián đoạn toàn bộ hoạt động của hệ thống.

## 4.5. Mục đích của Failover
- Đảm bảo hệ thống vẫn tiếp tục hoạt động trơn tru đối với người dùng cuối (End-user) ngay cả khi một phần của hệ thống gặp sự cố phần cứng hoặc phần mềm.
- Kết hợp với Replication để khai thác tối đa giá trị của bản sao lưu. Replication giữ dữ liệu an toàn, còn Failover là hành động "mang dữ liệu an toàn đó ra sử dụng khi cần thiết".

## 4.6. Cách nhóm triển khai Failover trong dự án
Để chứng minh hệ thống có khả năng chịu lỗi, nhóm đã xây dựng tính năng Failover trên từng Node:
- Mỗi Node duy trì một cờ trạng thái `simulate_fail_primary` (mặc định là False).
- Coordinator cung cấp một API giúp "Giả lập lỗi" trên bất kỳ Node nào. Khi gọi API này, cờ `simulate_fail_primary` của Node tương ứng sẽ chuyển sang True (coi như file `shard_X.json` đã bị hỏng hoặc không thể truy cập).
- Khi có yêu cầu truy vấn (đọc một sinh viên hoặc lấy toàn bộ sinh viên), Node sẽ kiểm tra trạng thái lỗi này. Nếu phát hiện lỗi, thay vì đọc từ file chính, Node sẽ **tự động** chuyển sang đọc dữ liệu từ đối tượng `replica_db` (tương ứng với file `shard_X_replica.json`).
- Sau đó, Node sẽ trả kết quả về cho Coordinator kèm theo một cờ báo hiệu `used_replica=True` để giao diện người dùng biết rằng dữ liệu này được phục hồi từ hệ thống dự phòng.

## 4.7. Minh họa luồng hoạt động
1. **Ghi dữ liệu (Replication):**
   Client -> Coordinator -> Node(Shard 0) -> Ghi vào `shard_0.json` & Ghi vào `shard_0_replica.json`.
2. **Sự cố xảy ra:**
   Người dùng gọi tính năng "Giả lập lỗi shard chính" trên Shard 0.
3. **Đọc dữ liệu (Failover):**
   Client yêu cầu lấy thông tin SV001 (thuộc Shard 0) -> Coordinator -> Node(Shard 0).
   Node(Shard 0) phát hiện file chính lỗi -> Tự động chuyển qua đọc từ `shard_0_replica.json` -> Trả về Client kèm thông báo Failover thành công.

## 4.8. Nhận xét
Việc cài đặt thành công Replication và Failover đã chứng minh được tính đúng đắn của mô hình lý thuyết trên môi trường thực hành. Hệ thống quản lý sinh viên sử dụng PupDB không còn là một ứng dụng tĩnh lưu trên một file duy nhất, mà đã trở thành một hệ thống cơ sở dữ liệu phân tán mini có khả năng tự động đồng bộ và chịu lỗi cơ bản.

# CHANGELOG - EXAM ARCHITECT

## [4.0.0] - 2026-10-26
### Added
- **Đổi tên chính thức thành Exam Architect** theo định hướng chuẩn khảo thí quốc tế.
- **Hệ thống 4 lệnh vận hành 1-chạm:** Tạo đề, Hấp thụ Test Bank GS.TS, Kiểm định đề, Tối ưu đề.
- **Bộ công cụ `testbank_ingester.py`:** Tự động hấp thụ tri thức, cấu trúc câu hỏi và trích xuất nhóm "Thuật ngữ cùng họ" (Sibling Concepts) từ file Test Bank PDF của Pearson, McGraw-Hill...
- **Nguyên tắc Sibling Concepts chuẩn GS.TS:** Phương án nhiễu bắt buộc là các khái niệm anh em cùng chương học.
- **Hỗ trợ Bẫy ngược (Reverse Traps):** Khuyến khích dùng "Tất cả đều đúng/sai" làm phương án nhiễu để trừng phạt thói quen đoán mò.
- **Mở rộng Giáo trình có kiểm soát (Controlled Expansion):** Đào sâu kiến thức giáo trình chính và Test Bank mà không bị lan man sang môn khác.

## [3.0.0] - 2026-10-25
### Added
- Kiến trúc 3 thành phần: Spec Builder (Hamilton-Hare) - Independent Auditor - Exporter.
- Xuất bản 3 chế độ: Chế độ A (Mock Exam SV), Chế độ B (Master Bank), Chế độ C (Azota Package).
- Bộ 10 Quy tắc Vàng thiết kế câu hỏi.

## [2.0.0] - 2026-10-24
### Added
- Thích ứng động theo từng môn học (Subject-adaptive: Tính toán, Lý thuyết, Hệ thống).
- Trích xuất tự động từ Đề cương môn học (DCMH).

# CHANGELOG - EXAM ARCHITECT

## [4.1.0] - 2026-10-26
### Added
- **Định hướng chuyên sâu 100% vào Ra đề (Question Authoring):** Loại bỏ tính năng ngoài lề, tập trung hoàn toàn vào kỹ nghệ thiết kế và biên soạn đề thi đại học.
- **Bộ 4 Định dạng câu hỏi chuyên sâu:**
  1. *Format 1:* Ghép mệnh đề kết hợp (Compound Statements - Đúng/Sai, (i) & (ii)) triệt tiêu đoán mò 50/50.
  2. *Format 2:* Tình huống nghiệp vụ & Đánh đổi kiến trúc (Scenario-based & Architectural Trade-offs) cho bài toán điểm 8-10.
  3. *Format 3:* Trình tự quy trình & Luồng xử lý (Process Sequencing & Lifecycle Stages).
  4. *Format 4:* Tính toán vi mô 30 giây (Micro-Calculation & Formula Traps) với bước giải nháp, đơn vị và quy ước làm tròn bắt buộc.
- **Cơ chế Phân rã Chủ đề con & Chống trùng lặp khái niệm (Topic Coverage & Anti-Redundancy):**
  - Ràng buộc hạn ngạch: Mỗi chủ đề con tối đa 20%-25% số câu của đề.
  - Ràng buộc đơn nhất thực thể & đa dạng hóa góc nhìn (Concept Unique Constraint).
  - Tích hợp kiểm tra tự động trùng lặp từ ngữ thân câu (>85% Word Overlap) vào `question_auditor.py`.

## [4.0.0] - 2026-10-26
### Added
- **Đổi tên chính thức thành Exam Architect** theo định hướng chuẩn khảo thí quốc tế.
- **Hệ thống 4 lệnh vận hành 1-chạm:** Tạo đề, Hấp thụ Test Bank, Kiểm định đề, Tối ưu đề.
- **Hệ thống kiểm định 2 tầng & Minh bạch học thuật:** Phân tách rõ ràng giữa Hard Errors (lỗi kỹ thuật chặn đứng) và Soft Warnings (cờ cảnh báo sư phạm), kèm Academic Disclaimer.
- **Bộ công cụ `testbank_ingester.py`:** Tự động hấp thụ tri thức, cấu trúc câu hỏi và trích xuất nhóm "Thuật ngữ cùng họ" (Sibling Concepts) từ file Test Bank PDF của Pearson, McGraw-Hill...
- **Nguyên tắc Sibling Concepts:** Phương án nhiễu bắt buộc là các khái niệm anh em cùng chương học.
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

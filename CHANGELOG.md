# CHANGELOG - EXAM ARCHITECT

## [4.2.0] - 2026-10-29
### Added
- **Lệnh Meta-Prompt cho NotebookLM (Quick Command #5):** Tự động phân tích kết quả thi Azota, lọc 100% các câu làm sai (`✗`), phân loại lỗ hổng kiến thức và sinh Meta-Prompt chuẩn hóa sẵn sàng 1-Click để dán vào NotebookLM nhờ đối chiếu Slide/Giáo trình nguồn giảng giải bản chất lý thuyết, giải mã bẫy thi và đúc kết quy tắc ghi nhớ logic.
- **Bộ công cụ `azota_diagnostic.py`:** Trích xuất kết quả thi Azota và tự động sinh Meta-Prompt.
- **Quy tắc Đối xứng Chú thích Tiếng Anh (English Term Symmetry):** Chặn đứng lỗi thiên vị hình thức (chỉ duy nhất câu đúng có tiếng Anh) hoặc ngược lại; nếu dùng tiếng Anh thì cả 4 phương án đều phải có, nếu thuần Việt thì cả 4 phương án dùng thuần Việt.
- **Quy tắc Chống thiên vị diễn giải (No Elaboration Bias) & Chống bắt chữ (Anti-Clang Association):** Thân câu hỏi không dùng từ đời thường để mớm nghĩa đen cho đáp án; phương án đúng không được kèm vế giải thích phụ kéo dài nếu các câu sai không có.
- **Nâng cấp `question_auditor.py`:** Tự động phát hiện lỗi bất đối xứng chú thích tiếng Anh (`English Term Asymmetry Check`), lỗi thiên vị vế giải thích (`Elaboration Bias`), và mở rộng bộ lọc từ khóa nhiễu ngớ ngẩn/lạc miền kiến thức.

## [4.1.0] - 2026-10-26
### Added
- **Định hướng chuyên sâu 100% vào Ra đề (Question Authoring):** Loại bỏ tính năng ngoài lề, tập trung hoàn toàn vào kỹ nghệ thiết kế và biên soạn đề thi đại học.
- **Bộ 4 Định dạng câu hỏi chuyên sâu:**
  1. *Format 1:* Thẩm định Tổ hợp Mệnh đề (Multi-Statement Evaluation) linh hoạt từ 2 mệnh đề đối ngẫu `(i)` & `(ii)` đến 3–4 mệnh đề tổng hợp `(i), (ii), (iii), (iv)` chọn tập hợp con hoặc đếm số lượng đúng. Triệt tiêu đoán mò 50/50.
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

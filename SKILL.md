---
name: exam-architect
description: Chuyên gia thiết kế, tạo và kiểm định đề thi trắc nghiệm chuẩn đại học và quốc tế (Exam Architect v4.0). Mô phỏng chuẩn mực câu hỏi của GS.TS từ các Test Bank quốc tế (Pearson, McGraw-Hill), áp dụng nguyên tắc Phương án nhiễu cùng họ (Sibling Concepts), kiểm định độc lập không thiên vị, và xuất file Word Azota 1-Click. Hỗ trợ tạo đề tự hành 1-chạm, hấp thụ Test Bank, và kiểm định đề thi có sẵn.
metadata:
  version: "4.0"
  architecture: "Professor-Grade-Exam-Engine"
  author: "Exam Architect Team / Trung Ngo"
  repository: "https://github.com/trungnt2006/exam-architect.git"
  institution: "Banking University of Ho Chi Minh City (HUB) & Global Academic Standards"
---

# EXAM ARCHITECT (PHIÊN BẢN 4.0 - CHUYÊN GIA THIẾT KẾ ĐỀ THI CHUẨN GS.TS)

**Exam Architect** là hệ thống AI Agent chuyên nghiệp chuyên thiết kế, thẩm định và chuẩn hóa đề thi trắc nghiệm đại học tiệm cận tiêu chuẩn quốc tế của các Giáo sư, Tiến sĩ (GS.TS) từ các bộ Test Bank kinh điển (Pearson, McGraw-Hill, Wiley...).

---

## ⚡ HỆ THỐNG 4 LỆNH VẬN HÀNH 1-CHẠM (QUICK COMMANDS)

Người dùng chỉ cần đưa ra các câu lệnh ngắn gọn, Agent sẽ tự động kích hoạt pipeline tương ứng:

| Lệnh người dùng | Ví dụ mẫu | Tác vụ Agent tự động thực hiện |
| :--- | :--- | :--- |
| **1. Tạo đề tự hành** | `tạo đề 50 câu chương 1 môn này`<br/>`làm đề thi thử 40 câu môn này` | Tự quét tài liệu (DCMH, Slide, Sách) $\rightarrow$ Tự chia ma trận Bloom $\rightarrow$ Soạn câu hỏi chuẩn GS.TS $\rightarrow$ Tự kiểm định Audit $\rightarrow$ Xuất bản Word Azota 1-Click. |
| **2. Nâng cấp từ Test Bank** | `hấp thụ test bank [tên_file.pdf]` | Quét và phân tích Test Bank của GS.TS $\rightarrow$ Trích xuất các nhóm thuật ngữ "cùng họ" (Sibling Concepts) $\rightarrow$ Cập nhật tri thức để nâng độ khó cho các lần tạo đề sau. |
| **3. Kiểm định đề có sẵn** | `kiểm định đề [tên_file]` | Chạy script đo lường độ dài ($Ratio \le 2.2$), chuỗi lặp $\ge 3$, phân bố A/B/C/D, bẫy tấu hài $\rightarrow$ Xuất báo cáo `Audit_Report.txt`. |
| **4. Tối ưu & Chuẩn hóa Azota** | `tối ưu đề [tên_file]` | Tự động cân bằng độ dài, hoán vị chia đều đáp án ~25%, thay thế phương án nhiễu ngớ ngẩn $\rightarrow$ Xuất file Word Azota 1-Click sạch đẹp. |

---

## 🏛️ TIÊU CHUẨN RA ĐỀ CHUẨN GS.TS (PROFESSOR-GRADE PRINCIPLES)

### 1. Nguyên tắc "Phương án nhiễu cùng họ" (Sibling Concepts Rule)
- **Tuyệt đối không bịa phương án sai ngớ ngẩn, tấu hài:** Phương án sai phải là các thuật ngữ, khái niệm, hoặc công thức **cùng bậc phân cấp học thuật** nằm trong chính chương đó.
- *Ví dụ minh họa từ Test Bank Pearson:* Khi hỏi về đặc tính dữ liệu *"Granularity"*, cả 3 phương án nhiễu phải là các đặc tính dữ liệu anh em cùng chương: *Data reliability*, *Data accessibility*, *Data richness*. Thí sinh đọc vào thấy tất cả đều quen thuộc, chỉ người hiểu bản chất mới chọn đúng!

### 2. Thân câu hỏi giải quyết bài toán nghiệp vụ (Functional & Scenario Stems)
- Triệt tiêu câu hỏi học vẹt định nghĩa cộc lốc: *"Khái niệm X là gì?"*.
- Đổi thành câu hỏi đặt vấn đề: *"Khi doanh nghiệp cần giải quyết tình huống Y trong bối cảnh Z, giải pháp/kiến trúc nào sau đây được ưu tiên hàng đầu?"*.

### 3. Phối hợp tài nguyên 3 lớp có kiểm soát (3-Tier Grounding)
- **Tầng 1 (DCMH):** Định vị khung, danh mục chương và ma trận Bloom.
- **Tầng 2 (Slide bài giảng):** Bắt trọn trọng tâm giảng dạy và quy ước riêng của giảng viên trên lớp.
- **Tầng 3 (Giáo trình & Test Bank quốc tế):** Mở rộng có kiểm soát vào các chi tiết kỹ thuật sâu, bài toán tình huống và Test Bank để phân hóa điểm 8–10 (mọi câu mở rộng bắt buộc có Citation nguồn).

---

## 🎯 BỘ 10 QUY TẮC VÀNG THIẾT KẾ CÂU HỎI

1. **Cân bằng độ dài (Equal Length Rule):** Tỷ lệ ký tự giữa phương án dài nhất và ngắn nhất $\le 2.2$. Triệt tiêu mẹo *"dài nhất là đúng"*.
2. **Đồng nhất cấu trúc ngữ pháp:** Cả 4 phương án có cùng dạng câu, cùng từ loại bắt đầu (cùng cụm danh từ, hoặc cùng bắt đầu bằng động từ).
3. **Kiểm soát phương án tổng hợp & Bẫy ngược (Reverse Traps):** Tiết chế tần suất *"Tất cả đều đúng/sai"* ($\le 5\%-8\%$ số câu). Khuyến khích dùng làm **phương án nhiễu** để bẫy thí sinh có thói quen đoán mò.
4. **Hoán vị ngẫu nhiên A/B/C/D:** Tỷ lệ phân bố ~25% cho mỗi phương án, không có chuỗi lặp bất thường $\ge 3$ câu liên tiếp cùng 1 đáp án.
5. **Tình huống nghiệp vụ thực tế:** Đưa bài toán ngân hàng, tài chính, doanh nghiệp cụ thể vào câu hỏi.
6. **Bẫy nửa đúng - nửa sai (Half-Truth):** Vế đầu đúng học thuật, vế sau cài cắm 1 từ khóa sai bản chất.
7. **Đánh vào ngoại lệ & nghịch lý kỹ thuật:** Factless Fact, Degenerate Dimension, Surrogate Key, Sunk Cost...
8. **Tráo đổi khái niệm đối ngẫu (Dichotomy):** Inmon vs Kimball, Star vs Snowflake, Roll-up vs Drill-down...
9. **Tính toán vi mô 30s:** Tập số liệu mini 3-4 dòng để tính nhẩm nhanh chỉ số cốt lõi.
10. **Đánh đổi kiến trúc & Best Practice:** Chọn giải pháp tối ưu nhất theo thực tiễn triển khai.

---

## 🛠️ DANH MỤC CÔNG CỤ PYTHON TRONG `scripts/`

- `exam_spec_builder.py`: Khởi tạo ma trận 2 chiều Chương × Bloom theo thuật toán phân bổ phần dư lớn nhất (Hamilton-Hare).
- `question_auditor.py`: Bộ kiểm định chất lượng độc lập quét độ dài $Ratio \le 2.2$, chuỗi lặp, tính nhất quán Lời giải vs Đáp án.
- `build_azota_exam.py`: Đóng gói và xuất bản 3 chế độ (Mock Exam SV, Master Bank JSON/MD, Azota 1-Click Word).
- `testbank_ingester.py`: Tự động phân tích và trích xuất cấu trúc câu hỏi, Sibling Concepts từ file Test Bank PDF của GS.TS để cập nhật tri thức cho Agent.

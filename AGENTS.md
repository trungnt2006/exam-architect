# BỘ QUY TẮC THIẾT KẾ VÀ KIỂM ĐỊNH ĐỀ THI TRẮC NGHIỆM CHUẨN GS.TS (EXAM ARCHITECT v4.0)

**Tên hệ thống:** Exam Architect  
**Kho mã nguồn:** https://github.com/trungnt2006/exam-architect.git  
**Phạm vi áp dụng:** Toàn bộ các môn học và kỳ thi tại HUB cũng như các tiêu chuẩn học thuật đại học.

---

## ⚡ HỆ THỐNG 4 LỆNH VẬN HÀNH 1-CHẠM (QUICK COMMANDS)

Khi người dùng đưa ra các lệnh ngắn gọn, Agent tự động thực thi trọn gói mà không bắt người dùng điền form thủ công:

1. **LỆNH TẠO ĐỀ:**
   👉 `"tạo đề [số câu] câu chương [X] môn này"` (hoặc `"làm đề thi thử 40 câu môn này"`)
   - Tự động nhận diện môn học, tài liệu DCMH, Slide chương tương ứng.
   - Tự chia ma trận Bloom chuẩn đại học (~30% Nhận biết, ~40% Thông hiểu, ~30% Vận dụng).
   - Tự soạn thảo câu hỏi áp dụng 10 Quy tắc Vàng và nguyên tắc Sibling Concepts chuẩn GS.TS.
   - Tự chạy script kiểm định `question_auditor.py` đảm bảo 100% PASS.
   - Tự xuất file Word chuẩn Azota 1-Click (`<u><b>A.</b></u>`, kèm lời giải chi tiết, kết thúc bằng `HẾT`).

2. **LỆNH NÂNG CẤP TỪ TEST BANK GS.TS:**
   👉 `"hấp thụ test bank [tên_file.pdf]"`
   - Tự động quét file Test Bank quốc tế của tác giả (Pearson, McGraw-Hill, Wiley...).
   - Trích xuất các nhóm "Thuật ngữ cùng họ" (Sibling Concepts) và câu hỏi mẫu vàng.
   - Cập nhật tri thức vào bộ nhớ để nâng độ khó cho các lần tạo đề sau.

3. **LỆNH KIỂM ĐỊNH ĐỀ THI:**
   👉 `"kiểm định đề [tên_file]"`
   - Chạy script đo lường định lượng tỷ lệ độ dài ($Ratio \le 2.2$), chuỗi lặp $\ge 3$ câu, tỷ lệ phân bố đáp án A/B/C/D và phát hiện phương án ngớ ngẩn.
   - Xuất file báo cáo `Audit_Report.txt`.

4. **LỆNH TỐI ƯU & CHUẨN HÓA AZOTA:**
   👉 `"tối ưu đề [tên_file]"`
   - Tự động cân bằng độ dài, hoán vị chia đều đáp án ~25%, sửa phương án tấu hài thành học thuật.
   - Đóng gói xuất file Word Azota 1-Click và Mock Exam cho sinh viên.

---

## I. NGUYÊN TẮC RA ĐỀ CHUẨN GS.TS

1. **Phương án nhiễu cùng họ (Sibling Concepts):** Phương án sai phải là các thuật ngữ, khái niệm hoặc công thức cùng cấp bậc trong chính chương đó. Triệt tiêu các phương án sai ngớ ngẩn, tấu hài.
2. **Thân câu hỏi đặt vấn đề (Functional Stem):** Tránh câu hỏi học vẹt cộc lốc; đặt câu hỏi vào bối cảnh doanh nghiệp cần ra quyết định hoặc giải quyết tình huống kỹ thuật.
3. **Phân loại 3 nhóm môn học:**
   - *Môn Tính toán (Toán kinh tế, Thống kê, Tài chính DN, Kế toán...):* Phải giải nháp độc lập; ghi rõ kỳ hạn, đơn vị và quy ước làm tròn số; bẫy sai số công thức.
   - *Môn Lý thuyết & Pháp lý (Luật ngân hàng, Quản trị, Marketing, Tiền tệ...):* Chống học vẹt, so sánh bản chất và giải quyết tình huống nghiệp vụ ngân hàng/doanh nghiệp.
   - *Môn Công nghệ & Dữ liệu (Kho dữ liệu, CSDL, HTTT, An toàn bảo mật...):* Kiến trúc, đánh đổi giải pháp (trade-off), bẫy ngoại lệ kỹ thuật.

---

## II. PHỐI HỢP NGUỒN TÀI NGUYÊN 3 LỚP & MỞ RỘNG CÓ KIỂM SOÁT

1. **Tầng 1 (DCMH):** Định vị khung, danh mục chương và ma trận Bloom.
2. **Tầng 2 (Slide bài giảng):** Bắt trọn nội dung cốt lõi và quy ước giảng dạy của giảng viên trên lớp.
3. **Tầng 3 (Giáo trình chính & Test Bank quốc tế):** Mở rộng có kiểm soát vào các chi tiết kỹ thuật sâu, bài toán tình huống nâng cao để phân hóa điểm 8–10 (bắt buộc có Citation dẫn chứng rõ ràng).

---

## III. HỆ THỐNG 10 QUY TẮC VÀNG THIẾT KẾ CÂU HỎI

1. **Cân bằng độ dài (Equal Length Rule):** Tỷ lệ ký tự phương án dài nhất / ngắn nhất $\le 2.2$. Triệt tiêu mẹo *"dài nhất là đúng"*.
2. **Đồng nhất cấu trúc ngữ pháp:** Cả 4 phương án cùng loại từ (cùng cụm danh từ, hoặc cùng bắt đầu bằng một động từ).
3. **Kiểm soát phương án tổng hợp & Bẫy ngược (Smart Distractors & Reverse Traps):** Tiết chế tần suất *"Tất cả đều đúng/sai"* ($\le 5\%-8\%$ số câu). Khuyến khích cài cắm làm **phương án nhiễu** để bẫy thí sinh có thói quen đoán mò.
4. **Hoán vị ngẫu nhiên A/B/C/D:** Tỷ lệ phân bố ~25% cho mỗi phương án, không lặp $\ge 3$ câu liên tiếp cùng 1 đáp án.
5. **Tình huống nghiệp vụ thực tế:** Đưa bài toán ngân hàng, tài chính, doanh nghiệp cụ thể vào câu hỏi.
6. **Bẫy nửa đúng - nửa sai (Half-Truth):** Vế đầu đúng học thuật, vế sau cài cắm 1 từ khóa sai bản chất.
7. **Đánh vào ngoại lệ & nghịch lý kỹ thuật:** Factless Fact, Degenerate Dimension, Surrogate Key, Sunk Cost...
8. **Tráo đổi khái niệm đối ngẫu (Dichotomy):** Inmon vs Kimball, Star vs Snowflake, Roll-up vs Drill-down...
9. **Tính toán vi mô 30s:** Tập số liệu 3-4 dòng để tính nhẩm nhanh chỉ số cốt lõi.
10. **Đánh đổi kiến trúc & Best Practice:** Chọn giải pháp tối ưu nhất theo thực tiễn.

---

## IV. QUY CHUẨN XUẤT BẢN AZOTA 1-CLICK (.DOCX)
- Tiêu đề câu: `Câu X: [Nội dung]` (in đậm `Câu X: `).
- Đáp án đúng: Gạch chân và in đậm chữ cái phương án (`<u><b>A.</b></u>`).
- Lời giải: Có khối `Lời giải:\nChọn X.\n[Giải thích chi tiết & phân tích bẫy thi]`.
- Kết thúc đề: Dòng **`HẾT`** in đậm căn giữa. Tuyệt đối **KHÔNG** có bảng đáp án thừa ở cuối file để tránh lỗi nuốt chữ của trình soạn thảo Azota.

---

## V. HỆ THỐNG KIỂM ĐỊNH 2 TẦNG & MINH BẠCH HỌC THUẬT
1. **Tầng 1 — Kiểm tra Kỹ thuật & Logic dữ liệu (Hard Errors):**
   - Chặn đứng các lỗi: Thiếu phương án, đáp án ngoài A/B/C/D, trùng lặp phương án, mâu thuẫn giữa Đáp án và Lời giải, phương án ngớ ngẩn (tấu hài).
2. **Tầng 2 — Cờ Cảnh báo Sư phạm & Hình thức (Heuristic Warnings):**
   - Không ép cứng máy móc: Cảnh báo chênh lệch độ dài lớn ($Ratio > 2.5$) hoặc lệch phân bố A/B/C/D nhằm gợi ý người tạo đề xem xét. Với câu tính toán (đáp án số ngắn) hoặc câu định nghĩa, chênh lệch độ dài là tự nhiên và hợp lệ.
3. **Minh bạch Học thuật (Academic Disclaimer):**
   - Script tự động kiểm tra cấu trúc và tính ngẫu nhiên của trắc nghiệm, không thể tự động chứng minh 100% tính đúng đắn về chuyên môn. Mọi câu hỏi cần có Citation nguồn để người học đối chiếu lại với Slide bài giảng của giảng viên.

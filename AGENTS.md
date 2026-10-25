# BỘ QUY TẮC THIẾT KẾ VÀ KIỂM ĐỊNH ĐỀ THI TRẮC NGHIỆM (EXAM ARCHITECT v4.0)

**Tên hệ thống:** Exam Architect  
**Kho mã nguồn:** https://github.com/trungnt2006/exam-architect.git  
**Phạm vi áp dụng:** Toàn bộ các môn học và kỳ thi tại HUB cũng như các môn học đại học.

---

## ⚡ HỆ THỐNG 4 LỆNH VẬN HÀNH 1-CHẠM (QUICK COMMANDS)

Khi người dùng đưa ra các lệnh ngắn gọn, Agent tự động thực thi trọn gói mà không bắt người dùng điền form thủ công:

1. **LỆNH TẠO ĐỀ:**
   👉 `"tạo đề [số câu] câu chương [X] môn này"` (hoặc `"làm đề thi thử 40 câu môn này"`)
   - Tự động nhận diện môn học, tài liệu DCMH, Slide chương tương ứng.
   - Tự chia ma trận Bloom chuẩn đại học (~30% Nhận biết, ~40% Thông hiểu, ~30% Vận dụng).
   - Tự soạn thảo câu hỏi áp dụng 10 Quy tắc Vàng và nguyên tắc Sibling Concepts học hỏi từ Test Bank.
   - Tự chạy script kiểm định `question_auditor.py` kiểm tra kỹ thuật và logic.
   - Tự xuất file Word chuẩn Azota 1-Click (`<u><b>A.</b></u>`, kèm lời giải chi tiết, kết thúc bằng `HẾT`).

2. **LỆNH HỌC HỎI TỪ TEST BANK:**
   👉 `"hấp thụ test bank [tên_file.pdf]"`
   - Tự động quét file Test Bank quốc tế của tác giả (Pearson, McGraw-Hill, Wiley...).
   - Trích xuất các nhóm "Thuật ngữ cùng họ" (Sibling Concepts) và câu hỏi mẫu hay.
   - Cập nhật tri thức vào bộ nhớ để nâng cao chất lượng cho các lần tạo đề sau.

3. **LỆNH KIỂM ĐỊNH ĐỀ THI:**
   👉 `"kiểm định đề [tên_file]"`
   - Chạy script đo lường định lượng tỷ lệ độ dài ($Ratio \le 2.2$), chuỗi lặp $\ge 3$ câu, tỷ lệ phân bố đáp án A/B/C/D và phát hiện phương án ngớ ngẩn.
   - Xuất file báo cáo `Audit_Report.txt`.

4. **LỆNH TỐI ƯU & CHUẨN HÓA AZOTA:**
   👉 `"tối ưu đề [tên_file]"`
   - Tự động cân bằng độ dài, hoán vị chia đều đáp án ~25%, sửa phương án tấu hài thành học thuật.
   - Đóng gói xuất file Word Azota 1-Click và Mock Exam cho sinh viên.

---

## I. NGUYÊN TẮC RA ĐỀ HỌC HỎI TỪ TEST BANK QUỐC TẾ

1. **Phương án nhiễu cùng họ (Sibling Concepts):** Phương án sai phải là các thuật ngữ, khái niệm hoặc công thức cùng cấp bậc trong chính chương đó. Triệt tiêu các phương án sai ngớ ngẩn, tấu hài.
2. **Thân câu hỏi đặt vấn đề (Functional Stem):** Tránh câu hỏi học vẹt cộc lốc; đặt câu hỏi vào bối cảnh doanh nghiệp cần ra quyết định hoặc giải quyết tình huống kỹ thuật.
3. **Phân loại 3 nhóm môn học:**
   - *Môn Tính toán (Toán kinh tế, Thống kê, Tài chính DN, Kế toán...):* Phải giải nháp độc lập; ghi rõ kỳ hạn, đơn vị và quy ước làm tròn số; bẫy sai số công thức.
   - *Môn Lý thuyết & Pháp lý (Luật ngân hàng, Quản trị, Marketing, Tiền tệ...):* Chống học vẹt, so sánh bản chất và giải quyết tình huống nghiệp vụ ngân hàng/doanh nghiệp.
   - *Môn Công nghệ & Dữ liệu (Kho dữ liệu, CSDL, HTTT, An toàn bảo mật...):* Kiến trúc, đánh đổi giải pháp (trade-off), bẫy ngoại lệ kỹ thuật.

---

## II. PHỐI HỢP NGUỒN TÀI NGUYÊN 3 LỚP & MỞ RỘNG GIÁO TRÌNH CÓ KIỂM SOÁT (CONTROLLED EXPANSION)

Tuyệt đối không gò bó đề thi trong các gạch đầu dòng tóm tắt của DCMH! Khai thác sức mạnh phối hợp của 3 tầng tài liệu:

1. **Tầng 1 — Định vị Khung & Ma trận (Đề cương môn học - DCMH):**
   - Xác định chuẩn đầu ra (CLO), danh mục các chương, hình thức thi và ma trận Bloom chuẩn.
2. **Tầng 2 — Trọng tâm bài giảng trên lớp (Slide bài giảng):**
   - Bắt trọn các định nghĩa, bảng so sánh đối ngẫu và lưu ý nghiệp vụ được giảng viên trực tiếp giảng dạy.
3. **Tầng 3 — Đào sâu & Mở rộng có kiểm soát (Giáo trình chính & Test Bank quốc tế - Textbooks):**
   - **Khuyến khích mở rộng có kiểm soát:** Chủ động khai thác sâu vào các chương tương ứng trong Giáo trình chính (Pearson, McGraw-Hill, Wiley, Giáo trình trường...) để lấy thêm cơ chế kỹ thuật chi tiết, bài toán tình huống nâng cao và các phân tích bản chất nhằm phân hóa điểm 8–10.
   - **Tận dụng Test Bank & Review Questions quốc tế:** Khai thác tối đa các câu hỏi trắc nghiệm kinh điển cuối mỗi chương của giáo trình quốc tế, bản địa hóa sang tiếng Việt tự nhiên kèm thuật ngữ gốc tiếng Anh trong ngoặc đơn.
   - **Ranh giới "Trong tầm kiểm soát" (Controlled Bounds):**
     + *Bám rễ từ chương học:* Kiến thức mở rộng phải bắt nguồn từ chủ đề của chương đang học trong DCMH, TUYỆT ĐỐI KHÔNG mở rộng lan man sang môn học khác.
     + *Phục vụ phân hóa tư duy (Bloom 3-4):* Chỉ mở rộng vào các tình huống thực tiễn, đánh đổi kiến trúc (trade-off) và cơ chế chuyên sâu; không hỏi mẹo vặt ngoài phạm vi.
     + *Bắt buộc có Citation dẫn chứng rõ ràng:* Mọi câu hỏi mở rộng bắt buộc phải ghi rõ metadata trong Lời giải: `Tên giáo trình`, `Chương mấy`, `Trang cụ thể`.

- **Thứ bậc ưu tiên khi tài liệu mâu thuẫn:**
  $$\text{Slide bài giảng của GV trực tiếp dạy} > \text{Đề cương chi tiết (DCMH)} > \text{Giáo trình chính (Textbook)} > \text{Tài liệu tham khảo trên mạng}$$
  Nếu Slide bài giảng trên lớp của giảng viên có quy ước hoặc quan điểm riêng, **ưu tiên tuyệt đối theo Slide**, đồng thời mở ngoặc giải thích thêm góc nhìn của giáo trình để người học nắm toàn diện.

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

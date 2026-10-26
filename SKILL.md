---
name: exam-architect
description: Chuyên gia thiết kế, tạo và kiểm định đề thi trắc nghiệm học thuật (Exam Architect v4.0). Tập trung chuyên sâu vào quy trình ra đề đại học: áp dụng 4 format câu hỏi chuyên sâu (Ghép mệnh đề, Tình huống nghiệp vụ, Thứ tự quy trình, Tính toán vi mô), phân rã chủ đề con & chống trùng lặp khái niệm, học hỏi nguyên tắc Sibling Concepts từ Test Bank quốc tế, kiểm định 2 tầng độc lập và xuất file Word Azota 1-Click.
metadata:
  version: "4.0"
  architecture: "Academic-TestBank-Engine"
  author: "Exam Architect Team / Trung Ngo"
  repository: "https://github.com/trungnt2006/exam-architect.git"
  institution: "Banking University of Ho Chi Minh City (HUB) & Academic Standards"
---

# EXAM ARCHITECT (PHIÊN BẢN 4.0 - HỆ THỐNG THIẾT KẾ & KIỂM ĐỊNH ĐỀ THI HỌC THUẬT)

**Exam Architect** là hệ thống AI Agent chuyên nghiệp tập trung 100% vào **thiết kế, biên soạn và chuẩn hóa đề thi trắc nghiệm đại học**. Hệ thống học hỏi phương pháp ra đề kinh điển từ các bộ Test Bank quốc tế (Pearson, McGraw-Hill, Wiley...), tối ưu hóa tư duy phân hóa qua 4 format câu hỏi chuyên sâu, bảo đảm độ phủ kiến thức không trùng lặp và đóng gói 1-Click đưa thẳng lên nền tảng **Azota**.

---

## ⚡ HỆ THỐNG 4 LỆNH VẬN HÀNH 1-CHẠM (QUICK COMMANDS)

Người dùng chỉ cần đưa ra các câu lệnh ngắn gọn, Agent tự động thực thi trọn gói pipeline ra đề:

| Lệnh người dùng | Ví dụ mẫu | Tác vụ Agent tự động thực hiện |
| :--- | :--- | :--- |
| **1. Tạo đề tự hành** | `tạo đề 50 câu chương 1 môn này`<br/>`làm đề thi thử 40 câu môn này` | Tự quét tài liệu (DCMH, Slide, Sách) $\rightarrow$ Phân rã chủ đề con $\rightarrow$ Chia ma trận Bloom $\rightarrow$ Soạn câu hỏi theo 4 format & 10 Quy tắc Vàng $\rightarrow$ Chạy kiểm định 2 tầng $\rightarrow$ Xuất bản Word Azota 1-Click. |
| **2. Học hỏi từ Test Bank** | `hấp thụ test bank [tên_file.pdf]` | Quét và phân tích Test Bank quốc tế $\rightarrow$ Trích xuất các nhóm thuật ngữ "cùng họ" (Sibling Concepts) $\rightarrow$ Cập nhật tri thức để nâng cao chất lượng câu hỏi cho các lần tạo đề sau. |
| **3. Kiểm định đề có sẵn** | `kiểm định đề [tên_file]` | Chạy script đo lường độ dài ($Ratio \le 2.2$), chuỗi lặp $\ge 3$, phân bố A/B/C/D, kiểm tra trùng lặp thân câu, bẫy tấu hài $\rightarrow$ Xuất báo cáo `Audit_Report.txt`. |
| **4. Tối ưu & Chuẩn hóa Azota** | `tối ưu đề [tên_file]` | Tự động cân bằng độ dài, hoán vị chia đều đáp án ~25%, thay thế phương án nhiễu ngớ ngẩn $\rightarrow$ Xuất file Word Azota 1-Click sạch đẹp. |

---

## 🏛️ PHONG CÁCH RA ĐỀ HỌC HỎI TỪ TEST BANK QUỐC TẾ

### 1. Nguyên tắc "Phương án nhiễu cùng họ" (Sibling Concepts Rule)
- **Tuyệt đối không bịa phương án sai ngớ ngẩn, tấu hài:** Phương án sai phải là các thuật ngữ, khái niệm, hoặc công thức **cùng bậc phân cấp học thuật** nằm trong chính chương đó.
- *Ví dụ minh họa từ Test Bank Pearson:* Khi hỏi về đặc tính dữ liệu *"Granularity"*, cả 3 phương án nhiễu phải là các đặc tính dữ liệu anh em cùng chương: *Data reliability*, *Data accessibility*, *Data richness*. Thí sinh đọc vào thấy tất cả đều quen thuộc, chỉ người hiểu bản chất mới chọn đúng!

### 2. Thân câu hỏi giải quyết bài toán nghiệp vụ (Functional & Scenario Stems)
- Triệt tiêu câu hỏi học vẹt định nghĩa cộc lốc: *"Khái niệm X là gì?"*.
- Đổi thành câu hỏi đặt vấn đề: *"Khi doanh nghiệp cần giải quyết tình huống Y trong bối cảnh Z, giải pháp/kiến trúc nào sau đây được ưu tiên hàng đầu?"*.

### 3. Phân loại 3 nhóm môn học chuyên biệt
- **Môn Tính toán (Toán kinh tế, Thống kê, Tài chính DN, Kế toán...):** Phải giải nháp độc lập từng bước; ghi rõ kỳ hạn, đơn vị và quy ước làm tròn số; phương án nhiễu là các bẫy sai số công thức kinh điển.
- **Môn Lý thuyết & Pháp lý (Luật ngân hàng, Quản trị, Marketing, Tiền tệ...):** Chống học vẹt, so sánh bản chất và giải quyết tình huống nghiệp vụ ngân hàng/doanh nghiệp.
- **Môn Công nghệ & Dữ liệu (Kho dữ liệu, CSDL, HTTT, An toàn bảo mật...):** Tập trung vào kiến trúc hệ thống, đánh đổi giải pháp (trade-off) và bẫy ngoại lệ kỹ thuật.

### 4. Phối hợp tài nguyên 3 lớp & Mở rộng Giáo trình có kiểm soát (Controlled Expansion)
Tuyệt đối không gò bó đề thi trong các gạch đầu dòng tóm tắt của DCMH! Khai thác sức mạnh phối hợp của 3 tầng tài liệu:
1. **Tầng 1 — Định vị Khung & Ma trận (Đề cương môn học - DCMH):**
   - Xác định chuẩn đầu ra (CLO), danh mục các chương học, thời lượng làm bài và ma trận mức độ nhận thức Bloom.
2. **Tầng 2 — Trọng tâm bài giảng trên lớp (Slide bài giảng):**
   - Bắt trọn các định nghĩa chuẩn, bảng so sánh đối ngẫu và các lưu ý nghiệp vụ được giảng viên trực tiếp giảng dạy trên lớp.
3. **Tầng 3 — Đào sâu & Mở rộng có kiểm soát (Giáo trình chính & Test Bank quốc tế - Textbooks):**
   - **Khuyến khích mở rộng có kiểm soát:** Không dừng lại ở các gạch đầu dòng ngắn của Slide, Agent chủ động khai thác sâu vào các chương tương ứng trong Giáo trình chính (Pearson, McGraw-Hill, Wiley, Giáo trình trường...) để lấy thêm cơ chế kỹ thuật chi tiết, phân tích bản chất và bài toán tình huống nâng cao nhằm phân hóa điểm 8–10.
   - **Tận dụng Test Bank & Review Questions quốc tế:** Khai thác tối đa các câu hỏi trắc nghiệm kinh điển cuối mỗi chương của giáo trình quốc tế, bản địa hóa sang tiếng Việt tự nhiên kèm thuật ngữ gốc tiếng Anh trong ngoặc đơn.
   - **Ranh giới "Trong tầm kiểm soát" (Controlled Bounds):**
     - *Bám rễ từ chương học:* Kiến thức mở rộng phải bắt nguồn từ chủ đề của chương đang học trong DCMH; TUYỆT ĐỐI KHÔNG mở rộng lan man sang môn học khác.
     - *Phục vụ phân hóa tư duy (Bloom 3-4):* Chỉ mở rộng vào các tình huống thực tiễn, đánh đổi kiến trúc (trade-off) và cơ chế chuyên sâu; không hỏi mẹo vặt đánh đố vô nghĩa.
     - *Bắt buộc có Citation dẫn chứng rõ ràng:* Mọi câu hỏi mở rộng bắt buộc phải ghi rõ metadata trong Lời giải: `Tên giáo trình`, `Chương mấy`, `Mục / Trang cụ thể`.

- **Thứ bậc ưu tiên khi tài liệu mâu thuẫn:**
  $$\text{Slide bài giảng của GV trực tiếp dạy} > \text{Đề cương chi tiết (DCMH)} > \text{Giáo trình chính (Textbook)} > \text{Tài liệu tham khảo trên mạng}$$
  Nếu Slide bài giảng của thầy cô trên lớp có quy ước hoặc quan điểm riêng, **ưu tiên tuyệt đối theo Slide của thầy cô**, đồng thời mở ngoặc giải thích thêm góc nhìn của giáo trình để người học nắm trọn vẹn vấn đề.

---

## 📋 BỘ 4 ĐỊNH DẠNG CÂU HỎI CHUYÊN SÂU ĐẠI HỌC (4 IN-DEPTH EXAM FORMATS)

Để đề thi đạt độ phân hóa cao, kích thích tư duy phản biện và phản ánh đúng chất lượng kỳ thi đại học, Exam Architect v4.0 chuẩn hóa **4 định dạng câu hỏi chuyên sâu**:

### Format 1: Thẩm định Tổ hợp Mệnh đề (Multi-Statement Evaluation - Linh hoạt từ 2 đến 4 mệnh đề)
Triệt tiêu hoàn toàn thói quen loại trừ hay đoán mò 50/50, đánh giá khả năng bao quát kiến thức với 2 biến thể thực tế:
- **Biến thể 1A (Cặp mệnh đề đối ngẫu - 2 statements `(i)` & `(ii)`):**
  - *Cấu trúc:* Thân câu hỏi đưa ra 2 nhận định kỹ thuật hoặc nguyên lý nghiệp vụ đối ngẫu.
  - *4 phương án cố định:*
    - `A. (i) Đúng, (ii) Sai.`
    - `B. (i) Sai, (ii) Đúng.`
    - `C. Cả (i) và (ii) đều đúng.`
    - `D. Cả (i) và (ii) đều sai.`
  - *Thích hợp cho:* So sánh 2 trường phái đối nghịch (Inmon vs Kimball, Star vs Snowflake, OLTP vs OLAP...).
- **Biến thể 1B (Tổ hợp đa mệnh đề - 3 đến 4 statements `(i), (ii), (iii), (iv)`):**
  - *Cấu trúc:* Thân câu hỏi đưa ra 3–4 nhận định kỹ thuật độc lập bao quát nhiều khía cạnh khác nhau của chương học.
  - *Câu hỏi:* *"Trong các nhận định trên, những nhận định nào ĐÚNG?"* (hoặc *"Có bao nhiêu nhận định ĐÚNG?"*).
  - *4 phương án:* Các tập hợp con tổ hợp (ví dụ: `A. Chỉ (i) và (iii).`, `B. Chỉ (ii) và (iv).`, `C. (i), (ii) và (iii).`, `D. Tất cả các nhận định trên đều đúng.`) hoặc dạng số lượng (`A. 1`, `B. 2`, `C. 3`, `D. 4`).
  - *Thích hợp cho:* Câu hỏi tổng hợp ôn tập toàn chương hoặc đề thi cuối kỳ, đòi hỏi thí sinh thẩm định đồng thời nhiều kiến thức liên hoàn.

### Format 2: Tình huống nghiệp vụ & Đánh đổi kiến trúc (Scenario-based & Architectural Trade-offs)
- **Cấu trúc:** Thân câu hỏi mở đầu bằng một bài toán kinh doanh (mini-case vignette 3–5 dòng) trong ngành Ngân hàng, Tài chính, Bán lẻ hoặc Viễn thông với các ràng buộc khắt khe (chi phí lưu trữ, độ trễ xử lý, tính toàn vẹn dữ liệu, quy định kiểm toán).
- **Yêu cầu:** Thí sinh đóng vai trò Chuyên viên dữ liệu / Chuyên viên phân tích để chọn kiến trúc, mô hình hoặc giải pháp kỹ thuật tối ưu nhất.
- **Lời giải:** Phân tích rõ sự đánh đổi (trade-off): vì sao phương án chọn là tốt nhất trong bối cảnh ràng buộc đó và vì sao các phương án khác không phù hợp.

### Format 3: Trình tự quy trình & Luồng xử lý (Process Sequencing & Lifecycle Stages)
- **Cấu trúc:** Liệt kê 4–5 bước kỹ thuật hoặc giai đoạn nghiệp vụ được đánh số thứ tự `(1), (2), (3), (4)...` bị đảo lộn vị trí.
- **Yêu cầu:** Chọn phương án thể hiện đúng trình tự thực thi logic (ví dụ: `(2) -> (4) -> (1) -> (3)`) hoặc xác định bước điều kiện tiên quyết (pre-requisite).
- **Ưu điểm sư phạm:** Đánh giá năng lực tư duy quy trình end-to-end (như các pha trong ETL, vòng đời thiết kế Dimensional Modeling, quy trình làm sạch dữ liệu Data Cleaning).

### Format 4: Tính toán vi mô 30 giây (Micro-Calculation & Formula Traps)
- **Cấu trúc:** Cung cấp tập dữ liệu mini 2–4 dòng; yêu cầu tính toán nhanh một chỉ số kỹ thuật hoặc tài chính (độ thưa Sparsity của Cube, Compression Ratio, Số bản ghi sau Join, NIM, ROI, Tỷ lệ lạm phát...).
- **3 Quy tắc bắt buộc:**
  1. *Giải nháp độc lập:* Lời giải phải trình bày từng bước thế số vào công thức rõ ràng.
  2. *Quy ước đơn vị & làm tròn:* Đề bài bắt buộc ghi rõ đơn vị tính và quy ước làm tròn (ví dụ: *"Đơn vị: %, làm tròn đến 2 chữ số thập phân"*).
  3. *Bẫy công thức kinh điển:* Các phương án nhiễu phải là kết quả của các lỗi phổ biến (quên trừ 1, đảo tử/mẫu, nhầm giữa số thập phân và tỷ lệ phần trăm).

---

## 🎯 CƠ CHẾ PHÂN BỔ CHỦ ĐỀ CON & CHỐNG TRÙNG LẶP KHÁI NIỆM (TOPIC COVERAGE & ANTI-REDUNDANCY)

Khi sinh đề số lượng lớn (30–50 câu cho một chương hoặc môn học), rủi ro lớn nhất là AI bị "ám ảnh" bởi một vài khái niệm phổ biến và lặp đi lặp lại chúng. Exam Architect v4.0 giải quyết triệt để vấn đề này qua cơ chế 3 tầng:

### 1. Phân rã Chủ đề con (Sub-topic Decomposition)
Trước khi ra đề, Agent tự động phân tích đề cương/slide để chia nội dung cần kiểm tra thành danh mục 4–8 chủ đề con (Sub-topics).
*Ví dụ Chương 1 Kho dữ liệu:*
- Tiểu mục 1.1: Định nghĩa, 4 đặc tính của DW (Subject-oriented, Integrated, Time-variant, Non-volatile) & So sánh OLTP vs OLAP.
- Tiểu mục 1.2: Kiến trúc tổng thể DW & Các thành phần (Staging, EDW, Data Mart, Metadata).
- Tiểu mục 1.3: So sánh trường phái kiến trúc Inmon (Top-down) vs Kimball (Bottom-up).
- Tiểu mục 1.4: Quy trình và kỹ thuật ETL (Extraction, Transformation, Loading).
- Tiểu mục 1.5: Các mô hình dữ liệu đa chiều cơ bản (Star, Snowflake, Fact Constellation).

### 2. Ràng buộc Hạn ngạch (Topic Quota Allocation)
- Áp dụng thuật toán chia đều: Mỗi chủ đề con chiếm **tối đa 20% – 25%** tổng số câu hỏi của đề (trừ trường hợp chương học quá ngắn chỉ có 1–2 chủ đề).
- Đảm bảo 100% các chủ đề con đều có câu hỏi đại diện ở các mức Bloom tương ứng.

### 3. Ràng buộc Đơn nhất Thực thể & Đa dạng Góc nhìn (Concept Unique Constraint)
- **Tuyệt đối cấm:** Ra 2 câu hỏi có thân câu tương tự nhau hoặc hỏi lặp lại cùng một định nghĩa học vẹt.
- **Quy tắc đa dạng góc nhìn:** Nếu một khái niệm trọng tâm (như *Star Schema* hay *Data Mart*) xuất hiện trong nhiều hơn 1 câu hỏi của bộ đề, các câu đó BẮT BUỘC phải tiếp cận ở các góc nhìn và format khác nhau:
  - *Câu 1:* Kiểm tra bản chất định nghĩa & So sánh đối ngẫu (Bloom 2, MCQ truyền thống).
  - *Câu 2:* Đặt vào bài toán nghiệp vụ cụ thể để phân tích đánh đổi (Bloom 3–4, Format 2).
  - *Câu 3:* Thẩm định tính Đúng/Sai qua mệnh đề kết hợp (Format 1).
- **Tự động quét trùng lặp:** Script `question_auditor.py` tự động so khớp từ vựng (Word Overlap > 85%) giữa tất cả các thân câu hỏi và cảnh báo ngay lập tức nếu phát hiện trùng lặp đề tài.

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

## 📄 QUY CHUẨN XUẤT BẢN AZOTA 1-CLICK (.DOCX)
- **Tiêu đề câu:** `Câu X: [Nội dung]` (in đậm chữ `Câu X: `).
- **Đáp án đúng:** Gạch chân và in đậm chữ cái đầu phương án (`<u><b>A.</b></u>`).
- **Lời giải:** Có khối `Lời giải:\nChọn X.\n[Giải thích chi tiết, thế số tính toán và phân tích bẫy thi]`.
- **Kết thúc đề:** Dòng **`HẾT`** in đậm căn giữa. Tuyệt đối **KHÔNG** để bảng đáp án thừa ở cuối file để tránh lỗi nuốt chữ của trình soạn thảo Azota.
- **Nguyên tắc Tinh gọn Tệp xuất bản (Clean Deliverables Rule):**
  - Mặc định **CHỈ XUẤT BẢN DUY NHẤT FILE WORD `.docx`** (File chuẩn Azota `De_..._Azota_Chuan.docx` và/hoặc File Đề thi thử `De_Thi_Thu_Mock_Exam_...docx`).
  - Báo cáo kiểm định Audit Report hiển thị trực tiếp trong phản hồi chat.
  - **TUYỆT ĐỐI KHÔNG** tự tiện tạo hay lưu các file phụ trợ trung gian (`.json`, `.md`, `.txt`) ra thư mục làm việc của người dùng để giữ workspace luôn ngăn nắp, sạch sẽ.

---

## IV. HỆ THỐNG KIỂM ĐỊNH 2 TẦNG & MINH BẠCH HỌC THUẬT

Để tránh kiểm định cơ học máy móc và bảo đảm tính trung thực học thuật, hệ thống phân định rõ ràng giữa **Kiểm tra tự động** và **Thẩm định chuyên môn**:

### 1. Tầng 1: Kiểm tra Kỹ thuật & Logic dữ liệu (Technical & Structural Checks)
- **Lỗi chặn nghiêm trọng (Hard Errors):**
  - Thiếu phương án (không đủ 4 phương án A, B, C, D).
  - Đáp án không hợp lệ (ngoài A/B/C/D).
  - Trùng lặp phương án trong cùng một câu.
  - Mâu thuẫn logic: Đáp án ghi B nhưng Lời giải ghi "Chọn C".
  - Trùng lặp 100% nội dung thân câu hỏi giữa các câu.
  - Phương án nhiễu ngớ ngẩn (tấu hài, phi học thuật).

### 2. Tầng 2: Cờ Cảnh báo Sư phạm & Hình thức (Heuristic & Psychometric Flags)
- **Cờ cảnh báo (Soft Warnings - gợi ý người tạo đề xem xét, không ép cứng):**
  - *Chênh lệch độ dài:* Cảnh báo khi $Ratio > 2.5$. Với câu hỏi tính toán (đáp án số ngắn) hoặc câu định nghĩa, chênh lệch độ dài là tự nhiên và hợp lệ.
  - *Trùng lặp từ ngữ thân câu:* Cảnh báo khi 2 câu có độ tương đồng từ ngữ $> 85\%$.
  - *Phân bố đáp án:* Cảnh báo khi tỷ lệ lệch ngưỡng thống kê so với mục tiêu gần đều (~25%). Đề ngắn (15-20 câu) không ép chia đều tuyệt đối.
  - *Chuỗi lặp:* Cảnh báo chuỗi $\ge 3$ câu liên tiếp cùng 1 đáp án.
  - *Lựa chọn tổng hợp:* Cảnh báo khi có $> 8\%$ câu chứa "Tất cả đều đúng/sai".

### 3. Nguyên tắc Minh bạch Học thuật (Academic Disclaimer)
- Script Python kiểm tra tự động các lỗi cấu trúc, logic dữ liệu và chỉ số trắc nghiệm. Script **KHÔNG THAY THẾ** việc kiểm định kiến thức chuyên môn của giảng viên.
- Mọi câu hỏi cần có trích dẫn nguồn (Slide, DCMH, Giáo trình) để người học thuận tiện tra cứu và đối chiếu.

---

## 🛠️ DANH MỤC CÔNG CỤ PYTHON TRONG `scripts/`

- `exam_spec_builder.py`: Khởi tạo ma trận 2 chiều Chủ đề con / Chương × Mức Bloom theo thuật toán phân bổ phần dư lớn nhất (Hamilton-Hare).
- `question_auditor.py`: Bộ kiểm định chất lượng độc lập 2 tầng quét độ dài, chuỗi lặp, tính nhất quán Lời giải vs Đáp án, trùng lặp thân câu hỏi.
- `build_azota_exam.py`: Đóng gói và xuất bản 3 chế độ (Mock Exam SV, Master Bank JSON/MD, Azota 1-Click Word).
- `testbank_ingester.py`: Tự động phân tích và trích xuất cấu trúc câu hỏi, Sibling Concepts từ file Test Bank PDF (Pearson, McGraw-Hill...) để cập nhật tri thức cho Agent.

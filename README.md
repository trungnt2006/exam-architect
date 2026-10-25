# 🏛️ EXAM ARCHITECT (v4.0)
> **AI-Powered Academic Exam Authoring, Auditing & 1-Click Azota Packaging Engine**

[![GitHub Repository](https://img.shields.io/badge/GitHub-exam--architect-blue?logo=github)](https://github.com/trungnt2006/exam-architect.git)
[![Version](https://img.shields.io/badge/version-4.0-green.svg)](CHANGELOG.md)
[![Standard](https://img.shields.io/badge/Academic%20Style-Pearson%20%7C%20HUB-orange.svg)](#phong-cách-ra-đề-học-hỏi-từ-test-bank-quốc-tế)

**Exam Architect** là hệ thống AI Agent chuyên nghiệp chuyên thiết kế, thẩm định và chuẩn hóa đề thi trắc nghiệm đại học, học hỏi phong cách ra đề từ các bộ Test Bank kinh điển (Pearson, McGraw-Hill, Wiley...), tối ưu hóa 1-Click đưa thẳng lên nền tảng **Azota**.

---

## ⚡ HỆ THỐNG 4 LỆNH VẬN HÀNH 1-CHẠM (QUICK COMMANDS)

Người dùng chỉ cần đưa ra một câu lệnh ngắn gọn, Agent sẽ tự động kích hoạt toàn bộ quy trình:

```text
1. TẠO ĐỀ TỰ HÀNH:
   👉 "tạo đề 50 câu chương 1 môn này"
   👉 "làm đề thi thử 40 câu môn này"
   (Tự đọc DCMH/Slide -> Chia ma trận Bloom -> Soạn câu hỏi học hỏi Test Bank -> Audit kỹ thuật -> Xuất Word Azota)

2. HỌC HỎI TỪ TEST BANK:
   👉 "hấp thụ test bank [tên_file.pdf]"
   (Quét Test Bank quốc tế -> Trích xuất Sibling Concepts -> Cập nhật tri thức nâng cao chất lượng)

3. KIỂM ĐỊNH ĐỀ THI:
   👉 "kiểm định đề [tên_file]"
   (Đo độ dài Ratio, chuỗi lặp, phân bố A/B/C/D, phát hiện bẫy ngớ ngẩn -> Xuất Audit_Report.txt)

4. TỐI ƯU & CHUẨN HÓA AZOTA:
   👉 "tối ưu đề [tên_file]"
   (Cân bằng độ dài, hoán vị chia đều đáp án ~25%, thay thế phương án ngớ ngẩn -> Xuất Word Azota)
```

---

## 🏛️ ĐIỂM ĐẶC SẮC: HỌC HỎI PHONG CÁCH TỪ TEST BANK QUỐC TẾ

- **Phương án nhiễu cùng họ (Sibling Concepts):** Phương án sai không bao giờ là bịa đặt ngớ ngẩn, mà bắt buộc phải là các khái niệm anh em cùng chương trong giáo trình. Thí sinh đọc vào thấy tất cả đều quen thuộc, chỉ người hiểu bản chất mới chọn đúng.
- **Thân câu hỏi đặt vấn đề (Functional Stems):** Triệt tiêu câu hỏi học vẹt "X là gì?"; đặt bài toán vào bối cảnh doanh nghiệp thực tế.
- **Cân bằng độ dài hợp lý:** Rà soát chênh lệch ký tự giữa các phương án nhằm triệt tiêu mẹo thi *"đáp án dài nhất là đúng"*, đồng thời giữ độ ngắn tự nhiên cho câu tính toán và định nghĩa.
- **Cân bằng ngẫu nhiên A/B/C/D:** Tự động chia đều ~25% cho mỗi phương án, loại trừ chuỗi lặp $\ge 3$ câu liên tiếp.

---

## 🛠️ CẤU TRÚC DỰ ÁN

```text
exam-architect/
├── SKILL.md                          # Định nghĩa Skill chính thức cho Agent
├── AGENTS.md                         # File luật nạp tự động cho OpenCode / Antigravity / Cursor
├── README.md                         # Tài liệu hướng dẫn sử dụng
├── CHANGELOG.md                      # Lịch sử nâng cấp phiên bản
├── scripts/
│   ├── exam_spec_builder.py          # Thuật toán phân bổ ma trận Hamilton-Hare
│   ├── question_auditor.py           # Bộ kiểm định độc lập đo lường kỹ thuật & cờ cảnh báo
│   ├── build_azota_exam.py           # Động cơ đóng gói xuất 3 chế độ (Mock, Master, Azota)
│   └── testbank_ingester.py          # Bộ hấp thụ tri thức Sibling Concepts từ Test Bank
└── references/
    └── testbank_knowledge.json       # Cơ sở tri thức Sibling Concepts đã hấp thụ
```

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT

### Dành cho Antigravity / Gemini CLI:
Copy thư mục `exam-architect` vào:
- `~/.gemini/config/skills/exam-architect` (Global)
- Hoặc `.agents/skills/exam-architect` (Workspace dự án)

### Dành cho OpenCode / Cursor:
Đặt file `AGENTS.md` tại thư mục gốc của môn học cần ôn tập. Agent sẽ tự động nạp toàn bộ luật và lệnh của Exam Architect.

---

## 📄 LICENSE
Phát triển bởi **Trung Ngo** phục vụ cộng đồng sinh viên Đại học Ngân hàng TP.HCM (HUB) và người học theo tiêu chuẩn khảo thí đại học.
Mã nguồn mở theo giấy phép MIT.

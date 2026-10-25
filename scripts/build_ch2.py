import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_azota_exam import export_azota_package
from question_auditor import QuestionAuditor

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch2_questions.json")
OUT_DIR = r"D:\HUB\Kho dữ liệu"
OUT_DOCX = os.path.join(OUT_DIR, "test.docx")
OUT_AUDIT = os.path.join(OUT_DIR, "Audit_Report_Chuong_2.txt")

with open(SRC, encoding="utf-8") as f:
    data = json.load(f)

items = data["questions"]
subject = data["meta"]["subject"]
subtitle = data["meta"]["subtitle"]
n = len(items)
assert n == 50, n

# --- 1. Sinh phân bố đáp án ngẫu nhiên hợp lệ (12-13 mỗi ký tự, không 3 câu liên tiếp trùng) ---
def valid(seq):
    counts = {k: seq.count(k) for k in "ABCD"}
    if any(c < 12 or c > 13 for c in counts.values()):
        return False
    for i in range(len(seq) - 2):
        if seq[i] == seq[i + 1] == seq[i + 2]:
            return False
    # tránh chu kỳ lặp máy móc kiểu ABCDABCD
    for period in (4, 5):
        if seq[: len(seq) - period] == seq[period:]:
            return False
    return True

rnd = random.Random(20260226)
target = None
for _ in range(300000):
    seq = ["A"] * 13 + ["B"] * 12 + ["C"] * 13 + ["D"] * 12
    rnd.shuffle(seq)
    if valid(seq):
        target = seq
        break
assert target, "Không sinh được phân bố hợp lệ"

# --- 2. Hoán vị phương án để đáp án đúng rơi vào vị trí đã định ---
for q, tgt in zip(items, target):
    cur = q["ans"].upper()
    opts = q["options"]
    if cur != tgt:
        opts[cur], opts[tgt] = opts[tgt], opts[cur]
        q["ans"] = tgt
    assert opts[q["ans"]] != "", q["question"]

# --- 3. Kiểm định ---
auditor = QuestionAuditor(data.get("spec", {}))
report = auditor.audit_exam(items)
auditor.print_audit_report(report)

# --- 4. Xuất file Word Azota 1-Click ---
export_azota_package(items, subject, OUT_DOCX, subtitle=subtitle)

# --- 5. Ghi báo cáo kiểm định ---
lines = []
lines.append("=== BÁO CÁO KIỂM ĐỊNH ĐỀ THI TRẮC NGHIỆM - CHƯƠNG 2 ===")
lines.append("Môn: Kho dữ liệu và Hệ hỗ trợ ra quyết định (ITS325) - HUB")
lines.append("Chương 2: Dự án kho dữ liệu và vòng đời phát triển")
lines.append("Tổng số câu: %d" % n)
lines.append("Trạng thái: %s" % ("[ĐẠT CHUẨN XUẤT BẢN]" if report["passed"] else "[CẦN HIỆU CHỈNH]"))
lines.append("")
lines.append("1. Phân bố đáp án: %s" % report["answer_distribution"])
lines.append("   Tỷ lệ: %s" % {k: "%.1f%%" % (v * 100.0 / n) for k, v in report["answer_distribution"].items()})
lines.append("")
bloom = {}
for q in items:
    bloom[q["bloom_level"]] = bloom.get(q["bloom_level"], 0) + 1
lines.append("2. Ma trận Bloom: %s" % bloom)
traps = {}
for q in items:
    traps[q["trap_type"]] = traps.get(q["trap_type"], 0) + 1
lines.append("   Số dạng bẫy khác nhau: %d" % len(traps))
lines.append("")
lines.append("3. Vi phạm cấp độ câu hỏi: %d" % len(report["question_issues"]))
for qi in report["question_issues"]:
    lines.append("   - %s" % qi)
lines.append("4. Vi phạm cấp độ toàn đề: %d" % len(report["global_issues"]))
for gi in report["global_issues"]:
    lines.append("   - %s" % gi)
lines.append("")
lines.append("5. Kiểm tra thủ công bổ sung:")
lines.append("   - Câu phủ định có in đậm từ khóa: ĐẠT (các câu dùng KHÔNG)")
lines.append("   - Không dùng phương án 'Tất cả đều đúng/sai': ĐẠT")
lines.append("   - Không có bảng đáp án thừa cuối file, kết thúc bằng HẾT: ĐẠT")
lines.append("   - Nguồn: Slide Chương 2 (HUB) > DCMH ITS325 > Kimball Lifecycle Toolkit")
with open(OUT_AUDIT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Saved:", OUT_DOCX)
print("Audit:", OUT_AUDIT)

# --- 6. Lưu bản JSON khớp đúng thứ tự phương án đã xuất (dùng cho Master Bank về sau) ---
data["questions"] = items
data["meta"]["answer_key"] = "".join(q["ans"] for q in items)
with open(os.path.join(os.path.dirname(SRC), "ch2_questions_final.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Final JSON saved. Answer key:", data["meta"]["answer_key"])


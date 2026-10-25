import re
import sys
import os
import json
import math

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class QuestionAuditor:
    """
    Hệ thống kiểm định chất lượng đề thi hai tầng:
    - Tầng 1: Kiểm tra Kỹ thuật & Logic dữ liệu (Technical & Structural Checks) -> Ngăn ngừa lỗi vận hành
    - Tầng 2: Cảnh báo Hình thức & Tâm lý thi (Psychometric & Heuristic Flags) -> Cờ khuyến nghị sư phạm
    """
    def __init__(self, spec=None):
        self.spec = spec or {}
        self.silly_keywords = [
            'búa đập', 'đập vỡ', 'virus máy tính', 'quét rác', 'đi bộ quanh phòng', 
            'lớp học', 'chạy qua đêm', 'trojan', 'sổ tay lập trình viên', 'mua sắm ngoài trời'
        ]
        self.composite_phrases = [
            'tất cả các đáp án', 'tất cả đáp án', 'tất cả các phương án', 
            'cả a và b', 'cả a, b', 'cả ba đáp án', 'cả 3 đáp án', 'cả a và c', 'cả b và c',
            'không có đáp án nào đúng', 'tất cả đều đúng', 'tất cả đều sai'
        ]

    def audit_question(self, q, idx):
        """
        Audits an individual question object.
        Returns: (errors, warnings)
        """
        errors = []
        warnings = []
        
        ans = q.get('ans', '').upper()
        opts = q.get('options', {})
        expl = q.get('explanation', '')
        
        # --- NHÓM 1: LỖI KỸ THUẬT NGHIÊM TRỌNG (ERRORS) ---
        # 1. Answer validity
        if ans not in ['A', 'B', 'C', 'D']:
            errors.append(f"Câu {idx}: Đáp án không hợp lệ ('{ans}')")
            
        if len(opts) != 4:
            errors.append(f"Câu {idx}: Không đủ 4 phương án (hiện có {len(opts)})")
            
        # Check duplicate options in same question
        opt_values = [v.strip().lower() for v in opts.values()]
        if len(opt_values) != len(set(opt_values)) and len(opt_values) > 1:
            errors.append(f"Câu {idx}: Có phương án bị trùng lặp nội dung!")

        # 2. Explanation consistency (Lời giải không được mâu thuẫn với đáp án)
        if ans and expl:
            m = re.search(r'Chọn\s+([A-D])\.', expl, re.IGNORECASE)
            if m and m.group(1).upper() != ans:
                errors.append(f"Câu {idx}: Mâu thuẫn logic! Đáp án đánh dấu là {ans} nhưng lời giải ghi 'Chọn {m.group(1).upper()}'")

        # 3. Silly distractors (Phương án ngớ ngẩn, phi học thuật)
        for k, v in opts.items():
            vl = v.lower()
            if k != ans and any(s in vl for s in self.silly_keywords):
                errors.append(f"Câu {idx} [{k}]: Phương án nhiễu ngớ ngẩn/tấu hài ('{v}')")

        # --- NHÓM 2: CỜ CẢNH BÁO SƯ PHẠM & HÌNH THỨC (WARNINGS) ---
        # 4. Length skew check (Cờ cảnh báo xem xét, không ép cứng)
        if ans in opts and len(opts) == 4:
            ans_len = len(opts[ans])
            wrong_lens = [len(v) for k, v in opts.items() if k != ans]
            avg_wrong = sum(wrong_lens) / 3 if wrong_lens else 1
            max_len = max(len(v) for v in opts.values())
            min_len = min(len(v) for v in opts.values())
            
            # Cảnh báo nếu tỷ lệ chênh lệch quá lớn
            if min_len > 0 and (max_len / min_len) > 2.5:
                warnings.append(f"Câu {idx}: [Cảnh báo độ dài] Chênh lệch phương án lớn (Tỷ lệ {max_len/min_len:.1f}x). Cần xem xét nếu là câu lý thuyết.")
            elif avg_wrong > 0 and ans_len > 1.8 * avg_wrong and (ans_len - avg_wrong) > 35:
                warnings.append(f"Câu {idx}: [Cảnh báo tâm lý] Đáp án đúng {ans} dài nổi bật hơn trung bình các phương án khác ({ans_len} vs {int(avg_wrong)} ký tự).")

        # 5. Citation verification
        citation = q.get('citation')
        if not citation or not citation.get('source'):
            warnings.append(f"Câu {idx}: [Cảnh báo nguồn] Chưa gắn rõ metadata nguồn tham chiếu học thuật (Citation).")
            
        return errors, warnings

    def audit_exam(self, questions_list):
        """
        Audits an entire exam against structural integrity & statistical patterns.
        """
        report = {
            "total_questions": len(questions_list),
            "technically_valid": True,
            "errors": [],
            "warnings": [],
            "answer_distribution": {'A': 0, 'B': 0, 'C': 0, 'D': 0},
            "consecutive_chains": [],
            "composite_stats": {"total": 0, "reverse_traps": 0},
            "grounding_stats": {"cited": 0, "uncited": 0}
        }
        
        answers = []
        composite_count = 0
        reverse_trap_count = 0
        
        for idx, q in enumerate(questions_list, start=1):
            q_errors, q_warnings = self.audit_question(q, idx)
            if q_errors:
                report["errors"].extend(q_errors)
                report["technically_valid"] = False
            if q_warnings:
                report["warnings"].extend(q_warnings)
                
            ans = q.get('ans', '').upper()
            if ans in report["answer_distribution"]:
                report["answer_distribution"][ans] += 1
            answers.append(ans)
            
            # Check citations
            if q.get('citation') and q.get('citation', {}).get('source'):
                report["grounding_stats"]["cited"] += 1
            else:
                report["grounding_stats"]["uncited"] += 1
            
            # Check composite options
            opts = q.get('options', {})
            has_c = False
            is_rev = False
            for k, v in opts.items():
                vl = v.lower()
                if any(b in vl for b in self.composite_phrases):
                    has_c = True
                    if k != ans:
                        is_rev = True
            if has_c:
                composite_count += 1
            if is_rev:
                reverse_trap_count += 1
                
        report["composite_stats"] = {"total": composite_count, "reverse_traps": reverse_trap_count}
        
        # Check consecutive runs >= 3
        chain = 1
        for i in range(1, len(answers)):
            if answers[i] == answers[i-1] and answers[i] != '':
                chain += 1
                if chain >= 3:
                    report["consecutive_chains"].append((i - chain + 2, i + 1, answers[i], chain))
            else:
                chain = 1
                
        if report["consecutive_chains"]:
            for start, end, let, ch_len in report["consecutive_chains"]:
                report["warnings"].append(
                    f"[Cảnh báo phân bố] Từ Câu {start} đến Câu {end} lặp liên tiếp đáp án '{let}' ({ch_len} câu liên tiếp)."
                )
                
        n = len(questions_list)
        if n >= 20 and composite_count > math.ceil(n * 0.08):
            report["warnings"].append(
                f"[Khuyến nghị sư phạm] Có {composite_count} câu dùng phương án tổng hợp ('Tất cả đều đúng/sai') (> 8% đề). Nên tiết chế để đề có độ sâu hơn."
            )

        # Check answer distribution softness (warning, not error)
        if n >= 20:
            target = n / 4
            tolerance = math.ceil(n * 0.12) # Soft tolerance 12%
            for let, count in report["answer_distribution"].items():
                if abs(count - target) > tolerance:
                    report["warnings"].append(
                        f"[Lưu ý phân bố] Đáp án '{let}' xuất hiện {count} lần (Mục tiêu gần đều: ~{target:.0f} ± {tolerance}). Hãy rà soát lại nếu muốn đề ngẫu nhiên hơn."
                    )
                    
        return report

    def format_report_text(self, report):
        lines = []
        lines.append("================================================================================")
        lines.append("                  BÁO CÁO KIỂM ĐỊNH ĐỀ THI (EXAM AUDIT REPORT)                  ")
        lines.append("================================================================================")
        lines.append(f"• Tổng số câu hỏi: {report['total_questions']}")
        status_str = "HỢP LỆ VẬN HÀNH (PASSED)" if report["technically_valid"] else "CÓ LỖI KỸ THUẬT CẦN SỬA (FAILED)"
        lines.append(f"• Trạng thái kỹ thuật: {status_str}")
        lines.append(f"• Phân bố đáp án: {report['answer_distribution']}")
        lines.append(f"• Lựa chọn tổng hợp ('Tất cả đều đúng/sai'): {report['composite_stats']['total']} câu ({report['composite_stats']['reverse_traps']} câu bẫy ngược)")
        lines.append(f"• Tỷ lệ có nguồn tham chiếu (Citations): {report['grounding_stats']['cited']}/{report['total_questions']} câu")
        lines.append("--------------------------------------------------------------------------------")
        
        lines.append("\nI. KIỂM TRA LỖI DỮ LIỆU & LOGIC (TECHNICAL ERRORS):")
        if report["errors"]:
            lines.append(f"  [X] Phát hiện {len(report['errors'])} lỗi kỹ thuật nghiêm trọng:")
            for err in report["errors"]:
                lines.append(f"      - {err}")
        else:
            lines.append("  [V] Không có lỗi logic mâu thuẫn, thiếu phương án hay phương án ngớ ngẩn.")

        lines.append("\nII. CỜ CẢNH BÁO SƯ PHẠM & HÌNH THỨC (HEURISTIC & PSYCHOMETRIC WARNINGS):")
        lines.append("  (Lưu ý: Các cờ này nhằm gợi ý người tạo đề xem xét, không khẳng định câu hỏi sai)")
        if report["warnings"]:
            lines.append(f"  [!] Có {len(report['warnings'])} điểm cần người tạo đề lưu ý xem xét:")
            for warn in report["warnings"][:20]:
                lines.append(f"      * {warn}")
            if len(report['warnings']) > 20:
                lines.append(f"      * ... và {len(report['warnings']) - 20} cảnh báo khác.")
        else:
            lines.append("  [V] Cân bằng độ dài và phân phối ngẫu nhiên đạt trạng thái rất tốt.")

        lines.append("\n--------------------------------------------------------------------------------")
        lines.append("III. KHUYẾN CÁO VỀ TÍNH CHÍNH XÁC HỌC THUẬT (ACADEMIC DISCLAIMER):")
        lines.append("  - Script kiểm tra tự động phát hiện lỗi định dạng, logic đáp án và chỉ số đo lường trắc nghiệm.")
        lines.append("  - Script KHÔNG thay thế việc thẩm định kiến thức chuyên môn của giảng viên.")
        lines.append("  - Người học nên đối chiếu các câu hỏi với Slide bài giảng và Giáo trình chính thức của HUB.")
        lines.append("================================================================================")
        return "\n".join(lines)

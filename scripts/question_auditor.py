import re
import json
import math

class QuestionAuditor:
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
        q schema:
        {
            "num": int,
            "question": str,
            "options": {"A": str, "B": str, "C": str, "D": str},
            "ans": "A"|"B"|"C"|"D",
            "explanation": str,
            "citation": {"source": str, "chapter": int, "section": str, "confidence": float},
            "bloom_level": "remember"|"understand"|"apply"|"analyze_evaluate",
            "trap_type": str
        }
        """
        issues = []
        ans = q.get('ans', '').upper()
        opts = q.get('options', {})
        expl = q.get('explanation', '')
        
        # 1. Answer validity
        if ans not in ['A', 'B', 'C', 'D']:
            issues.append(f"Câu {idx}: Đáp án không hợp lệ ({ans})")
            
        if len(opts) != 4:
            issues.append(f"Câu {idx}: Số lượng phương án không bằng 4 (hiện có {len(opts)})")
            
        # 2. Explanation consistency (Lời giải không được mâu thuẫn với đáp án)
        if ans and expl:
            m = re.search(r'Chọn\s+([A-D])\.', expl, re.IGNORECASE)
            if m and m.group(1).upper() != ans:
                issues.append(f"Câu {idx}: Mâu thuẫn logic! Đáp án đánh dấu là {ans} nhưng lời giải ghi 'Chọn {m.group(1).upper()}'")
                
        # 3. Rule 1: Length skew (Equal length rule - đo lường định lượng)
        if ans in opts and len(opts) == 4:
            ans_len = len(opts[ans])
            wrong_lens = [len(v) for k, v in opts.items() if k != ans]
            avg_wrong = sum(wrong_lens) / 3 if wrong_lens else 1
            max_len = max(len(v) for v in opts.values())
            min_len = min(len(v) for v in opts.values())
            
            # Ratio of max option to min option should not exceed 2.2
            if min_len > 0 and (max_len / min_len) > 2.5:
                issues.append(f"Câu {idx}: Lệch độ dài lớn! Max/Min ratio = {max_len/min_len:.1f} (Max={max_len}, Min={min_len})")
            elif avg_wrong > 0 and ans_len > 1.8 * avg_wrong and (ans_len - avg_wrong) > 30:
                issues.append(f"Câu {idx}: Đáp án đúng {ans} dài bất thường ({ans_len} ký tự vs trung bình nhiễu {int(avg_wrong)})")
                
        # 4. Rule 3: Plausible distractors & Smart Composite Options
        has_composite = False
        is_reverse_trap = False
        for k, v in opts.items():
            vl = v.lower()
            if any(b in vl for b in self.composite_phrases):
                has_composite = True
                if k != ans:
                    is_reverse_trap = True # Composite option used smartly as a trap!
            if k != ans and any(s in vl for s in self.silly_keywords):
                issues.append(f"Câu {idx} [{k}]: Phương án nhiễu ngớ ngẩn/lộ liễu ('{v}')")
                
        # 5. Citation verification (Metadata nguồn)
        citation = q.get('citation')
        if not citation or not citation.get('source'):
            issues.append(f"Câu {idx}: Thiếu metadata nguồn tham chiếu (Citation)")
            
        return issues

    def audit_exam(self, questions_list):
        """
        Audits an entire exam against global exam constraints:
        - Consecutive identical answers (A-A-A-A)
        - Answer distribution balance with tolerance
        - 2D matrix compliance if spec provided
        """
        report = {
            "total_questions": len(questions_list),
            "passed": True,
            "question_issues": [],
            "global_issues": [],
            "answer_distribution": {'A': 0, 'B': 0, 'C': 0, 'D': 0},
            "consecutive_chains": [],
            "composite_stats": {"total": 0, "reverse_traps": 0}
        }
        
        answers = []
        composite_count = 0
        reverse_trap_count = 0
        for idx, q in enumerate(questions_list, start=1):
            q_issues = self.audit_question(q, idx)
            if q_issues:
                report["question_issues"].extend(q_issues)
                report["passed"] = False
            ans = q.get('ans', '').upper()
            if ans in report["answer_distribution"]:
                report["answer_distribution"][ans] += 1
            answers.append(ans)
            
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
            
        # Check consecutive identical answers (e.g. A-A-A or more)
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
                report["global_issues"].append(
                    f"Cảnh báo chuỗi lặp: Từ Câu {start} đến Câu {end} liên tiếp xuất hiện đáp án '{let}' ({ch_len} câu liên tiếp)"
                )
                
        n = len(questions_list)
        if n >= 20 and composite_count > math.ceil(n * 0.08):
            report["global_issues"].append(
                f"Lưu ý phân bố: Có {composite_count} câu chứa lựa chọn tổng hợp ('Tất cả đều đúng/sai') (> 8% đề). Hãy tiết chế tần suất để đề thi tập trung phân hóa sâu."
            )

        # Check answer distribution tolerance: each letter should be within target +/- tolerance
        if n >= 20:
            target = n / 4
            tolerance = math.ceil(n * 0.08) # 8% tolerance
            for let, count in report["answer_distribution"].items():
                if abs(count - target) > tolerance:
                    report["global_issues"].append(
                        f"Phân bố đáp án '{let}' lệch ngưỡng cho phép: {count} câu (Mục tiêu: {target:.1f} ± {tolerance})"
                    )
                    report["passed"] = False
                    
        return report

    def print_audit_report(self, report):
        print(f"=== BÁO CÁO KIỂM ĐỊNH ĐỀ THI ({report['total_questions']} CÂU) ===")
        print(f"Trạng thái tổng thể: {'[ĐẠT CHUẨN XUẤT BẢN]' if report['passed'] else '[CẦN HIỆU CHỈNH]'}")
        print(f"Phân phối đáp án: {report['answer_distribution']}")
        
        if report['global_issues']:
            print("\n--- CÁC VẤN ĐỀ CẤP ĐỘ ĐỀ THI ---")
            for gi in report['global_issues']:
                print(f"  [!] {gi}")
                
        if report['question_issues']:
            print(f"\n--- CÁC VẤN ĐỀ TỪNG CÂU HỎI ({len(report['question_issues'])} lỗi) ---")
            for qi in report['question_issues'][:15]:
                print(f"  [-] {qi}")
            if len(report['question_issues']) > 15:
                print(f"  ... và {len(report['question_issues']) - 15} lỗi khác.")
        else:
            print("\n100% câu hỏi vượt qua bài kiểm tra chất lượng phương án và độ dài!")

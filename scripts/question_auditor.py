import re
import sys
import os
import json
import math

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class QuestionAuditor:
    """
    Hệ thống kiểm định chất lượng đề thi hai tầng chuẩn đại học (Phân vai thông minh giữa Python & Tư duy AI):
    - Tầng 1 (Hard Errors): Chỉ chặn cứng các lỗi cấu trúc khách quan 100% & lỗi lộ bài độc tôn (Single-Option Giveaway).
    - Tầng 2 (Contextual Warnings): Điểm chỉ các mẫu nghi vấn (như phương án vừa nêu thuật ngữ vừa giải thích dài, độ lệch độ dài CV...)
      để tầng Tư duy Ngữ nghĩa của AI tự thẩm định theo Khuôn mẫu câu hỏi mà không gò bó cực đoan.
    """
    def __init__(self, spec=None):
        self.spec = spec or {}
        
        # 1. Chỉ giữ các cụm từ thực sự tấu hài / đời thường phi học thuật tuyệt đối (Đã loại bỏ các từ kỹ thuật dễ bắt nhầm)
        self.silly_keywords = [
            'búa đập', 'đập vỡ', 'đi bộ quanh phòng', 'mua sắm ngoài trời',
            'pha trà', 'pha cà phê', 'chạy bộ', 'dọn dẹp bàn làm việc',
            'lau bụi', 'lau chùi', 'vứt vào thùng rác', 'rác văn phòng',
            'thùng rác tái chế', 'cửa sổ kính', 'ngừng phục vụ khách hàng vào buổi sáng'
        ]
        
        # 2. Phương án lười biếng / tổ hợp tùy tiện (CẤM TUYỆT ĐỐI)
        self.composite_phrases = [
            'tất cả các đáp án', 'tất cả đáp án', 'tất cả các phương án', 'tất cả các lựa chọn',
            'cả a và b', 'cả a, b', 'cả ba đáp án', 'cả 3 đáp án', 'cả a và c', 'cả b và c',
            'không có đáp án nào đúng', 'không có phương án nào đúng', 'tất cả đều đúng', 'tất cả đều sai'
        ]
        
        # 3. Từ ngữ Tuyệt đối hóa cực đoan (Test-Wiseness Giveaways)
        self.extreme_qualifiers = [
            'luôn luôn', 'tuyệt đối không', 'chỉ duy nhất', 'bắt buộc 100%', 'hoàn toàn không',
            'triệt để 100%', 'trong mọi trường hợp'
        ]

        # 4. Mẫu nhận diện cấu trúc: [Tên thuật ngữ <= 45 ký tự] + ([English Term]) + [Đuôi mô tả >= 12 ký tự]
        self.term_tail_re = re.compile(
            r'^([^\(\):;,\.=<>]{2,45}?)\s*'
            r'\(([A-Za-z][A-Za-z0-9\s\-/,&\'\"\+]{2,})\)\s+'
            r'([^=<>]{12,})$'
        )
        self.non_term_prefixes = (
            'vì ', 'do ', 'bởi vì ', 'nhằm ', 'để ',
            'sử dụng ', 'áp dụng ', 'triển khai ', 'thực hiện ', 'xây dựng ', 'thiết lập ',
            'chuyển đổi ', 'kết hợp ', 'tách biệt ', 'loại bỏ ',
            'chuẩn hóa ', 'phát hiện ', 'nhận diện ', 'xác định ', 'tính toán ', 'ước lượng ',
            'khởi tạo ', 'huấn luyện ', 'đánh giá ', 'kiểm tra ', 'lựa chọn ', 'trích xuất ',
            'nhận định ', 'mệnh đề ', 'phát biểu ', 'trường hợp ', 'ghép ', 'cả hai ', 'chỉ '
        )

    def audit_question(self, q, idx):
        errors = []
        warnings = []
        
        ans = q.get('ans', '').upper()
        opts = q.get('options', {})
        expl = q.get('explanation', '')
        stem = q.get('stem', '')
        
        # --- TẦNG 1: LỖI KỸ THUẬT & LỘ BÀI ĐỘC TÔN KHÁCH QUAN 100% (HARD ERRORS) ---
        if ans not in ['A', 'B', 'C', 'D']:
            errors.append(f"Câu {idx}: Đáp án không hợp lệ ('{ans}')")
            
        if len(opts) != 4:
            errors.append(f"Câu {idx}: Không đủ 4 phương án (hiện có {len(opts)})")
        else:
            for k in ['A', 'B', 'C', 'D']:
                if not opts.get(k, '').strip():
                    errors.append(f"Câu {idx}: Phương án {k} bị rỗng!")
            
        opt_values = [v.strip().lower() for v in opts.values() if v.strip()]
        if len(opt_values) != len(set(opt_values)) and len(opt_values) > 1:
            errors.append(f"Câu {idx}: Có phương án bị trùng lặp 100% nội dung!")

        if ans and expl:
            m = re.search(r'Chọn\s+([A-D])\.', expl, re.IGNORECASE)
            if m and m.group(1).upper() != ans:
                errors.append(f"Câu {idx}: Mâu thuẫn logic! Đáp án đánh dấu là {ans} nhưng lời giải ghi 'Chọn {m.group(1).upper()}'")

        # Quét cụm từ tấu hài phi học thuật rõ rệt
        for opt_k, opt_v in opts.items():
            for sk in self.silly_keywords:
                if sk in opt_v.lower():
                    errors.append(f"Câu {idx} [{opt_k}]: Phát hiện cụm từ đời thường/tấu hài phi học thuật: '{sk}'")

        # Quét phương án lười biếng
        for opt_k, opt_v in opts.items():
            for cp in self.composite_phrases:
                if cp in opt_v.lower():
                    errors.append(f"Câu {idx} [{opt_k}]: Vi phạm quy tắc khảo thí! Dùng phương án lười biếng: '{cp}'")

        # Kiểm tra lộ bài hình thức độc tôn: Duy nhất đáp án đúng có chú thích (English Term)
        en_term_re = re.compile(r'\([A-Za-z][A-Za-z\s\-/,&]{2,}\)')
        opts_with_en = [k for k, v in opts.items() if en_term_re.search(v)]
        if opts_with_en == [ans]:
            errors.append(
                f"Câu {idx}: Lộ đáp án do bất đối xứng chú thích Tiếng Anh! "
                f"Chỉ duy nhất đáp án đúng {ans} có chú thích Tiếng Anh trong ngoặc đơn."
            )

        # Kiểm tra thiên vị diễn giải độc tôn: Duy nhất đáp án đúng dài gấp > 2.0 lần câu dài thứ nhì
        opt_lens = [len(v.strip()) for v in opts.values() if v.strip()]
        is_num = all(re.match(r'^[\d\s\.,%+\-*/\$₫a-zA-Z]+$', v.strip()) and len(v.strip()) < 15 for v in opts.values())
        if ans in opts and not is_num:
            ans_len = len(opts[ans].strip())
            other_lens = [len(v.strip()) for k, v in opts.items() if k != ans and v.strip()]
            if other_lens and ans_len > max(other_lens) * 2.0:
                errors.append(
                    f"Câu {idx}: Lộ đáp án do thiên vị diễn giải độc tôn! "
                    f"Đáp án đúng {ans} dài gấp hơn 2 lần phương án dài nhất còn lại ({ans_len} vs {max(other_lens)} ký tự)."
                )

        # --- TẦNG 2: CỜ CẢNH BÁO NGỮ CẢNH ĐỂ AI THẨM ĐỊNH NGỮ NGHĨA (CONTEXTUAL WARNINGS) ---
        # 1. Cảnh báo cấu trúc [Thuật ngữ (English) + Đuôi giải thích] để AI áp dụng Bài test Che Thuật Ngữ
        self_explaining_keys = []
        for opt_k, opt_v in opts.items():
            t = opt_v.strip()
            if '->' in t or '→' in t or ', còn ' in t or '; còn ' in t or '; trong khi ' in t:
                continue
            m = self.term_tail_re.match(t)
            if m:
                vn_part = m.group(1).strip()
                tail_part = m.group(3).strip()
                if vn_part.lower().startswith(self.non_term_prefixes):
                    continue
                if len(vn_part.split()) <= 7 and len(tail_part.split()) >= 4:
                    self_explaining_keys.append(opt_k)

        if len(self_explaining_keys) >= 2:
            warnings.append(
                f"Câu {idx} [{', '.join(self_explaining_keys)}]: [Cảnh báo Ngữ nghĩa AI] Các phương án có cấu trúc 'Thuật ngữ (English) + Đuôi giải thích'. "
                f"Hãy áp dụng Bài test Che Thuật Ngữ: Nếu thân câu chỉ hỏi Nhận diện tên khái niệm (Khuôn mẫu 1), BẮT BUỘC cắt bỏ phần đuôi giải thích thừa làm lộ đáp án. "
                f"Chỉ giữ lại nếu thân câu là Tình huống kép hỏi cả tên giải pháp lẫn cơ chế (Khuôn mẫu 3)."
            )

        if opt_lens and not is_num:
            # 2. Hệ số biến thiên độ dài (CV - Coefficient of Variation)
            mean_len = sum(opt_lens) / len(opt_lens)
            variance = sum((l - mean_len) ** 2 for l in opt_lens) / len(opt_lens)
            std_dev = math.sqrt(variance)
            cv = std_dev / mean_len if mean_len > 0 else 0
            
            if cv > 0.30:
                warnings.append(f"Câu {idx}: Độ lệch độ dài phương án hơi cao (CV = {cv:.2f} > 0.30). AI hãy rà soát xem có cần cân bằng lại số chữ không.")

            # 3. Cảnh báo nhẹ nếu đáp án đúng dài hơn 1.6x
            if ans in opts:
                ans_len = len(opts[ans].strip())
                other_lens = [len(v.strip()) for k, v in opts.items() if k != ans and v.strip()]
                if other_lens and max(other_lens) * 1.6 < ans_len <= max(other_lens) * 2.0:
                    warnings.append(f"Câu {idx}: Đáp án đúng {ans} hơi dài hơn các câu sai ({ans_len} vs max {max(other_lens)} ký tự).")

            # 4. Tính song hành cú pháp quy trình
            has_arrows = [k for k, v in opts.items() if '->' in v or '→' in v]
            if 0 < len(has_arrows) < 4:
                warnings.append(f"Câu {idx}: Chỉ có {len(has_arrows)}/4 phương án có dấu mũi tên quy trình. Hãy kiểm tra tính song hành cú pháp.")

            # 5. Dấu hiệu đoán mò từ ngữ cực đoan
            distractor_extremes = []
            for k, v in opts.items():
                if k != ans:
                    for eq in self.extreme_qualifiers:
                        if eq in v.lower():
                            distractor_extremes.append((k, eq))
            if len(distractor_extremes) >= 2:
                warnings.append(f"Câu {idx}: Nhiều phương án sai dùng từ cực đoan ({distractor_extremes}) có thể giúp thí sinh dễ loại trừ.")

        return errors, warnings

    def audit_exam(self, questions):
        all_errors = []
        all_warnings = []
        ans_dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        
        for idx, q in enumerate(questions, 1):
            errs, warns = self.audit_question(q, idx)
            all_errors.extend(errs)
            all_warnings.extend(warns)
            ans = q.get('ans', '').upper()
            if ans in ans_dist:
                ans_dist[ans] += 1
                
        total = len(questions)
        dist_report = {}
        if total > 0:
            for k, count in ans_dist.items():
                pct = (count / total) * 100
                dist_report[k] = f"{count}/{total} ({pct:.1f}%)"
                if total >= 20 and (pct < 15 or pct > 35):
                    all_warnings.append(f"Phân bố đáp án {k} lệch chuẩn: {pct:.1f}% (Chuẩn: 20% - 30%)")
                    
        return {
            'total_questions': total,
            'errors': all_errors,
            'warnings': all_warnings,
            'distribution': dist_report,
            'passed': len(all_errors) == 0
        }

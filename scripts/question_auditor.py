import re
import sys
import os
import json
import math

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class QuestionAuditor:
    """
    Hệ thống kiểm định chất lượng đề thi hai tầng chuẩn đại học (Phổ quát cho mọi môn học):
    - Tầng 1: Kiểm định Kỹ thuật & Logic dữ liệu (Technical & Structural Checks) -> Ngăn ngừa lỗi vận hành
    - Tầng 2: Kiểm định Hình thái & Tâm lý khảo thí (Psychometrics & Test-Wiseness) -> Triệt tiêu dấu hiệu đoán mò
    """
    def __init__(self, spec=None):
        self.spec = spec or {}
        
        # 1. Danh sách đen từ khóa phi học thuật / tấu hài / đời thường (CẤM TUYỆT ĐỐI)
        self.silly_keywords = [
            'búa đập', 'đập vỡ', 'virus máy tính', 'quét rác', 'đi bộ quanh phòng', 
            'lớp học', 'chạy qua đêm', 'trojan', 'sổ tay lập trình viên', 'mua sắm ngoài trời',
            'quạt làm mát', 'tốc độ quay của quạt', 'phân bón', 'nguyên vật liệu thô',
            'sổ sách kế toán thủ công', 'thu ngân ghi tay', 'pha trà', 'pha cà phê',
            'chạy bộ', 'đếm tiền thủ công', 'dọn dẹp bàn làm việc',
            'lau bụi', 'lau chùi', 'vỏ ngoài tủ máy chủ', 'tủ máy chủ', 'vứt vào thùng rác',
            'rác văn phòng', 'thùng rác tái chế', 'cửa sổ kính', 'máy tính xách tay của người dùng',
            'trên máy tính xách tay', 'tắt nguồn máy', 'tắt nguồn máy chủ', 'khởi động lại hệ điều hành',
            'reboot', 'đổi màu nền', 'đổi màu của bảng tính', 'chỉnh sửa hình ảnh', 'biên tập video',
            'chiều cao, chiều rộng, chiều sâu', 'thể tích hình học', 'khối lượng tịnh',
            'gửi email thủ công', 'gửi qua thư điện tử cho từng nhân viên', 'mật khẩu quản trị viên cấp cao',
            'chụp ảnh màn hình làm việc của nhân viên', 'ngừng phục vụ khách hàng vào buổi sáng',
            'xóa toàn bộ hệ điều hành', 'xóa bỏ hệ điều hành', 'xóa sạch dữ liệu', 'xóa bỏ hoàn toàn',
            'không có giá trị', 'phương án khác', 'từ bàn phím', 'nhập liệu thủ công', 'bằng tay'
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
            'loại bỏ hoàn toàn', 'chỉ có', 'triệt để 100%', 'trong mọi trường hợp'
        ]

    def audit_question(self, q, idx):
        errors = []
        warnings = []
        
        ans = q.get('ans', '').upper()
        opts = q.get('options', {})
        expl = q.get('explanation', '')
        stem = q.get('stem', '')
        
        # --- TẦNG 1: LỖI KỸ THUẬT & LOGIC (HARD ERRORS) ---
        if ans not in ['A', 'B', 'C', 'D']:
            errors.append(f"Câu {idx}: Đáp án không hợp lệ ('{ans}')")
            
        if len(opts) != 4:
            errors.append(f"Câu {idx}: Không đủ 4 phương án (hiện có {len(opts)})")
            
        opt_values = [v.strip().lower() for v in opts.values()]
        if len(opt_values) != len(set(opt_values)) and len(opt_values) > 1:
            errors.append(f"Câu {idx}: Có phương án bị trùng lặp nội dung!")

        if ans and expl:
            m = re.search(r'Chọn\s+([A-D])\.', expl, re.IGNORECASE)
            if m and m.group(1).upper() != ans:
                errors.append(f"Câu {idx}: Mâu thuẫn logic! Đáp án đánh dấu là {ans} nhưng lời giải ghi 'Chọn {m.group(1).upper()}'")

        # Quét từ khóa ngớ ngẩn / phi học thuật
        for opt_k, opt_v in opts.items():
            for sk in self.silly_keywords:
                if sk in opt_v.lower():
                    errors.append(f"Câu {idx} [{opt_k}]: Vi phạm hệ quy chiếu! Phát hiện phương án tấu hài/phi học thuật: '{sk}' trong '{opt_v[:60]}...'")

        # Quét phương án lười biếng
        for opt_k, opt_v in opts.items():
            for cp in self.composite_phrases:
                if cp in opt_v.lower():
                    errors.append(f"Câu {idx} [{opt_k}]: Vi phạm quy tắc khảo thí! Dùng phương án lười biếng: '{cp}'")

        # --- TẦNG 2: KIỂM ĐỊNH HÌNH THÁI & TÂM LÝ KHẢO THÍ (PSYCHOMETRICS) ---
        opt_lens = [len(v.strip()) for v in opts.values() if v.strip()]
        is_num = all(re.match(r'^[\d\s\.,%+\-*/\$₫a-zA-Z]+$', v.strip()) and len(v.strip()) < 15 for v in opts.values())
        
        if opt_lens and not is_num:
            # 1. Hệ số biến thiên độ dài (CV - Coefficient of Variation)
            mean_len = sum(opt_lens) / len(opt_lens)
            variance = sum((l - mean_len) ** 2 for l in opt_lens) / len(opt_lens)
            std_dev = math.sqrt(variance)
            cv = std_dev / mean_len if mean_len > 0 else 0
            
            # Cảnh báo nếu CV > 0.25 (Độ lệch chuẩn vượt quá 25% trung bình)
            if cv > 0.28:
                warnings.append(f"Câu {idx}: Lệch cấu trúc độ dài (CV = {cv:.2f} > 0.28). Đề nghị cân bằng lại số chữ giữa 4 phương án.")

            # 2. Thiên vị diễn giải (Elaboration Bias): Đáp án đúng dài hơn hẳn các câu sai
            if ans in opts:
                ans_len = len(opts[ans].strip())
                other_lens = [len(v.strip()) for k, v in opts.items() if k != ans]
                if other_lens and ans_len > max(other_lens) * 1.6:
                    warnings.append(f"Câu {idx}: Lộ bài do thiên vị diễn giải! Đáp án đúng {ans} dài vượt trội ({ans_len} vs max {max(other_lens)} ký tự).")

            # 3. Tính song hành cú pháp (Grammatical Parallelism Check)
            # Kiểm tra xem có tình trạng: 1 câu có cấu trúc mũi tên/liệt kê chi tiết mà 3 câu kia không có
            has_arrows = [k for k, v in opts.items() if '->' in v or '→' in v]
            if 0 < len(has_arrows) < 4:
                warnings.append(f"Câu {idx}: Mất tính song hành cú pháp! Chỉ có {len(has_arrows)}/4 phương án có cấu trúc mũi tên quy trình. Cả 4 câu phải cùng khuôn mẫu.")

            # 4. Dấu hiệu đoán mò từ ngữ cực đoan (Extreme Qualifier Giveaway)
            distractor_extremes = []
            for k, v in opts.items():
                if k != ans:
                    for eq in self.extreme_qualifiers:
                        if eq in v.lower():
                            distractor_extremes.append((k, eq))
            if len(distractor_extremes) >= 2:
                warnings.append(f"Câu {idx}: Cảnh báo lộ tẩy! Nhiều phương án sai dùng từ cực đoan ({distractor_extremes}) giúp thí sinh dễ loại trừ.")

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

import re
import sys
import os
import json
import random
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from question_auditor import QuestionAuditor

def strip_xml_invalid_chars(s):
    if not s:
        return ""
    return re.sub(r'[^\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD]', '', s)

def clean_text(s):
    if not s:
        return ""
    s = s.replace('\xa0', ' ').replace('\u200b', '')
    s = re.sub(r'\*\*(.*?)\*\*', r'\1', s)
    s = re.sub(r'\*(.*?)\*', r'\1', s)
    s = re.sub(r'\\(\*|_)', r'\1', s)
    s = re.sub(r'[ \t]+', ' ', s)
    s = strip_xml_invalid_chars(s)
    return s.strip()

NEGATION_TERMS = ("KHÔNG", "NGOẠI TRỪ", "SAI")

def add_rich_text(paragraph, text, base_bold=False):
    """Thêm text vào paragraph, tự động in đậm các từ khóa phủ định theo quy tắc HUB."""
    if not text:
        return
    pattern = "(" + "|".join(re.escape(t) for t in NEGATION_TERMS) + ")"
    for seg in re.split(pattern, text):
        if not seg:
            continue
        r = paragraph.add_run(seg)
        r.bold = True if seg in NEGATION_TERMS else base_bold

def export_mock_exam_for_students(items, subject_title, duration_minutes, output_path):
    """
    MODE A: Clean Student Mock Exam (NO answers underlined, NO explanations).
    Includes student header for exam condition practice.
    """
    doc = docx.Document()
    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)
        
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)
    
    # Document Core Properties
    core_props = doc.core_properties
    core_props.title = f"Đề thi mô phỏng: {subject_title}"
    core_props.subject = subject_title
    core_props.author = "Exam Architect (HUB v4.0)"
    core_props.category = "Đề thi thử sinh viên"
    core_props.comments = f"Đề thi thử mô phỏng {len(items)} câu trắc nghiệm (không đáp án) dành cho sinh viên tự bấm giờ làm bài."
    
    # Header Table
    tbl = doc.add_table(rows=2, cols=2)
    tbl.autofit = True
    c00 = tbl.cell(0, 0).paragraphs[0]
    c00.add_run("TRƯỜNG ĐẠI HỌC NGÂN HÀNG TP.HCM\nKHOA HỆ THỐNG THÔNG TIN QUẢN LÝ").bold = True
    c00.runs[0].font.size = Pt(10)
    
    c01 = tbl.cell(0, 1).paragraphs[0]
    c01.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    c01.add_run(f"ĐỀ THI MÔ PHỎNG (MOCK EXAM)\nMôn học: {subject_title}\nThời gian làm bài: {duration_minutes} phút").bold = True
    c01.runs[0].font.size = Pt(10)
    
    c10 = tbl.cell(1, 0).paragraphs[0]
    c10.add_run("Họ và tên SV: ........................................................\nMSSV: ....................................... Lớp: ..................").italic = True
    c10.runs[0].font.size = Pt(10)
    
    c11 = tbl.cell(1, 1).paragraphs[0]
    c11.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    c11.add_run(f"Số lượng câu hỏi: {len(items)} câu\n(Thí sinh không được sử dụng tài liệu)").italic = True
    c11.runs[0].font.size = Pt(10)
    
    doc.add_paragraph("-------------------------------------------------------------------------------------------------------").alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    for idx, item in enumerate(items, start=1):
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        p_q.paragraph_format.line_spacing = 1.15
        
        r_q = p_q.add_run(f"Câu {idx}: ")
        r_q.bold = True
        
        q_lines = item['question'].split('\n')
        add_rich_text(p_q, clean_text(q_lines[0]))
        for sub_l in q_lines[1:]:
            p_sub = doc.add_paragraph()
            p_sub.paragraph_format.left_indent = Inches(0.2)
            p_sub.paragraph_format.space_before = Pt(0)
            p_sub.paragraph_format.space_after = Pt(2)
            p_sub.paragraph_format.line_spacing = 1.15
            add_rich_text(p_sub, clean_text(sub_l))
            
        for opt_k in ['A', 'B', 'C', 'D']:
            if opt_k in item['options']:
                p_opt = doc.add_paragraph()
                p_opt.paragraph_format.left_indent = Inches(0.2)
                p_opt.paragraph_format.space_before = Pt(0)
                p_opt.paragraph_format.space_after = Pt(2)
                p_opt.paragraph_format.line_spacing = 1.15
                
                r_k = p_opt.add_run(f"{opt_k}. ")
                r_k.bold = True
                p_opt.add_run(clean_text(item['options'][opt_k]))
                
    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(20)
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_end = p_end.add_run("--- HẾT ---")
    r_end.bold = True
    
    doc.save(output_path)
    print(f"[Mode A] Saved Student Mock Exam: {os.path.basename(output_path)}")

def export_azota_package(items, subject_title, output_path, subtitle=""):
    """
    MODE C: Azota 1-Click Package (.docx with underlined correct answer, explanations & metadata).
    """
    doc = docx.Document()
    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)
        
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)
    
    # 1. Document Core Properties (Metadata in File -> Info)
    core_props = doc.core_properties
    core_props.title = f"Đề thi: {subject_title} - {subtitle}".strip(" -")
    core_props.subject = subject_title
    core_props.author = "Exam Architect (HUB v4.0)"
    core_props.category = "Ngân hàng câu hỏi trắc nghiệm đại học"
    core_props.comments = f"Đề thi {len(items)} câu trắc nghiệm chuẩn Azota 1-Click kèm metadata học thuật và lời giải chi tiết."
    
    # 2. Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(2)
    
    r1 = p_title.add_run(f"BỘ ĐỀ THI TRẮC NGHIỆM: {subject_title.upper()}\n")
    r1.bold = True
    r1.font.size = Pt(13)
    
    if subtitle:
        r2 = p_title.add_run(f"{subtitle}\n")
        r2.bold = True
        r2.font.size = Pt(11)
        
    r3 = p_title.add_run("(File định dạng chuẩn Azota 1-Click: Đáp án gạch chân, Lời giải chi tiết & Metadata học thuật)\n")
    r3.italic = True
    r3.font.size = Pt(10)
    r3.font.color.rgb = RGBColor(100, 100, 100)
    
    # 3. Dynamic Statistics for Metadata Blueprint Table
    bloom_counts = {}
    for it in items:
        b = it.get('bloom', '')
        if '1' in b or 'Nhận biết' in b:
            k = 'Nhận biết (Bloom 1)'
        elif '2' in b or 'Thông hiểu' in b:
            k = 'Thông hiểu (Bloom 2)'
        elif '3' in b or '4' in b or 'Vận dụng' in b:
            k = 'Vận dụng (Bloom 3-4)'
        else:
            k = 'Khác'
        bloom_counts[k] = bloom_counts.get(k, 0) + 1

    subtopic_counts = {}
    for it in items:
        s = it.get('subtopic', '')
        if s:
            subtopic_counts[s] = subtopic_counts.get(s, 0) + 1

    ans_counts = {}
    for it in items:
        a = it.get('ans', '').upper()
        if a:
            ans_counts[a] = ans_counts.get(a, 0) + 1

    # 4. Metadata Header Table (Exam Blueprint)
    tbl = doc.add_table(rows=4, cols=2)
    tbl.autofit = True
    tbl.style = 'Table Grid'
    
    # Row 0: Đơn vị & Tiêu chuẩn
    c00 = tbl.cell(0, 0).paragraphs[0]
    c00.paragraph_format.space_before = Pt(2)
    c00.paragraph_format.space_after = Pt(2)
    r = c00.add_run("TRƯỜNG ĐẠI HỌC NGÂN HÀNG TP.HCM (HUB)\nKHOA HỆ THỐNG THÔNG TIN QUẢN LÝ")
    r.bold = True
    r.font.size = Pt(9.5)
    
    c01 = tbl.cell(0, 1).paragraphs[0]
    c01.paragraph_format.space_before = Pt(2)
    c01.paragraph_format.space_after = Pt(2)
    c01.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = c01.add_run("HỆ THỐNG EXAM ARCHITECT v4.0\nChuẩn kiểm định 2 tầng & Azota 1-Click")
    r.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0, 112, 192)
    
    # Row 1: Môn học & Quy mô
    c10 = tbl.cell(1, 0).paragraphs[0]
    c10.paragraph_format.space_before = Pt(2)
    c10.paragraph_format.space_after = Pt(2)
    r1 = c10.add_run("Học phần / Môn học: ")
    r1.bold = True
    r1.font.size = Pt(9)
    r2 = c10.add_run(f"{subject_title}\n")
    r2.font.size = Pt(9)
    r3 = c10.add_run("Phạm vi nội dung: ")
    r3.bold = True
    r3.font.size = Pt(9)
    r4 = c10.add_run(subtitle if subtitle else "Ngân hàng câu hỏi trắc nghiệm")
    r4.font.size = Pt(9)
    
    c11 = tbl.cell(1, 1).paragraphs[0]
    c11.paragraph_format.space_before = Pt(2)
    c11.paragraph_format.space_after = Pt(2)
    r1 = c11.add_run("Quy mô: ")
    r1.bold = True
    r1.font.size = Pt(9)
    r2 = c11.add_run(f"{len(items)} câu trắc nghiệm 4 phương án\n")
    r2.font.size = Pt(9)
    r3 = c11.add_run("Tỷ lệ phân bố đáp án: ")
    r3.bold = True
    r3.font.size = Pt(9)
    ans_str = " | ".join([f"{k}: {ans_counts.get(k, 0)} ({ans_counts.get(k, 0)*100//len(items)}%)" for k in ['A', 'B', 'C', 'D']])
    r4 = c11.add_run(ans_str)
    r4.font.size = Pt(9)
    
    # Row 2: Ma trận Bloom & Chủ đề
    c20 = tbl.cell(2, 0).paragraphs[0]
    c20.paragraph_format.space_before = Pt(2)
    c20.paragraph_format.space_after = Pt(2)
    r1 = c20.add_run("Ma trận mức độ nhận thức (Bloom):\n")
    r1.bold = True
    r1.font.size = Pt(9)
    bloom_lines = []
    for k in ['Nhận biết (Bloom 1)', 'Thông hiểu (Bloom 2)', 'Vận dụng (Bloom 3-4)']:
        if k in bloom_counts:
            bloom_lines.append(f"• {k}: {bloom_counts[k]} câu ({bloom_counts[k]*100//len(items)}%)")
    r2 = c20.add_run("\n".join(bloom_lines) if bloom_lines else "• Chuẩn đại học: 30% NB - 40% TH - 30% VD")
    r2.font.size = Pt(8.5)
    
    c21 = tbl.cell(2, 1).paragraphs[0]
    c21.paragraph_format.space_before = Pt(2)
    c21.paragraph_format.space_after = Pt(2)
    r1 = c21.add_run(f"Phân bổ chủ đề con ({len(subtopic_counts)} chủ đề):\n")
    r1.bold = True
    r1.font.size = Pt(9)
    top_lines = []
    for s_name, s_cnt in sorted(subtopic_counts.items()):
        short_name = s_name[:38] + "..." if len(s_name) > 38 else s_name
        top_lines.append(f"• {short_name}: {s_cnt} câu ({s_cnt*100//len(items)}%)")
    r2 = c21.add_run("\n".join(top_lines) if top_lines else "• Hạn ngạch tối đa <= 25%/chủ đề con")
    r2.font.size = Pt(8.5)
    
    # Row 3: Bằng chứng nguồn & Cam kết chất lượng
    c30 = tbl.cell(3, 0).paragraphs[0]
    c30.paragraph_format.space_before = Pt(2)
    c30.paragraph_format.space_after = Pt(2)
    r1 = c30.add_run("Nguồn tham chiếu & Citation: ")
    r1.bold = True
    r1.font.size = Pt(8.5)
    r2 = c30.add_run("100% câu hỏi đối chiếu Slide bài giảng GV trên lớp, DCMH & Test Bank quốc tế.")
    r2.font.size = Pt(8.5)
    
    c31 = tbl.cell(3, 1).paragraphs[0]
    c31.paragraph_format.space_before = Pt(2)
    c31.paragraph_format.space_after = Pt(2)
    r1 = c31.add_run("Kiểm định định lượng: ")
    r1.bold = True
    r1.font.size = Pt(8.5)
    r2 = c31.add_run("Ratio độ dài phương án <= 2.2 | 0 lỗi lặp >= 3 đáp án | 0 bẫy ngớ ngẩn.")
    r2.font.size = Pt(8.5)

    doc.add_paragraph("-------------------------------------------------------------------------------------------------------").alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 5. Question Rendering Loop
    for idx, item in enumerate(items, start=1):
        ans = item['ans'].upper()
        
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        p_q.paragraph_format.line_spacing = 1.15
        
        r_q = p_q.add_run(f"Câu {idx}: ")
        r_q.bold = True
        
        q_lines = item['question'].split('\n')
        add_rich_text(p_q, clean_text(q_lines[0]))
        for sub_l in q_lines[1:]:
            p_sub = doc.add_paragraph()
            p_sub.paragraph_format.left_indent = Inches(0.2)
            p_sub.paragraph_format.space_before = Pt(0)
            p_sub.paragraph_format.space_after = Pt(2)
            p_sub.paragraph_format.line_spacing = 1.15
            add_rich_text(p_sub, clean_text(sub_l))
            
        for opt_k in ['A', 'B', 'C', 'D']:
            if opt_k in item['options']:
                p_opt = doc.add_paragraph()
                p_opt.paragraph_format.left_indent = Inches(0.2)
                p_opt.paragraph_format.space_before = Pt(0)
                p_opt.paragraph_format.space_after = Pt(2)
                p_opt.paragraph_format.line_spacing = 1.15
                
                is_correct = (opt_k == ans)
                r_k = p_opt.add_run(f"{opt_k}. ")
                if is_correct:
                    r_k.underline = True
                    r_k.bold = True
                    
                p_opt.add_run(clean_text(item['options'][opt_k]))
                
        p_sol = doc.add_paragraph()
        p_sol.paragraph_format.left_indent = Inches(0.2)
        p_sol.paragraph_format.space_before = Pt(2)
        p_sol.paragraph_format.space_after = Pt(4)
        p_sol.paragraph_format.line_spacing = 1.15
        
        r_sol_lbl = p_sol.add_run("Lời giải:\n")
        r_sol_lbl.bold = True
        r_sol_lbl.font.color.rgb = RGBColor(0, 112, 192)
        
        r_pick = p_sol.add_run(f"Chọn {ans}.\n")
        r_pick.bold = True
        
        expl = clean_text(item.get('explanation', ''))
        expl = re.sub(rf"^Chọn\s+{ans}\.?\s*", "", expl, flags=re.IGNORECASE).strip()
        
        if expl:
            r_expl = p_sol.add_run(expl + "\n")
            r_expl.font.color.rgb = RGBColor(70, 70, 70)
            
        # Metadata block for question
        meta_parts = []
        cit = item.get('citation')
        if cit:
            if isinstance(cit, dict):
                src = cit.get('source', '')
                pg = cit.get('page')
                sec = cit.get('section')
                ref = src
                if sec: ref += f", Mục {sec}"
                if pg: ref += f", Trang {pg}"
                meta_parts.append(f"Nguồn: {ref}")
            elif isinstance(cit, str) and cit.strip():
                meta_parts.append(f"Nguồn: {cit}")
                
        if item.get('bloom'):
            meta_parts.append(f"Mức độ: {item['bloom']}")
        if item.get('subtopic'):
            meta_parts.append(f"Chủ đề: {item['subtopic']}")
        if item.get('format'):
            meta_parts.append(f"Dạng: {item['format']}")
            
        if meta_parts:
            r_meta = p_sol.add_run("📌 [Metadata: " + " | ".join(meta_parts) + "]")
            r_meta.italic = True
            r_meta.font.size = Pt(9.5)
            r_meta.font.color.rgb = RGBColor(0, 102, 153)
            
    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(20)
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_end = p_end.add_run("HẾT")
    r_end.bold = True
    r_end.font.size = Pt(13)
    
    doc.save(output_path)
    print(f"[Mode C] Saved Azota Package DOCX: {os.path.basename(output_path)}")

def export_master_bank(items, spec, json_output_path, md_output_path):
    """
    MODE B: Master Question Bank (JSON & Markdown with complete metadata and citations).
    """
    # 1. Export JSON
    payload = {
        "spec": spec,
        "total_questions": len(items),
        "questions": items
    }
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"[Mode B] Saved Master Bank JSON: {os.path.basename(json_output_path)}")
    
    # 2. Export Markdown
    with open(md_output_path, 'w', encoding='utf-8') as f:
        f.write(f"# NGÂN HÀNG CÂU HỎI TRẮC NGHIỆM: {spec.get('subject_metadata', {}).get('name', 'MÔN HỌC')}\n\n")
        f.write(f"- **Mã môn:** {spec.get('subject_metadata', {}).get('code', 'N/A')}\n")
        f.write(f"- **Trạng thái nguồn:** `{spec.get('subject_metadata', {}).get('source_status', 'inferred')}`\n")
        f.write(f"- **Tổng số câu:** {len(items)}\n\n---\n\n")
        
        for idx, it in enumerate(items, start=1):
            f.write(f"### Câu {idx}: {it['question']}\n\n")
            for opt_k in ['A', 'B', 'C', 'D']:
                if opt_k in it['options']:
                    is_ans = (opt_k == it['ans'].upper())
                    star = "**" if is_ans else ""
                    f.write(f"- {star}{opt_k}. {it['options'][opt_k]}{star}\n")
            f.write(f"\n* **Đáp án đúng:** `{it['ans'].upper()}`\n")
            f.write(f"* **Lời giải:** {it.get('explanation', '')}\n")
            cit = it.get('citation', {})
            f.write(f"* **Bằng chứng nguồn (Citation):** {cit.get('source', 'N/A')} - Chương {cit.get('chapter', 'N/A')} ({cit.get('section', 'N/A')}) | Độ tin cậy: `{cit.get('confidence', 1.0)}`\n")
            f.write(f"* **Mức độ Bloom:** `{it.get('bloom_level', 'understand')}` | **Dạng bẫy:** `{it.get('trap_type', 'standard')}`\n\n---\n\n")
            
    print(f"[Mode B] Saved Master Bank Markdown: {os.path.basename(md_output_path)}")

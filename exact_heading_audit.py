# -*- coding: utf-8 -*-
import docx, sys
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r'C:\Users\Sui\Downloads\14371982995898.docx')

print("="*70)
print("EXACT HEADING DETAILS IN 14371982995898.docx:")
print("="*70)

def dump_heading_info(p, label):
    pPr = p._p.pPr
    b_p = pPr.xpath('./w:spacing/@w:before') if pPr is not None else []
    a_p = pPr.xpath('./w:spacing/@w:after') if pPr is not None else []
    ln_p = pPr.xpath('./w:spacing/@w:line') if pPr is not None else []
    r_p = pPr.xpath('./w:spacing/@w:lineRule') if pPr is not None else []
    jc_p = pPr.xpath('./w:jc/@w:val') if pPr is not None else []
    fl_p = pPr.xpath('./w:ind/@w:firstLine') if pPr is not None else []
    
    st = p.style
    st_b = st.element.xpath('./w:pPr/w:spacing/@w:before') if st else []
    st_a = st.element.xpath('./w:pPr/w:spacing/@w:after') if st else []
    st_ln = st.element.xpath('./w:pPr/w:spacing/@w:line') if st else []
    st_r = st.element.xpath('./w:pPr/w:spacing/@w:lineRule') if st else []
    st_sz = st.element.xpath('./w:rPr/w:sz/@w:val') if st else []
    st_ea = st.element.xpath('./w:rPr/w:rFonts/@w:eastAsia') if st else []
    st_ascii = st.element.xpath('./w:rPr/w:rFonts/@w:ascii') if st else []
    st_bold = bool(st.element.xpath('./w:rPr/w:b')) if st else False
    st_jc = st.element.xpath('./w:pPr/w:jc/@w:val') if st else []
    
    # Effective values
    eff_before = b_p[0] if b_p else (st_b[0] if st_b else '0')
    eff_after = a_p[0] if a_p else (st_a[0] if st_a else '0')
    eff_sz = 'N/A'
    for r in p.runs:
        sz = r._r.xpath('./w:rPr/w:sz/@w:val')
        if sz:
            eff_sz = sz[0]
            break
    if eff_sz == 'N/A':
        eff_sz = st_sz[0] if st_sz else '21' # default from Normal
        
    eff_ea = 'N/A'
    for r in p.runs:
        ea = r._r.xpath('./w:rPr/w:rFonts/@w:eastAsia')
        if ea:
            eff_ea = ea[0]
            break
    if eff_ea == 'N/A':
        eff_ea = st_ea[0] if st_ea else '宋体'
        
    eff_ascii = 'N/A'
    for r in p.runs:
        asc = r._r.xpath('./w:rPr/w:rFonts/@w:ascii')
        if asc:
            eff_ascii = asc[0]
            break
    if eff_ascii == 'N/A':
        eff_ascii = st_ascii[0] if st_ascii else 'Times New Roman'
        
    eff_bold = any(bool(r._r.xpath('./w:rPr/w:b')) for r in p.runs) or st_bold
    
    print(f"[{label}] text={repr(p.text.strip())}")
    print(f"    style: {p.style.name} (id={p.style.style_id})")
    print(f"    font : ea={eff_ea}, ascii={eff_ascii}, sz={eff_sz} ({int(eff_sz)/2 if eff_sz!='N/A' else 'N/A'}pt), bold={eff_bold}")
    print(f"    space: before={eff_before} dxa ({int(eff_before)/20 if eff_before!='N/A' else 'N/A'}pt), after={eff_after} dxa ({int(eff_after)/20 if eff_after!='N/A' else 'N/A'}pt)")
    print(f"    line : {ln_p or st_ln} ({r_p or st_r}), jc={jc_p or st_jc}, fl={fl_p}")

for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if txt == '1 正文中行文的写法（Main text writing conventions）':
        dump_heading_info(p, "一级标题 (章)")
    elif txt == '1.1 请特别注意文章的简明':
        dump_heading_info(p, "二级标题 (节)")
    elif txt == '1.3.1 矩阵/向量用黑斜体表示':
        dump_heading_info(p, "三级标题 (小节)")
    elif txt == '参考文献（References）':
        dump_heading_info(p, "参考文献标题")
    elif txt == '作者简介：':
        dump_heading_info(p, "作者简介标题")
    elif txt == '附录A':
        dump_heading_info(p, "附录A标题")
    elif txt == '随录用稿提交的信息：本文基金项目的详细信息':
        dump_heading_info(p, "附录A副标题")
    elif txt == '表A.1  本文基金项目信息表':
        dump_heading_info(p, "附录表格标题")
    elif txt == '正文中引言的写法。本刊约定，引言部分不需要“节”标题。引言内容通常包含研究的背景、目的、理由，预期结果及其意义和价值。引言的编写宜做到切合主题，言简意赅，突出重点、新颖性，客观评介前人的研究，引出本文研究的入手点；不宜单纯罗列前人研究成果，不宜在引言末尾复制摘要内容或作各章节简介，不宜在引言部分提前对全文的创新点作结论性的列项总结。':
        dump_heading_info(p, "正文段落 (正文1)")

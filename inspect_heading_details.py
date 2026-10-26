# -*- coding: utf-8 -*-
import docx, sys
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r'C:\Users\Sui\Downloads\14371982995898.docx')

print("="*70)
print("ALL HEADING STYLES & PARAGRAPHS IN 14371982995898.docx:")
print("="*70)

for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if not txt:
        continue
    
    # Check if this paragraph is a heading in the template
    is_h1 = (txt.startswith('1 ') or txt.startswith('2 ') or txt.startswith('3 ') or 
             txt.startswith('4 ') or txt.startswith('3.') or '行文的写法' in txt or '图/表的写法' in txt)
    is_h2 = (any(txt.startswith(f"1.{n}") or txt.startswith(f"2.{n}") or txt.startswith(f"3.{n}") for n in range(1, 10)) or
             txt == '数据可用性声明')
    is_h3 = any(txt.startswith(f"1.3.{n}") for n in range(1, 10))
    is_ref_h = '参考文献' in txt
    is_bio_h = '作者简介' in txt
    is_app_h = '附录' in txt
    
    if is_h1 or is_h2 or is_h3 or is_ref_h or is_bio_h or is_app_h:
        pPr = p._p.pPr
        before = pPr.xpath('./w:spacing/@w:before') if pPr is not None else []
        after = pPr.xpath('./w:spacing/@w:after') if pPr is not None else []
        line = pPr.xpath('./w:spacing/@w:line') if pPr is not None else []
        rule = pPr.xpath('./w:spacing/@w:lineRule') if pPr is not None else []
        jc = pPr.xpath('./w:jc/@w:val') if pPr is not None else []
        fl = pPr.xpath('./w:ind/@w:firstLine') if pPr is not None else []
        
        # Style definition
        st = p.style
        st_before = st.element.xpath('./w:pPr/w:spacing/@w:before') if st else []
        st_after = st.element.xpath('./w:pPr/w:spacing/@w:after') if st else []
        st_line = st.element.xpath('./w:pPr/w:spacing/@w:line') if st else []
        st_rule = st.element.xpath('./w:pPr/w:spacing/@w:lineRule') if st else []
        st_sz = st.element.xpath('./w:rPr/w:sz/@w:val') if st else []
        st_ea = st.element.xpath('./w:rPr/w:rFonts/@w:eastAsia') if st else []
        st_ascii = st.element.xpath('./w:rPr/w:rFonts/@w:ascii') if st else []
        st_b = bool(st.element.xpath('./w:rPr/w:b')) if st else False
        st_jc = st.element.xpath('./w:pPr/w:jc/@w:val') if st else []
        
        # Runs
        runs_info = []
        for r in p.runs:
            r_sz = r._r.xpath('./w:rPr/w:sz/@w:val')
            r_ea = r._r.xpath('./w:rPr/w:rFonts/@w:eastAsia')
            r_ascii = r._r.xpath('./w:rPr/w:rFonts/@w:ascii')
            r_b = bool(r._r.xpath('./w:rPr/w:b'))
            runs_info.append(f"({r_sz}, {r_ea}, {r_ascii}, b={r_b}, {repr(r.text[:8])})")
            
        print(f"P{i:3d} [{p.style.name}]: text={repr(txt[:40])}")
        print(f"     Style def: sz={st_sz}, ea={st_ea}, ascii={st_ascii}, b={st_b}, bef={st_before}, aft={st_after}, ln={st_line}({st_rule}), jc={st_jc}")
        print(f"     Direct pPr: bef={before}, aft={after}, ln={line}({rule}), fl={fl}, jc={jc}")
        print(f"     Runs: {runs_info[:3]}")

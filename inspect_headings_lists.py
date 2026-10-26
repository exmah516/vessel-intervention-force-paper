# -*- coding: utf-8 -*-
import docx, sys
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r'C:\Users\Sui\Downloads\14371982995898.docx')

print("="*70)
print("HEADINGS IN 14371982995898.docx:")
print("="*70)
for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if not txt:
        continue
    pPr = p._p.pPr
    before = pPr.xpath('./w:spacing/@w:before') if pPr is not None else []
    after = pPr.xpath('./w:spacing/@w:after') if pPr is not None else []
    line = pPr.xpath('./w:spacing/@w:line') if pPr is not None else []
    rule = pPr.xpath('./w:spacing/@w:lineRule') if pPr is not None else []
    fl = pPr.xpath('./w:ind/@w:firstLine') if pPr is not None else []
    flc = pPr.xpath('./w:ind/@w:firstLineChars') if pPr is not None else []
    left = pPr.xpath('./w:ind/@w:left') if pPr is not None else []
    num = bool(pPr.xpath('./w:numPr')) if pPr is not None else False
    
    # check runs
    run_szs = [r._r.xpath('./w:rPr/w:sz/@w:val') for r in p.runs]
    run_b = [bool(r._r.xpath('./w:rPr/w:b')) for r in p.runs]
    run_ea = [r._r.xpath('./w:rPr/w:rFonts/@w:eastAsia') for r in p.runs]
    run_ascii = [r._r.xpath('./w:rPr/w:rFonts/@w:ascii') for r in p.runs]
    
    # check style
    st_sz = p.style.element.xpath('./w:rPr/w:sz/@w:val') if p.style else []
    st_ea = p.style.element.xpath('./w:rPr/w:rFonts/@w:eastAsia') if p.style else []
    st_b = bool(p.style.element.xpath('./w:rPr/w:b')) if p.style else False
    
    is_heading = any(k in p.style.name for k in ['标题', 'heading', 'Heading']) or any(txt.startswith(k) for k in ['1 ', '2 ', '3 ', '4 ', '5 ', '1.', '2.', '3.'])
    is_list_item = any(txt.startswith(f"{n})") for n in range(1, 10)) or any(txt.startswith(f"({n})") for n in range(1, 10))
    
    if is_heading or is_list_item:
        print(f"P{i:3d} [{p.style.name}]: text={repr(txt[:45])}")
        print(f"     style: sz={st_sz}, ea={st_ea}, b={st_b}")
        print(f"     runs : sz={run_szs[:2]}, ea={run_ea[:2]}, ascii={run_ascii[:2]}, b={run_b[:2]}")
        print(f"     pPr  : before={before}, after={after}, line={line}({rule}), fl={fl}, flc={flc}, l={left}, num={num}")

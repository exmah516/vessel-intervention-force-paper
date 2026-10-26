# -*- coding: utf-8 -*-
import docx
import sys
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

ref_path = r'C:\Users\Sui\Downloads\14371982995898.docx'
doc = docx.Document(ref_path)

print("="*70)
print("1. ALL PARAGRAPHS IN TEMPLATE (with text, style, font, indent, spacing)")
print("="*70)

for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if not txt and not p._element.xpath('.//w:drawing') and not p._element.xpath('.//w:object'):
        continue
    
    style_name = p.style.name if p.style else 'None'
    style_id = p.style.style_id if p.style else 'None'
    align = p.alignment
    pPr = p._p.pPr
    
    # Indents
    first_line = pPr.xpath('./w:ind/@w:firstLine') if pPr is not None else []
    first_line_chars = pPr.xpath('./w:ind/@w:firstLineChars') if pPr is not None else []
    left_ind = pPr.xpath('./w:ind/@w:left') if pPr is not None else []
    
    # Spacing
    before = pPr.xpath('./w:spacing/@w:before') if pPr is not None else []
    after = pPr.xpath('./w:spacing/@w:after') if pPr is not None else []
    line = pPr.xpath('./w:spacing/@w:line') if pPr is not None else []
    line_rule = pPr.xpath('./w:spacing/@w:lineRule') if pPr is not None else []
    
    # Section break
    sectPr = pPr.xpath('./w:sectPr') if pPr is not None else []
    sect_info = ""
    if sectPr:
        stype = sectPr[0].xpath('./w:type/@w:val')
        scols = sectPr[0].xpath('./w:cols/@w:num')
        sect_info = f" [SECT_BREAK: type={stype}, cols={scols}]"
        
    # Runs font info
    runs_info = []
    for r in p.runs[:3]:
        rPr = r._r.rPr
        r_ascii = rPr.xpath('./w:rFonts/@w:ascii') if rPr is not None else []
        r_ea = rPr.xpath('./w:rFonts/@w:eastAsia') if rPr is not None else []
        r_sz = rPr.xpath('./w:sz/@w:val') if rPr is not None else []
        r_b = bool(rPr.xpath('./w:b')) if rPr is not None else False
        runs_info.append(f"(ea={r_ea}, ascii={r_ascii}, sz={r_sz}, b={r_b})")
        
    print(f"P{i:3d} [{style_name} / {style_id}]{sect_info}:")
    print(f"     text: {repr(txt[:60])}")
    print(f"     ind: fl={first_line}, flc={first_line_chars}, l={left_ind} | sp: b={before}, a={after}, line={line}({line_rule}) | al={align}")
    if runs_info:
        print(f"     runs: {runs_info[:2]}")

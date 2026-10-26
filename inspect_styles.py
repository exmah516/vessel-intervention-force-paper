# -*- coding: utf-8 -*-
import docx, sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r'C:\Users\Sui\Downloads\14371982995898.docx')

used_styles = set()
for p in doc.paragraphs:
    used_styles.add((p.style.name, p.style.style_id))

print('USED PARAGRAPH STYLES:')
for name, sid in sorted(used_styles):
    st = doc.styles[name]
    rPr = st.element.xpath('./w:rPr')
    pPr = st.element.xpath('./w:pPr')
    r_ea = rPr[0].xpath('./w:rFonts/@w:eastAsia') if rPr else []
    r_ascii = rPr[0].xpath('./w:rFonts/@w:ascii') if rPr else []
    r_sz = rPr[0].xpath('./w:sz/@w:val') if rPr else []
    r_b = bool(rPr[0].xpath('./w:b')) if rPr else False
    r_i = bool(rPr[0].xpath('./w:i')) if rPr else False
    pt = f"{int(r_sz[0])/2}pt" if r_sz else "N/A"
    print(f'Style: "{name}" (id={sid}) -> {pt}, ea={r_ea}, ascii={r_ascii}, b={r_b}')
    fl = pPr[0].xpath('./w:ind/@w:firstLine') if pPr else []
    flc = pPr[0].xpath('./w:ind/@w:firstLineChars') if pPr else []
    sp_b = pPr[0].xpath('./w:spacing/@w:before') if pPr else []
    sp_a = pPr[0].xpath('./w:spacing/@w:after') if pPr else []
    line = pPr[0].xpath('./w:spacing/@w:line') if pPr else []
    rule = pPr[0].xpath('./w:spacing/@w:lineRule') if pPr else []
    jc = pPr[0].xpath('./w:jc/@w:val') if pPr else []
    print(f'   pPr: fl={fl}, flc={flc}, before={sp_b}, after={sp_a}, line={line}({rule}), jc={jc}')

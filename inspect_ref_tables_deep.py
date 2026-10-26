# -*- coding: utf-8 -*-
import docx, sys
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r'C:\Users\Sui\Downloads\14371982995898.docx')

print("TABLES IN OFFICIAL TEMPLATE:")
for i, t in enumerate(doc.tables):
    print(f"\n{'='*30} Table {i} {'='*30}")
    tblPr = t._tbl.tblPr
    jc = tblPr.xpath('./w:jc/@w:val')
    tblW = tblPr.xpath('./w:tblW/@w:w')
    tblBorders = tblPr.xpath('./w:tblBorders')
    print(f"Alignment: {jc}, Width: {tblW}")
    if tblBorders:
        top = t._tbl.xpath('./w:tblPr/w:tblBorders/w:top/@w:val')
        top_sz = t._tbl.xpath('./w:tblPr/w:tblBorders/w:top/@w:sz')
        bot = t._tbl.xpath('./w:tblPr/w:tblBorders/w:bottom/@w:val')
        bot_sz = t._tbl.xpath('./w:tblPr/w:tblBorders/w:bottom/@w:sz')
        insideH = t._tbl.xpath('./w:tblPr/w:tblBorders/w:insideH/@w:val')
        insideH_sz = t._tbl.xpath('./w:tblPr/w:tblBorders/w:insideH/@w:sz')
        insideV = t._tbl.xpath('./w:tblPr/w:tblBorders/w:insideV/@w:val')
        print(f"Borders: top={top}(sz={top_sz}), bot={bot}(sz={bot_sz}), insideH={insideH}(sz={insideH_sz}), insideV={insideV}")
    
    # Check cell 0,0 and cell 1,0 font, style, alignment
    c0 = t.cell(0, 0)
    p0 = c0.paragraphs[0]
    r_ea = p0._element.xpath('.//w:rFonts/@w:eastAsia')
    r_sz = p0._element.xpath('.//w:sz/@w:val')
    print(f"Cell(0,0) text: {repr(c0.text.strip())}")
    print(f"          style: {p0.style.name}, font_ea={r_ea}, sz={r_sz}, jc={p0.alignment}")
    
    if len(t.rows) > 1:
        c1 = t.cell(1, 0)
        p1 = c1.paragraphs[0]
        r_ea1 = p1._element.xpath('.//w:rFonts/@w:eastAsia')
        r_sz1 = p1._element.xpath('.//w:sz/@w:val')
        print(f"Cell(1,0) text: {repr(c1.text.strip()[:30])}")
        print(f"          style: {p1.style.name}, font_ea={r_ea1}, sz={r_sz1}, jc={p1.alignment}")

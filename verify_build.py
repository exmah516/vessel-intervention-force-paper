# -*- coding: utf-8 -*-
import docx, sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
target = r'D:\Work_files\Vessel intervention Robot\力波动方法\write\论文撰写\面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_JQR.docx'
doc = docx.Document(target)

print("="*60)
print(f"VERIFICATION REPORT FOR: {target}")
print("="*60)

# Check Paragraph 0
p0 = doc.paragraphs[0]
print(f"P0 text: {repr(p0.text)}, style={p0.style.name}, font_size={p0.runs[0].font.size.pt if p0.runs else 'N/A'}")

# Check styles distribution
st_counts = Counter(p.style.name for p in doc.paragraphs)
print("\nSTYLE COUNTS:")
for st, cnt in st_counts.most_common():
    print(f"  {st:25s}: {cnt}")

# Check sections
print("\nSECTIONS:")
for idx, s in enumerate(doc.sections):
    cols = s._sectPr.xpath('./w:cols/@w:num')
    space = s._sectPr.xpath('./w:cols/@w:space')
    stype = s._sectPr.xpath('./w:type/@w:val')
    print(f"Sec {idx}: type={stype}, cols={cols}, space={space}, diffFirst={s.different_first_page_header_footer}")
    print(f"   Margins: top={s.top_margin.cm:.2f}cm, bot={s.bottom_margin.cm:.2f}cm, left={s.left_margin.cm:.2f}cm, right={s.right_margin.cm:.2f}cm")
    print(f"   Header default: {[p.text for p in s.header.paragraphs if p.text.strip()]}")
    print(f"   Header first:   {[p.text for p in s.first_page_header.paragraphs if p.text.strip()]}")
    print(f"   Footer first:   {[p.text[:30] for p in s.first_page_footer.paragraphs if p.text.strip()]}")

print("\nTABLES:")
print(f"Total tables: {len(doc.tables)} (including {len(doc.tables)-3} equation tables)")
for idx in [0, len(doc.tables)-2, len(doc.tables)-1]:
    if idx < len(doc.tables):
        t = doc.tables[idx]
        print(f"Table {idx}: rows={len(t.rows)}, cols={len(t.columns)}, cell(0,0)={repr(t.cell(0,0).text.strip()[:25])}")

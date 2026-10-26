import docx, sys, os
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')
tpl = docx.Document(r'C:\Users\Sui\Downloads\14371982995898.docx')

print("="*60)
print("1. SECTIONS AUDIT")
print("="*60)
for idx, s in enumerate(tpl.sections):
    cols = s._sectPr.xpath('./w:cols')
    col_num = cols[0].get(qn('w:num')) if cols else '1'
    col_space = cols[0].get(qn('w:space')) if cols else 'N/A'
    type_el = s._sectPr.xpath('./w:type/@w:val')
    sect_type = type_el[0] if type_el else 'default'
    print(f"Sec {idx}: type={sect_type}, cols={col_num}, space={col_space}, "
          f"top={s.top_margin.cm:.2f}cm, bot={s.bottom_margin.cm:.2f}cm, "
          f"left={s.left_margin.cm:.2f}cm, right={s.right_margin.cm:.2f}cm, "
          f"header_dist={s.header_distance.cm:.2f}cm, footer_dist={s.footer_distance.cm:.2f}cm, "
          f"diff_first={s.different_first_page_header_footer}")

print("\n" + "="*60)
print("2. EQUATIONS AUDIT")
print("="*60)
# Find equations in tpl
for i, p in enumerate(tpl.paragraphs):
    if '(1)' in p.text or '(2)' in p.text:
        omml = p._element.xpath('.//m:oMath')
        w_draw = p._element.xpath('.//w:drawing')
        print(f"P{i:3d} [{p.style.name:15s}]: text={repr(p.text[:50])}")
        print(f"     align={p.alignment}, ind={p.paragraph_format.first_line_indent}")
        print(f"     omml={len(omml)}, draw={len(w_draw)}")
        tabs = p._element.xpath('.//w:tabs/w:tab')
        if tabs:
            print(f"     tabs={[t.attrib for t in tabs]}")

print("\n" + "="*60)
print("3. TABLES AUDIT")
print("="*60)
for idx, t in enumerate(tpl.tables):
    rows = len(t.rows)
    cols = len(t.columns)
    grid_cols = [c.get(qn('w:w')) for c in t._tbl.xpath('./w:tblGrid/w:gridCol')]
    tblW = t._tbl.xpath('./w:tblPr/w:tblW/@w:w')
    jc = t._tbl.xpath('./w:tblPr/w:jc/@w:val')
    print(f"Table {idx}: rows={rows}, cols={cols}, tblW={tblW}, jc={jc}, gridCols={grid_cols}")
    cell0 = t.cell(0, 0).text.strip()[:30]
    print(f"   cell(0,0) text: {repr(cell0)}")

print("\n" + "="*60)
print("2.1 EQUATION P27 XML DETAILS")
print("="*60)
p27 = tpl.paragraphs[27]
print(p27._element.xml[:1500])

print("\n" + "="*60)
print("4. HEADERS AND FOOTERS AUDIT")
print("="*60)
for idx, s in enumerate(tpl.sections):
    print(f"--- Section {idx} Headers/Footers ---")
    for h_name, h in [('header', s.header), ('even_hdr', s.even_page_header), ('first_hdr', s.first_page_header)]:
        txts = [p.text.strip() for p in h.paragraphs if p.text.strip()]
        borders = [p._p.xpath('./w:pPr/w:pBdr') for p in h.paragraphs]
        print(f"  {h_name}: text={txts}, has_border={bool(any(borders))}")
    for f_name, f in [('footer', s.footer), ('even_ftr', s.even_page_footer), ('first_ftr', s.first_page_footer)]:
        txts = [p.text.strip() for p in f.paragraphs if p.text.strip()]
        draws = [p._p.xpath('.//w:drawing') for p in f.paragraphs]
        print(f"  {f_name}: text={txts[:1]}, has_drawing={bool(any(draws))}")

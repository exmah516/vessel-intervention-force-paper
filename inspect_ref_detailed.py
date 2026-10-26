import docx

ref = docx.Document('d:/Work_files/Vessel intervention Robot/力波动方法/write/论文撰写/面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制.docx')

print(f"Total sections: {len(ref.sections)}")
for i, s in enumerate(ref.sections):
    print(f"\n--- Section {i} ---")
    print(f"Start type: {s.start_type}")
    print(f"Page: {s.page_width.cm:.2f} x {s.page_height.cm:.2f} cm")
    print(f"Margins (cm): top={s.top_margin.cm:.2f}, bottom={s.bottom_margin.cm:.2f}, left={s.left_margin.cm:.2f}, right={s.right_margin.cm:.2f}")
    
    # Check cols
    cols = s._sectPr.xpath('./w:cols')
    if cols:
        num = cols[0].attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}num', '1')
        space = cols[0].attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}space', '0')
        print(f"Columns: num={num}, space={int(space)/20:.1f} pt ({int(space)/1440*2.54:.2f} cm)")
    else:
        print("Columns: 1 (default)")

# Now check which paragraph starts Section 1 and Section 2/3
for i, p in enumerate(ref.paragraphs):
    sectPr = p._p.xpath('./w:pPr/w:sectPr')
    if sectPr:
        print(f"Paragraph {i} has sectPr: text={repr(p.text[:30])}")

import docx

ref = docx.Document('d:/Work_files/Vessel intervention Robot/力波动方法/write/论文撰写/面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制.docx')

print("Paragraphs in ref:", len(ref.paragraphs))
for i, p in enumerate(ref.paragraphs):
    if any(k in p.text for k in ['图 1', '图 2', '图 3', '图 4', '图 5', '图 6', '表 1', '表 A.1', '表 B.1']):
        print(f"P{i}: style={p.style.name}, text={repr(p.text[:60])}")
    # check for section breaks inside paragraphs
    sectPr = p._p.xpath('./w:pPr/w:sectPr')
    if sectPr:
        cols = sectPr[0].xpath('./w:cols')
        c_str = cols[0].attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}num', '1') if cols else '?'
        print(f"   [Section Break after P{i} -> cols={c_str}]")

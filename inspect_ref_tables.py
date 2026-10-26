import docx
from lxml import etree

ref = docx.Document('d:/Work_files/Vessel intervention Robot/力波动方法/write/论文撰写/面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制.docx')
print("Tables in ref:", len(ref.tables))
for i, t in enumerate(ref.tables):
    print(f"Table {i}: rows={len(t.rows)}, cols={len(t.columns)}")
    tblPr = t._tbl.tblPr
    print("   tblPr:", etree.tostring(tblPr, encoding='utf-8').decode('utf-8')[:300])
    # check cell widths of row 0
    widths = [c.width for c in t.rows[0].cells]
    print(f"   cell widths: {[w.cm if w else None for w in widths]}")

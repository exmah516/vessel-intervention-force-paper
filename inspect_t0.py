import docx
from lxml import etree

ref = docx.Document('d:/Work_files/Vessel intervention Robot/力波动方法/write/论文撰写/面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制.docx')
t0 = ref.tables[0]
print(etree.tostring(t0._tbl.tblPr, encoding='utf-8', pretty_print=True).decode('utf-8'))

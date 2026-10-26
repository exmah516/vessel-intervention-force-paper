import docx
from lxml import etree

ref = docx.Document('d:/Work_files/Vessel intervention Robot/力波动方法/write/论文撰写/面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制.docx')
for i in [28, 29, 30, 31]:
    p = ref.paragraphs[i]
    print(f"P{i}: style={p.style.name}, text={repr(p.text[:40])}")
    print("   pPr:", etree.tostring(p._element.xpath('./w:pPr')[0], encoding='utf-8').decode('utf-8') if p._element.xpath('./w:pPr') else 'none')

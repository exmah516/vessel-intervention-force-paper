import sys, docx
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document('d:/Work_files/Vessel intervention Robot/力波动方法/write/论文撰写/JQR_LaTeX_Template-0507/intermediate.docx')
for i in range(170, len(doc.paragraphs)):
    p = doc.paragraphs[i]
    print(f"P{i}: {repr(p.text[:40])}")

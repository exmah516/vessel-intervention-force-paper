import docx

ref = docx.Document('d:/Work_files/Vessel intervention Robot/力波动方法/write/论文撰写/面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制.docx')
for i, p in enumerate(ref.paragraphs):
    if any(k in p.text for k in ['（1）', '（2）', '（3）', '（4）', '（5）']) and len(p.text.strip()) < 30:
        print(f"P{i}: {repr(p.text)}")

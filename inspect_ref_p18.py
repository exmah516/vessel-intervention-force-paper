import docx

ref = docx.Document('d:/Work_files/Vessel intervention Robot/力波动方法/write/论文撰写/面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制.docx')
for i in range(14, 21):
    p = ref.paragraphs[i]
    print(f"P{i:2d} [{p.style.name}]: {repr(p.text)}")

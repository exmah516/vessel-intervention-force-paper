import docx

doc = docx.Document('d:/Work_files/Vessel intervention Robot/力波动方法/write/论文撰写/面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_JQR.docx')
for i, t in enumerate(doc.tables):
    if len(t.rows) == 1 and len(t.columns) == 2:
        num = t.cell(0, 1).text.strip()
        # count runs/chars in cell 0
        txt = t.cell(0, 0).text.strip()
        # count omath elements
        omaths = len(t.cell(0, 0)._tc.xpath('.//m:oMath'))
        print(f"Eq {num}: text_len={len(txt)}, omaths={omaths}")

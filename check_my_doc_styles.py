# -*- coding: utf-8 -*-
import docx, sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
my_doc = docx.Document(r'D:\Work_files\Vessel intervention Robot\力波动方法\write\论文撰写\面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_JQR_v2.docx')

styles_count = Counter(p.style.name for p in my_doc.paragraphs)
print("STYLES DISTRIBUTION IN MY DOC:")
for s, c in styles_count.most_common():
    print(f"  {s:25s}: {c}")

print("\nPARAGRAPHS WITH 'Body Text Indent' or 'Normal':")
for i, p in enumerate(my_doc.paragraphs):
    if p.style.name in ['Body Text Indent', 'Normal']:
        txt = p.text.strip()[:40]
        if txt:
            print(f"P{i:3d} [{p.style.name:18s}]: {repr(txt)}")

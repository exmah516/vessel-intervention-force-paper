# -*- coding: utf-8 -*-
import docx, sys
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

ref_doc = docx.Document(r'C:\Users\Sui\Downloads\14371982995898.docx')
my_doc = docx.Document(r'D:\Work_files\Vessel intervention Robot\力波动方法\write\论文撰写\面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_JQR_v2.docx')

def get_p_details(p):
    pPr = p._p.pPr
    style_name = p.style.name if p.style else 'None'
    fl = pPr.xpath('./w:ind/@w:firstLine') if pPr is not None else []
    flc = pPr.xpath('./w:ind/@w:firstLineChars') if pPr is not None else []
    left = pPr.xpath('./w:ind/@w:left') if pPr is not None else []
    before = pPr.xpath('./w:spacing/@w:before') if pPr is not None else []
    after = pPr.xpath('./w:spacing/@w:after') if pPr is not None else []
    line = pPr.xpath('./w:spacing/@w:line') if pPr is not None else []
    lineRule = pPr.xpath('./w:spacing/@w:lineRule') if pPr is not None else []
    jc = pPr.xpath('./w:jc/@w:val') if pPr is not None else []
    sect = pPr.xpath('./w:sectPr/w:type/@w:val') if pPr is not None else []
    
    # Run font info
    fonts = []
    for r in p.runs:
        rPr = r._r.rPr
        if rPr is not None:
            ea = rPr.xpath('./w:rFonts/@w:eastAsia')
            ascii_f = rPr.xpath('./w:rFonts/@w:ascii')
            sz = rPr.xpath('./w:sz/@w:val')
            b = bool(rPr.xpath('./w:b'))
            i = bool(rPr.xpath('./w:i'))
            fonts.append((ea, ascii_f, sz, b, i, r.text[:10]))
    return {
        'text': p.text.strip()[:40],
        'style': style_name,
        'fl': fl, 'flc': flc, 'left': left,
        'before': before, 'after': after,
        'line': line, 'lineRule': lineRule,
        'jc': jc, 'sect': sect,
        'fonts': fonts[:3]
    }

print("=== REF DOC KEY PARAGRAPHS ===")
for i in [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 15, 16, 17, 19, 21, 24, 48, 86, 107, 131, 132, 138, 142]:
    if i < len(ref_doc.paragraphs):
        p = ref_doc.paragraphs[i]
        d = get_p_details(p)
        print(f"P{i:3d} [{d['style']}]: text={repr(d['text'])}")
        print(f"     fl={d['fl']}, flc={d['flc']}, l={d['left']} | sp: b={d['before']}, a={d['after']}, ln={d['line']}({d['lineRule']}) | jc={d['jc']} | sect={d['sect']}")
        print(f"     fonts: {d['fonts']}")

print("\n=== MY DOC KEY PARAGRAPHS ===")
for i in range(min(25, len(my_doc.paragraphs))):
    p = my_doc.paragraphs[i]
    d = get_p_details(p)
    print(f"P{i:3d} [{d['style']}]: text={repr(d['text'])}")
    print(f"     fl={d['fl']}, flc={d['flc']}, l={d['left']} | sp: b={d['before']}, a={d['after']}, ln={d['line']}({d['lineRule']}) | jc={d['jc']} | sect={d['sect']}")
    print(f"     fonts: {d['fonts']}")

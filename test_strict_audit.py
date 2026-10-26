# -*- coding: utf-8 -*-
import docx, sys

sys.stdout.reconfigure(encoding='utf-8')
target = r'D:\Work_files\Vessel intervention Robot\力波动方法\write\论文撰写\面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_JQR.docx'
doc = docx.Document(target)

print("="*60)
print("STRICT AUDIT FOR RE-GENERATED DOCUMENT:")
print("="*60)

# 1. Check for ANY numPr in the document
numpr_paras = []
for i, p in enumerate(doc.paragraphs):
    if p._p.xpath('.//w:numPr'):
        numpr_paras.append((i, p.text[:30]))
print(f"1. Automatic numbered paragraphs (numPr): {len(numpr_paras)}")
if numpr_paras:
    print(f"   Found numPr at: {numpr_paras[:5]}")
else:
    print("   -> ALL automatic numbering completely eliminated! Pure manual numbering enforced.")

# 2. Check 1) 2) paragraphs
print("\n2. Checking manual '1)' paragraphs:")
for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if txt.startswith('1) ') or txt.startswith('2) ') or txt.startswith('1\\) '):
        sz = [r.font.size.pt for r in p.runs if r.font.size]
        fl = p.paragraph_format.first_line_indent.pt if p.paragraph_format.first_line_indent else 0
        l_ind = p.paragraph_format.left_indent.pt if p.paragraph_format.left_indent else 0
        print(f"   P{i:3d}: text={repr(txt[:35])}, sz={sz[:1]}, fl_ind={fl}pt, l_ind={l_ind}pt")

# 3. Check Headings
print("\n3. Checking Heading font sizes and spacings:")
for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if any(txt.startswith(k) for k in ['1 问题描述', '1.1 往复', '1.3.1 矩阵', '参考文献（', '作者简介', '附录A']):
        sz = [r.font.size.pt for r in p.runs if r.font.size]
        b = p.paragraph_format.space_before.pt if p.paragraph_format.space_before else 0
        a = p.paragraph_format.space_after.pt if p.paragraph_format.space_after else 0
        jc = p.alignment
        print(f"   [{p.style.name:10s}] text={repr(txt[:30])} -> sz={sz[:1]}pt, bef={b}pt, aft={a}pt, jc={jc}")

# 4. Check Body Text font sizes
print("\n4. Checking Body Text font sizes:")
body_samples = []
for i, p in enumerate(doc.paragraphs):
    if p.style.name == '正文1':
        sz = [r.font.size.pt for r in p.runs if r.font.size]
        ea = [r._r.xpath('./w:rPr/w:rFonts/@w:eastAsia') for r in p.runs if r._r.xpath('./w:rPr/w:rFonts/@w:eastAsia')]
        fl = p.paragraph_format.first_line_indent.pt if p.paragraph_format.first_line_indent else 0
        body_samples.append((sz[:1], ea[:1], fl, p.text[:25]))

print(f"   Total '正文1' paragraphs: {len(body_samples)}")
for sz, ea, fl, txt in body_samples[:5]:
    print(f"     sz={sz}pt, font={ea}, firstLine={fl}pt, text={repr(txt)}")

# 5. Check References font sizes
print("\n5. Checking Reference entries font sizes:")
ref_samples = []
for i, p in enumerate(doc.paragraphs):
    if p.style.name == 'table of figures':
        sz = [r.font.size.pt for r in p.runs if r.font.size]
        fl = p.paragraph_format.first_line_indent.pt if p.paragraph_format.first_line_indent else 0
        l_ind = p.paragraph_format.left_indent.pt if p.paragraph_format.left_indent else 0
        ref_samples.append((sz[:1], fl, l_ind, p.text[:30]))

print(f"   Total reference entries: {len(ref_samples)}")
for sz, fl, l_ind, txt in ref_samples[:3]:
    print(f"     sz={sz}pt, fl={fl}pt, l={l_ind}pt, text={repr(txt)}")

# -*- coding: utf-8 -*-
import docx, sys

sys.stdout.reconfigure(encoding='utf-8')

ref_doc = docx.Document(r'C:\Users\Sui\Downloads\14371982995898.docx')
my_doc = docx.Document(r'D:\Work_files\Vessel intervention Robot\力波动方法\write\论文撰写\面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_JQR_v2.docx')

print("="*60)
print("COMPARING SECTIONS")
print("="*60)
print(f"Ref sections: {len(ref_doc.sections)}")
print(f"My sections:  {len(my_doc.sections)}")

for i in range(min(len(ref_doc.sections), len(my_doc.sections))):
    s_r = ref_doc.sections[i]
    s_m = my_doc.sections[i]
    print(f"\n--- Section {i} ---")
    print(f"Ref: cols={s_r._sectPr.xpath('./w:cols/@w:num')}, space={s_r._sectPr.xpath('./w:cols/@w:space')}, type={s_r._sectPr.xpath('./w:type/@w:val')}")
    print(f"My : cols={s_m._sectPr.xpath('./w:cols/@w:num')}, space={s_m._sectPr.xpath('./w:cols/@w:space')}, type={s_m._sectPr.xpath('./w:type/@w:val')}")
    print(f"Ref margins: top={s_r.top_margin.cm:.2f}, bot={s_r.bottom_margin.cm:.2f}, left={s_r.left_margin.cm:.2f}, right={s_r.right_margin.cm:.2f}")
    print(f"My  margins: top={s_m.top_margin.cm:.2f}, bot={s_m.bottom_margin.cm:.2f}, left={s_m.left_margin.cm:.2f}, right={s_m.right_margin.cm:.2f}")
    print(f"Ref diffFirst={s_r.different_first_page_header_footer}")
    print(f"My  diffFirst={s_m.different_first_page_header_footer}")
    
print("\n" + "="*60)
print("COMPARING FIRST 15 PARAGRAPHS")
print("="*60)
for i in range(min(15, len(my_doc.paragraphs))):
    p_m = my_doc.paragraphs[i]
    p_r = ref_doc.paragraphs[i] if i < len(ref_doc.paragraphs) else None
    r_txt = p_r.text[:30] if p_r else "N/A"
    r_sty = p_r.style.name if p_r else "N/A"
    print(f"P{i:2d}: My [{p_m.style.name:15s}] {repr(p_m.text[:30])}")
    print(f"     Ref[{r_sty:15s}] {repr(r_txt)}")

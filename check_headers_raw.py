# -*- coding: utf-8 -*-
import docx, sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r'C:\Users\Sui\Downloads\14371982995898.docx')

for i, s in enumerate(doc.sections):
    print(f"=== SECTION {i} ===")
    print("Header default:", [p.text for p in s.header.paragraphs])
    print("Header even:   ", [p.text for p in s.even_page_header.paragraphs])
    print("Header first:  ", [p.text for p in s.first_page_header.paragraphs])
    print("Footer default:", [p.text for p in s.footer.paragraphs])
    print("Footer even:   ", [p.text for p in s.even_page_footer.paragraphs])
    print("Footer first:  ", [p.text for p in s.first_page_footer.paragraphs])
    print("diffFirst:", s.different_first_page_header_footer)

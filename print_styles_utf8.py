# -*- coding: utf-8 -*-
import zipfile, sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

with zipfile.ZipFile(r'C:\Users\Sui\Downloads\14371982995898.docx') as z:
    styles_xml = z.read('word/styles.xml').decode('utf-8')

root = ET.fromstring(styles_xml)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

for s in root.findall('.//w:style', ns):
    sid = s.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}styleId')
    name_el = s.find('.//w:name', ns)
    name = name_el.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if name_el is not None else ''
    stype = s.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type')
    if stype == 'paragraph':
        rPr = s.find('.//w:rPr', ns)
        pPr = s.find('.//w:pPr', ns)
        rf = {}
        sz_val = 'N/A'
        b_val = False
        if rPr is not None:
            rFonts = rPr.find('.//w:rFonts', ns)
            if rFonts is not None:
                rf = {k.split('}')[-1]: v for k, v in rFonts.attrib.items()}
            sz = rPr.find('.//w:sz', ns)
            if sz is not None:
                sz_val = sz.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
            b_val = rPr.find('.//w:b', ns) is not None
        ind_dict = {}
        sp_dict = {}
        jc_val = 'N/A'
        if pPr is not None:
            ind = pPr.find('.//w:ind', ns)
            if ind is not None:
                ind_dict = {k.split('}')[-1]: v for k, v in ind.attrib.items()}
            sp = pPr.find('.//w:spacing', ns)
            if sp is not None:
                sp_dict = {k.split('}')[-1]: v for k, v in sp.attrib.items()}
            jc = pPr.find('.//w:jc', ns)
            if jc is not None:
                jc_val = jc.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
        print(f"Style: '{name}' (id={sid})")
        print(f"   font: {rf}, sz={sz_val} ({int(sz_val)/2 if sz_val!='N/A' else 'N/A'}pt), bold={b_val}")
        print(f"   pPr: ind={ind_dict}, spacing={sp_dict}, jc={jc_val}")

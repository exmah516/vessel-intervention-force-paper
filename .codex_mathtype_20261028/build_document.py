from pathlib import Path
from copy import deepcopy
import json,re,hashlib
from zipfile import ZipFile
from lxml import etree as E
from docx import Document
from docx.shared import Pt,Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH,WD_LINE_SPACING,WD_BREAK
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement,parse_xml
from docx.oxml.ns import qn
from docx.opc.part import Part
from docx.opc.packuri import PackURI
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from convert_equations import key,EQ

TASK=Path(__file__).parent;BASE=TASK.parent
SOURCE=json.loads((TASK/'source.json').read_text(encoding='utf-8'))
TEMPLATE=BASE/'14371982995898.docx'
OUTPUT=BASE/'面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_MathType.docx'
manifest=json.loads((TASK/'equation_manifest.json').read_text(encoding='utf-8'))
COLWIDTH=(11907-1440-1133)/40
PAGEWIDTH=(11907-1440)/20
doc=Document(TEMPLATE);package=doc.part.package
sectlist=doc._element.xpath('.//w:sectPr')
frontsect=deepcopy(sectlist[0]);bodysect=deepcopy(sectlist[1])
object_template=deepcopy(doc._element.xpath('.//w:r[w:object]')[0])
for c in list(doc._element.body):doc._element.body.remove(c)
doc._element.body.append(deepcopy(bodysect))
olecount=0;previewparts={};inventory=[];actualequations=[]

def remove(el,tag):
    for x in el.findall(qn(tag)):el.remove(x)

def child(el,tag,**attrs):
    x=el.find(qn(tag))
    if x is None:x=OxmlElement(tag);el.append(x)
    for k,v in attrs.items():x.set(qn('w:'+k),str(v))
    return x

def fonts(rpr,ea='宋体',pt=None):
    f=child(rpr,'w:rFonts',ascii='Times New Roman',hAnsi='Times New Roman',eastAsia=ea,cs='Times New Roman')
    for a in list(f.attrib):
        if 'theme' in a.lower():del f.attrib[a]
    if pt is not None:child(rpr,'w:sz',val=round(pt*2));child(rpr,'w:szCs',val=round(pt*2))
    col=rpr.find(qn('w:color'))
    if col is not None:col.set(qn('w:val'),'000000');col.attrib.pop(qn('w:themeColor'),None)

# Enforce explicit Latin/East Asian fonts on every template style.
for st in doc.styles:
    rp=st.element.find(qn('w:rPr'))
    if rp is None:rp=OxmlElement('w:rPr');st.element.append(rp)
    ea=rp.find(qn('w:rFonts'))
    current=ea.get(qn('w:eastAsia'),'宋体') if ea is not None else '宋体'
    if st.type==WD_STYLE_TYPE.PARAGRAPH and 'heading' in st.name.lower():current='黑体'
    fonts(rp,current)
    for np in st.element.xpath('.//w:numPr'):np.getparent().remove(np)
    for x in st.element.xpath('./w:autoRedefine'):st.element.remove(x)
    if st.type==WD_STYLE_TYPE.PARAGRAPH:
        pp=st.element.get_or_add_pPr();child(pp,'w:autoSpaceDE',val='0');child(pp,'w:autoSpaceDN',val='0')
defaults=doc.styles.element.find(qn('w:docDefaults'))
if defaults is not None:
    rp=defaults.find(qn('w:rPrDefault')).find(qn('w:rPr'));fonts(rp,'宋体',10.5)

def style(name,size=10.5,ea='宋体',before=0,after=0,indent=21,align=WD_ALIGN_PARAGRAPH.JUSTIFY,keep=False):
    st=doc.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
    st.base_style=doc.styles['Normal'];fonts(st.element.get_or_add_rPr(),ea,size)
    f=st.paragraph_format;f.space_before=Pt(before);f.space_after=Pt(after);f.first_line_indent=Pt(indent)
    f.left_indent=Pt(0);f.right_indent=Pt(0);f.alignment=align
    f.line_spacing_rule=WD_LINE_SPACING.AT_LEAST;f.line_spacing=Pt(12 if size>=10.5 else 11.5)
    f.keep_with_next=keep;f.keep_together=False
    pp=st.element.get_or_add_pPr();child(pp,'w:autoSpaceDE',val='0');child(pp,'w:autoSpaceDN',val='0');child(pp,'w:snapToGrid',val='0')
    return st
style('JQRBody')
for lv,size,before,after in [(1,12,6,6),(2,10.5,6,0),(3,10.5,2,2)]:
    s=style('JQRHeading'+str(lv),size,'黑体',before,after,0,WD_ALIGN_PARAGRAPH.LEFT,True)
    child(s.element.get_or_add_pPr(),'w:outlineLvl',val=lv-1)
style('JQREquation',10.5,before=3,after=3,indent=0,align=WD_ALIGN_PARAGRAPH.LEFT)
style('JQRCaption',9,before=0,after=0,indent=0,align=WD_ALIGN_PARAGRAPH.CENTER)
style('JQRFigure',9,before=3,after=0,indent=0,align=WD_ALIGN_PARAGRAPH.CENTER,keep=True)
style('JQRPlaceholder',9,before=3,after=3,indent=0,align=WD_ALIGN_PARAGRAPH.JUSTIFY,keep=True)
style('JQRReference',9,before=0,after=0,indent=-15,align=WD_ALIGN_PARAGRAPH.JUSTIFY)
doc.styles['JQRReference'].paragraph_format.left_indent=Pt(15)
for name in ['JQRPlaceholder','JQRCaption','JQRReference']:
    doc.styles[name].paragraph_format.keep_together=True
style('JQRAuthorBio',9,before=0,after=0,indent=18)
style('JQRTable',9,before=0,after=0,indent=0,align=WD_ALIGN_PARAGRAPH.CENTER)
style('JQRSectionBreak',1,before=0,after=0,indent=0)

def xml_text(nodes):
    result=''
    for n in nodes:
        t=n['t'];c=n.get('c')
        if t=='Str':result+=c
        elif t in ['Space','SoftBreak']:result+=' '
        elif t=='LineBreak':result+='\n'
        elif t in ['Strong','Emph','Superscript','Subscript','SmallCaps','Strikeout']:result+=xml_text(c)
        elif t=='Quoted':result+=xml_text(c[1])
        elif t=='Link':result+=xml_text(c[1])
    return result

def plain_ast(blocks):
    return ' '.join(xml_text(b['c']) for b in blocks if b['t'] in ['Para','Plain'])

def addmath(p,tex,size=10.5,display=False):
    global olecount
    k=key(tex,size);e=manifest[k];assert 'width' in e,(tex,k)
    olecount+=1
    if k not in previewparts:
        pp=Part(PackURI('/word/media/jqr_eq_'+k+'.wmf'),'image/x-wmf',(EQ/(k+'.wmf')).read_bytes(),package);previewparts[k]=pp
    imgid=doc.part.relate_to(previewparts[k],RT.IMAGE)
    native=Part(PackURI(f'/word/embeddings/jqr_eq_{olecount:04d}.bin'),'application/vnd.openxmlformats-officedocument.oleObject',(EQ/(k+'.bin')).read_bytes(),package)
    oid=doc.part.relate_to(native,RT.OLE_OBJECT)
    run=deepcopy(object_template)
    rp=run.find(qn('w:rPr'))
    if rp is None:rp=OxmlElement('w:rPr');run.insert(0,rp)
    fonts(rp,'宋体',size)
    child(rp,'w:position',val=round(-e['baseline']*2))
    shape=run.find('.//{urn:schemas-microsoft-com:vml}shape');shapeid=f'_x0000_i{2000+olecount}'
    shape.set('id',shapeid);shape.set('style',f"width:{e['width']}pt;height:{e['height']}pt")
    shape.find('{urn:schemas-microsoft-com:vml}imagedata').set(qn('r:id'),imgid)
    ole=run.find('.//{urn:schemas-microsoft-com:office:office}OLEObject')
    ole.set('ShapeID',shapeid);ole.set('ObjectID',str(2000000000+olecount));ole.set(qn('r:id'),oid)
    ob=run.find(qn('w:object'));ob.set(qn('w:dxaOrig'),str(round(e['width']*20)));ob.set(qn('w:dyaOrig'),str(round(e['height']*20)))
    p._p.append(run)
    actualequations.append({'occurrence':olecount,'key':k,'display':display,'width':e['width'],'height':e['height'],'tex':tex})
    return e

def inlines(p,nodes,size=10.5,cn=True,attrs=None):
    attrs=attrs or {}
    for i,n in enumerate(nodes):
        t=n['t'];c=n.get('c')
        if t=='Math':addmath(p,c[1],size);continue
        if t in ['Space','SoftBreak']:
            prev=nodes[i-1]['t'] if i else None;nxt=nodes[i+1]['t'] if i+1<len(nodes) else None
            if cn and (prev=='Math' or nxt=='Math'):continue
            text=' '
        elif t=='Str':text=c
        elif t=='LineBreak':p.add_run().add_break();continue
        elif t in ['Strong','Emph','Superscript','Subscript','SmallCaps']:
            a=dict(attrs);a[{'Strong':'bold','Emph':'italic','Superscript':'superscript','Subscript':'subscript','SmallCaps':'small_caps'}[t]]=True
            inlines(p,c,size,cn,a);continue
        elif t=='Quoted':
            p.add_run('“' if c[0]['t']=='DoubleQuote' else '‘');inlines(p,c[1],size,cn,attrs);p.add_run('”' if c[0]['t']=='DoubleQuote' else '’');continue
        elif t=='Link':inlines(p,c[1],size,cn,attrs);continue
        elif t=='Span':inlines(p,c[1],size,cn,attrs);continue
        elif t=='Code':text=c[1]
        else:raise ValueError(('INLINE',t,n))
        if cn:text=re.sub(r'(?<=[\u3400-\u9fff，。、；：！？（）]) +| +(?=[\u3400-\u9fff，。、；：！？（）])','',text)
        r=p.add_run(text)
        for a,v in attrs.items():
            if a in ['superscript','subscript','small_caps']:setattr(r.font,a,v)
            else:setattr(r,a,v)

def paragraph(blocks,sty,size=10.5,cn=True,prefix='',keep=False):
    p=doc.add_paragraph(style=sty)
    if prefix:p.add_run(prefix)
    for i,b in enumerate(blocks):
        if i:p.add_run().add_break()
        assert b['t'] in ['Para','Plain'],b
        inlines(p,b['c'],size,cn)
    if keep:p.paragraph_format.keep_with_next=True
    return p

def sectbreak(section):
    p=doc.add_paragraph(style='JQRSectionBreak')
    p.paragraph_format.line_spacing_rule=WD_LINE_SPACING.EXACTLY;p.paragraph_format.line_spacing=Pt(1)
    p._p.get_or_add_pPr().append(deepcopy(section))

def bookmark(p,name):
    start=OxmlElement('w:bookmarkStart');start.set(qn('w:id'),str(10000+len(inventory)));start.set(qn('w:name'),name)
    end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),start.get(qn('w:id')))
    p._p.insert(1,start);p._p.append(end)

def captions(record,table=False):
    for language,prefix in [('cn','表' if table else '图'),('en','Table ' if table else 'Fig. ')]:
        p=paragraph(record[language+'_ast'],'JQRCaption',9,language=='cn',f"{prefix}{record['number']} ")
        for t in p._p.xpath('.//w:t'):
            if t.text:t.text=t.text.rstrip('。.') if t is p._p.xpath('.//w:t')[-1] else t.text
        p.paragraph_format.keep_with_next=language=='cn' or table
        if language=='en':p.paragraph_format.space_after=Pt(3)

def render_record(record):
    kind=record['type'];inventory.append({'type':kind,'number':record.get('number')})
    if kind=='equation':
        p=doc.add_paragraph(style='JQREquation')
        pp=p._p.get_or_add_pPr();tabs=OxmlElement('w:tabs')
        for pos,align in [((COLWIDTH-26)/2,'center'),(COLWIDTH,'right')]:
            tab=OxmlElement('w:tab');tab.set(qn('w:val'),align);tab.set(qn('w:pos'),str(round(pos*20)));tabs.append(tab)
        pp.append(tabs);p.add_run('\t')
        e=addmath(p,record['tex'],10.5,True);assert e['width']<=COLWIDTH-26,(record['number'],e['width'])
        p.add_run('\t('+str(record['number'])+')')
        p.paragraph_format.keep_together=True;bookmark(p,'JQR_eq_'+str(record['number']))
    elif kind=='figure':
        if 'image' in record:
            p=doc.add_paragraph(style='JQRFigure')
            p.add_run().add_picture(str(Path(SOURCE['source']).parent/record['image']),width=Pt(COLWIDTH))
            if 'note_ast' in record:paragraph(record['note_ast'],'JQRPlaceholder',9,keep=True)
        else:paragraph(record['placeholder_ast'],'JQRPlaceholder',9,keep=True)
        captions(record)
    elif kind=='references':
        p=doc.add_paragraph('参考文献（References）',style='JQRHeading1');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        for ref in SOURCE['references']:paragraph(ref['ast'],'JQRReference',9,False,prefix=f"[{ref['number']}] ")
    elif kind=='table':
        sectbreak(bodysect)
        captions(record,True)
        table=doc.add_table(rows=0,cols=5);table.autofit=False
        widths=[PAGEWIDTH*.29,PAGEWIDTH*.19,PAGEWIDTH*.19,PAGEWIDTH*.17,PAGEWIDTH*.16]
        for col,width in zip(table.columns,widths):col.width=Pt(width)
        pr=table._tbl.tblPr
        remove(pr,'w:tblBorders');borders=OxmlElement('w:tblBorders')
        for tag,val,sz in [('top','single',8),('bottom','single',8),('left','nil',0),('right','nil',0),('insideH','nil',0),('insideV','nil',0)]:
            x=OxmlElement('w:'+tag);x.set(qn('w:val'),val);x.set(qn('w:sz'),str(sz));x.set(qn('w:color'),'000000');borders.append(x)
        pr.append(borders)
        for idx,rowdata in enumerate(record['rows']):
            cells=table.add_row().cells;ci=0
            for cellinfo in rowdata:
                cell=cells[ci];span=cellinfo['span']
                if span>1:cell=cell.merge(cells[ci+span-1])
                p=cell.paragraphs[0];p.style='JQRTable'
                if ci==0:p.alignment=WD_ALIGN_PARAGRAPH.LEFT
                for j,b in enumerate(cellinfo['ast']):
                    if j:p.add_run().add_break()
                    inlines(p,b['c'],9,True)
                ci+=span
                cell.vertical_alignment=1
            trpr=table.rows[-1]._tr.get_or_add_trPr();child(trpr,'w:cantSplit')
            if idx==0:
                child(trpr,'w:tblHeader')
                for cell in cells:
                    tcpr=cell._tc.get_or_add_tcPr();cb=OxmlElement('w:tcBorders');line=OxmlElement('w:bottom');line.set(qn('w:val'),'single');line.set(qn('w:sz'),'4');cb.append(line);tcpr.append(cb)
            if idx==len(record['rows'])-1:
                for cell in cells:
                    tcpr=cell._tc.get_or_add_tcPr();cb=OxmlElement('w:tcBorders');line=OxmlElement('w:top');line.set(qn('w:val'),'single');line.set(qn('w:sz'),'4');cb.append(line);tcpr.append(cb)
        singlesect=deepcopy(bodysect);singlesect.find(qn('w:cols')).set(qn('w:num'),'1')
        singlesect.find(qn('w:cols')).set(qn('w:space'),'720')
        sectbreak(singlesect)
    else:raise ValueError(kind)

# Template front matter styles are the authority for title, authors and abstracts.
metadata=SOURCE['metadata']
p=doc.add_paragraph('DOI：10.13973/j.cnki.robot.'+metadata['doi'],style='JQRCaption');p.alignment=WD_ALIGN_PARAGRAPH.LEFT
for keyname,sty,size,cn,prefix in [
    ('cntitle','论文题目',18,True,''),('cnauthor','作者姓名',14,True,''),
    ('cnaddress','作者单位',9,True,'（'),('cnabstract','摘要&关键词',9,True,'摘  要：'),
    ('cnkeywords','摘要&关键词',9,True,'关键词：'),('entitle','英文文题',14,False,''),
    ('enauthor','作者姓名',12,False,''),('enaddress','作者单位',9,False,'('),
    ('enabstract','英文摘要',9,False,'Abstract: '),('enkeywords','英文摘要',9,False,'Keywords: ')]:
    p=paragraph(metadata[keyname+'_ast'],sty,size,cn,prefix)
    if keyname=='cntitle':
        title=metadata['cntitle'];left,right=title.split('力反馈',1)
        p.clear();p.add_run(left).add_break();p.add_run('力反馈'+right)
    if keyname.endswith('address'):p.add_run('）' if cn else ')')
    if keyname in ['cntitle','cnauthor','cnaddress','entitle','enauthor','enaddress']:
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next=True
        fonts(child(p._p.get_or_add_pPr(),'w:rPr'),'黑体' if keyname=='cntitle' else ('仿宋_GB2312' if keyname=='cnauthor' else '宋体'),size)
        for run in p.runs:fonts(run._r.get_or_add_rPr(),'黑体' if keyname=='cntitle' else ('仿宋_GB2312' if keyname=='cnauthor' else '宋体'),size)
    if keyname in ['cnaddress','enaddress']:p.paragraph_format.line_spacing=Pt(11)
    if keyname=='entitle':p.paragraph_format.space_before=Pt(12);p.paragraph_format.space_after=Pt(6)
    if keyname in ['cnabstract','cnkeywords','enabstract','enkeywords']:
        p.paragraph_format.first_line_indent=Pt(18);p.paragraph_format.left_indent=Pt(0);p.paragraph_format.right_indent=Pt(0)
        p.paragraph_format.line_spacing_rule=WD_LINE_SPACING.AT_LEAST;p.paragraph_format.line_spacing=Pt(11.5)
        for run in p.runs:fonts(run._r.get_or_add_rPr(),'宋体',9)
sectbreak(frontsect)

counts=[0,0,0];bio=False
for block in SOURCE['blocks']:
    t=block['t'];c=block.get('c')
    if t in ['Para','Plain']:
        text=xml_text(c)
        if text in SOURCE['records']:render_record(SOURCE['records'][text])
        else:
            sty='JQRAuthorBio' if bio else 'JQRBody';size=9 if bio else 10.5
            p=paragraph([block],sty,size)
            if text=='数据可用性声明':p.style='JQRHeading2';p.paragraph_format.keep_with_next=True
            inventory.append({'type':'paragraph','text':text})
    elif t=='Header':
        level,attr,nodes=c;unnumbered='unnumbered' in attr[1]
        title=xml_text(nodes)
        if title=='作者简介':bio=True
        if not unnumbered:
            counts[level-1]+=1
            for j in range(level,3):counts[j]=0
            prefix='.'.join(str(v) for v in counts[:level])+' '
        else:prefix=''
        p=doc.add_paragraph(style='JQRHeading'+str(min(level,3)));p.add_run(prefix);inlines(p,nodes,12 if level==1 else 10.5)
        if bio:p.style='JQRHeading2'
        inventory.append({'type':'heading','text':prefix+title})
    elif t=='OrderedList':
        for i,item in enumerate(c[1],c[0][0]):
            p=paragraph(item,'JQRBody',prefix=str(i)+'）')
            inventory.append({'type':'list','text':p.text})
    else:raise ValueError(('BLOCK',t))

# Replace template instructional footer text with manuscript metadata.
for section in doc.sections:
    footer=section.first_page_footer
    if any(p.text for p in footer.paragraphs):
        first=footer.paragraphs[0]
        for p in list(footer.paragraphs)[1:]:p._element.getparent().remove(p._element)
        first.clear();first.add_run('通信作者：'+plain_ast(metadata['corrauthor_ast'])+'　收稿/录用/修回：'+metadata['dates'])
        first.paragraph_format.line_spacing=Pt(10)
        for r in first.runs:fonts(r._r.get_or_add_rPr(),'宋体',8)
        child(first._p.get_or_add_pPr(),'w:autoSpaceDE',val='0');child(first._p.get_or_add_pPr(),'w:autoSpaceDN',val='0')

# Do not inherit list numbering or stale editing hints from the template.
for x in doc._element.xpath('.//w:numPr'):x.getparent().remove(x)
for x in doc.styles.element.xpath('.//w:numPr'):x.getparent().remove(x)
settings=doc.settings.element
child(settings,'w:updateFields',val='true')
for tag in ['w:trackRevisions','w:doNotTrackMoves','w:doNotTrackFormatting']:remove(settings,tag)
for part in package.parts:
    if part.partname==PackURI('/word/numbering.xml'):continue
for element in [doc._element,doc.styles.element,doc.settings.element]:
    for f in element.xpath('.//w:rFonts'):
        for a in list(f.attrib):
            if 'theme' in a.lower():del f.attrib[a]
doc.core_properties.title=metadata['cntitle'];doc.core_properties.subject='';doc.core_properties.comments=''
doc.save(OUTPUT)
(TASK/'build_inventory.json').write_text(json.dumps({'output':str(OUTPUT),'source_sha256':SOURCE['source_sha256'],'ole_count':olecount,'paragraphs':inventory,'equations':actualequations},ensure_ascii=False,indent=2),encoding='utf-8')
print('SAVED',OUTPUT,'OLE_OBJECTS',olecount,'SECTIONS',len(doc.sections),'PARAGRAPHS',len(doc.paragraphs),'TABLES',len(doc.tables))

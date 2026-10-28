from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image
import json,re,hashlib,ctypes as C,posixpath
from mathtype_native import MathType,guid,qi,method,release

task=Path(__file__).parent;base=task.parent
inventory=json.loads((task/'build_inventory.json').read_text(encoding='utf-8'))
source=json.loads((task/'source.json').read_text(encoding='utf-8'))
manifest=json.loads((task/'equation_manifest.json').read_text(encoding='utf-8'))
doc=Path(inventory['output']);z=ZipFile(doc)
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math','o':'urn:schemas-microsoft-com:office:office','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','rel':'http://schemas.openxmlformats.org/package/2006/relationships'}
def attr(x,name):return x.get('{'+ns['w']+'}'+name)
body=E.fromstring(z.read('word/document.xml'));styles=E.fromstring(z.read('word/styles.xml'));settings=E.fromstring(z.read('word/settings.xml'))
assert hashlib.sha256(Path(source['source']).read_bytes()).hexdigest()==source['source_sha256']
assert hashlib.sha256((base/'14371982995898.docx').read_bytes()).hexdigest()=='df597ceac1d22789ecfa9e9e7e1f7a1e2597ebe7d9ee0d515be65aaf3c5bb3c5'
assert not body.xpath('//w:numPr|//m:oMath|//w:ins|//w:del',namespaces=ns)
assert not styles.xpath('//w:numPr',namespaces=ns)
for s in styles.findall('w:style',ns):
 f=s.find('w:rPr/w:rFonts',ns)
 assert f is not None and all(attr(f,k) for k in ['ascii','hAnsi','eastAsia']),attr(s,'styleId')
 assert attr(f,'ascii')==attr(f,'hAnsi')=='Times New Roman',attr(s,'styleId')
 assert not any('theme' in k.lower() for k in f.attrib),attr(s,'styleId')
byid={attr(s,'styleId'):s for s in styles.findall('w:style',ns)}
for name,size,ea,before,after in [('JQRBody',21,'宋体',0,0),('JQRHeading1',24,'黑体',120,120),('JQRHeading2',21,'黑体',120,0),('JQRHeading3',21,'黑体',40,40),('JQRCaption',18,'宋体',0,0)]:
 s=byid[name];assert int(attr(s.find('w:rPr/w:sz',ns),'val'))==size
 assert attr(s.find('w:rPr/w:rFonts',ns),'eastAsia')==ea
 spacing=s.find('w:pPr/w:spacing',ns)
 assert (int(attr(spacing,'before')),int(attr(spacing,'after')))==(before,after),name
 for opt in ['autoSpaceDE','autoSpaceDN']:
  assert attr(s.find('w:pPr/w:'+opt,ns),'val')=='0'

paras=body.xpath('/w:document/w:body/w:p',namespaces=ns)
text=lambda p:''.join(p.xpath('.//w:t/text()',namespaces=ns))
sty=lambda p:attr(p.find('w:pPr/w:pStyle',ns),'val') if p.find('w:pPr/w:pStyle',ns) is not None else None
eqs=[p for p in paras if sty(p)=='JQREquation']
assert [text(p) for p in eqs]==[f'({i})' for i in range(1,28)]
assert all(len(p.xpath('.//o:OLEObject',namespaces=ns))==1 and p.find('w:pPr/w:keepLines',ns) is not None for p in eqs)
captions=[p for p in paras if sty(p)=='JQRCaption' and re.match(r'^(?:图|表|Fig\.|Table)',text(p))]
assert len(captions)==18
for p in captions:assert not text(p).endswith(('。','.'))
for i in range(0,18,2):assert paras.index(captions[i+1])==paras.index(captions[i])+1
refs=[p for p in paras if sty(p)=='JQRReference']
assert len(refs)==26
assert [re.match(r'\[(\d+)\]',text(p)).group(1) for p in refs]==[str(i) for i in range(1,27)]
assert sum(bool(re.match(r'\d+）',text(p))) for p in paras)==9
aff=[text(p) for p in paras if '中国科学院沈阳自动化研究所' in text(p)]
assert len(aff)==1 and aff[0].count('110016')==2 and aff[0].count('100049')==1
assert any('硕士研究生' in text(p) for p in paras)
assert len(body.xpath('//w:tbl',namespaces=ns))==1
assert len([r for r in source['records'].values() if r['type']=='figure'])==8
assert not any('JQRBLOCK' in text(p) for p in paras)
objects=body.xpath('//o:OLEObject',namespaces=ns)
assert len(objects)==inventory['ole_count']==len(inventory['equations'])==172
assert all(o.get('ProgID')=='Equation.DSMT4' and o.get('Type')=='Embed' for o in objects)
rels=E.fromstring(z.read('word/_rels/document.xml.rels'));relmap={r.get('Id'):r.get('Target') for r in rels}
native_paths=[]
temp=Path(r'C:\Users\Sui\AppData\Local\Temp\jqr_mt_20261028')/'audit';temp.mkdir(exist_ok=True)
eqroot=temp.parent/'equations'
red=[]
for key,item in manifest.items():
 im=Image.open(eqroot/(key+'.wmf'));im.load(dpi=96);im=im.convert('RGB')
 if any(r>170 and g<80 and b<80 for r,g,b in im.getdata()):red.append((key,item['tex']))
assert not red,red
for i,o in enumerate(objects):
 target=posixpath.normpath('word/'+relmap[o.get('{'+ns['r']+'}id')])
 data=z.read(target);expected=(eqroot/(inventory['equations'][i]['key']+'.bin')).read_bytes()
 assert data==expected and data[:8]==bytes.fromhex('d0cf11e0a1b11ae1')
 p=temp/f'eq_{i+1:03}.bin';p.write_bytes(data);native_paths.append(p)
 for neighbor in [o.getparent().getparent().getprevious(),o.getparent().getparent().getnext()]:
  if neighbor is not None:
   ts=neighbor.xpath('.//w:t/text()',namespaces=ns)
   if ts and sty(o.getparent().getparent().getparent())=='JQRBody':
    assert not ts[0].startswith(' ') and not ts[-1].endswith(' '),ts

# Reopen every saved native object in the installed MathType server and
# verify that its editable equation can be read back without translation loss.
mt=MathType();loaded=[]
mt.ole.StgOpenStorage.argtypes=[C.c_wchar_p,C.c_void_p,C.c_uint,C.c_void_p,C.c_uint,C.POINTER(C.c_void_p)]
try:
 for i,p in enumerate(native_paths):
  storage=C.c_void_p();obj=C.c_void_p();persist=None
  try:
   assert mt.ole.StgOpenStorage(str(p),None,0x10,None,0,C.byref(storage))==0
   cls=guid('0002CE03-0000-0000-C000-000000000046');iid=guid('00020400-0000-0000-C000-000000000046')
   assert mt.ole.CoCreateInstance(C.byref(cls),None,5,C.byref(iid),C.byref(obj))==0
   persist=qi(obj,'0000010A-0000-0000-C000-000000000046')
   assert method(persist,6,C.c_long,C.c_void_p)(persist,storage)==0
   n=C.c_int(20000);out=C.create_string_buffer(40000)
   assert mt.d.MTGetLangStrFromEqn(obj,1,out,C.byref(n))==0
   result=out.value.decode('utf-8',errors='replace')
   expected=manifest[inventory['equations'][i]['key']]['roundtrip']
   assert result==expected,(i+1,result,expected)
   loaded.append(i+1)
  finally:release(persist);release(storage);release(obj)
finally:mt.close()
report={'source_sha256':source['source_sha256'],'output_sha256':hashlib.sha256(doc.read_bytes()).hexdigest(),'style_count':len(byid),'native_objects_checked':len(loaded),'display_equations':27,'figures':8,'tables':1,'references':26,'captions':18,'manual_items':9,'all_checks_passed':True}
(task/'final_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))

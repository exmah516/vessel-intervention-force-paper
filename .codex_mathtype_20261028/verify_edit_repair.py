from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import ctypes as C,json,posixpath,hashlib
from mathtype_native import MathType,guid,qi,method,release
task=Path(__file__).parent
report=json.loads((task/'edit_repair_audit.json').read_text(encoding='utf-8'))
z=ZipFile(report['output']);old=ZipFile(report['source'])
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','o':'urn:schemas-microsoft-com:office:office','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
doc=E.fromstring(z.read('word/document.xml'));before=E.fromstring(old.read('word/document.xml'))
assert doc.xpath('//w:t/text()',namespaces=ns)==before.xpath('//w:t/text()',namespaces=ns)
assert z.read('word/styles.xml')==old.read('word/styles.xml')
for part in z.namelist():
 if part not in report['updated_parts']:assert z.read(part)==old.read(part),part
rels=E.fromstring(z.read('word/_rels/document.xml.rels'));targets={r.get('Id'):posixpath.normpath('word/'+r.get('Target')) for r in rels if r.get('TargetMode')!='External'}
mt=MathType();mt.ole.StgOpenStorage.argtypes=[C.c_wchar_p,C.c_void_p,C.c_uint,C.c_void_p,C.c_uint,C.POINTER(C.c_void_p)]
mt.d.MTXFormSetTranslator.argtypes=[C.c_short,C.c_char_p];mt.d.MTXFormSetTranslator.restype=C.c_int
cls=guid('0002CE03-0000-0000-C000-000000000046');iid=guid('00020400-0000-0000-C000-000000000046')
work=Path(r'C:\Users\Sui\AppData\Local\Temp\jqr_mt_20261028\edit_repair');count=0
try:
 for i,o in enumerate(doc.xpath('//o:OLEObject',namespaces=ns),1):
  p=work/f'verify_{i:03d}.bin';p.write_bytes(z.read(targets[o.get('{'+ns['r']+'}id')]))
  storage=C.c_void_p();obj=C.c_void_p();persist=None
  try:
   assert mt.ole.StgOpenStorage(str(p),None,0x10,None,0,C.byref(storage))==0
   assert mt.ole.CoCreateInstance(C.byref(cls),None,5,C.byref(iid),C.byref(obj))==0
   persist=qi(obj,'0000010A-0000-0000-C000-000000000046')
   assert method(persist,6,C.c_long,C.c_void_p)(persist,storage)==0
   n=C.c_int(0);dummy=C.create_string_buffer(16)
   assert mt.d.MTGetLangBytesFromEqn(obj,3,dummy,C.byref(n))==0
   out=C.create_string_buffer(n.value+2)
   assert mt.d.MTGetLangBytesFromEqn(obj,3,out,C.byref(n))==0
   data=out.raw[:n.value];assert bytes.fromhex('02009807ef') not in data
   for translator in [b'Texvc.tdl',b'Texvc (DataObject).tdl']:
    mt.d.MTXFormReset();assert mt.d.MTXFormSetTranslator(0,translator)==0
    src=C.create_string_buffer(data);dst=C.create_string_buffer(100000);dims=C.create_string_buffer(100)
    assert mt.d.MTXFormEqn(-3,4,src,len(data),-3,7,dst,len(dst),b'',dims)==0,(i,translator)
   count+=1
  finally:release(persist);release(storage);release(obj)
finally:mt.close()
assert count==172
result={'native_objects_reopened':count,'texvc_pass':count,'dataobject_pass':count,'prose_and_styles_unchanged':True,'sha256':hashlib.sha256(Path(report['output']).read_bytes()).hexdigest(),'computer_use_check':'unavailable: native pipe missing; no GUI-edit claim'}
(task/'edit_repair_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))

from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import ctypes as C,json,hashlib,posixpath,re,struct
from mathtype_native import MathType,guid,qi,method,release

task=Path(__file__).parent;base=task.parent
source=task/'before_edit_repair.docx'
output=base/'面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_MathType_编辑修复版.docx'
work=Path(r'C:\Users\Sui\AppData\Local\Temp\jqr_mt_20261028\edit_repair');work.mkdir(exist_ok=True)
z=ZipFile(source);parts={n:z.read(n) for n in z.namelist()}
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','o':'urn:schemas-microsoft-com:office:office','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','v':'urn:schemas-microsoft-com:vml'}
body=E.fromstring(parts['word/document.xml'])
rels=E.fromstring(parts['word/_rels/document.xml.rels'])
targets={r.get('Id'):posixpath.normpath('word/'+r.get('Target')) for r in rels if r.get('TargetMode')!='External'}
q=lambda p: '{'+ns[p.split(':')[0]]+'}'+p.split(':')[1]
mt=MathType()
mt.ole.StgOpenStorage.argtypes=[C.c_wchar_p,C.c_void_p,C.c_uint,C.c_void_p,C.c_uint,C.POINTER(C.c_void_p)]
mt.d.MTXFormSetTranslator.argtypes=[C.c_short,C.c_char_p];mt.d.MTXFormSetTranslator.restype=C.c_int
cls=guid('0002CE03-0000-0000-C000-000000000046');iid=guid('00020400-0000-0000-C000-000000000046')

def load(data,index):
 p=work/f'original_{index:03d}.bin';p.write_bytes(data)
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
  return out.raw[:n.value]
 finally:release(persist);release(storage);release(obj)

def translate(data,translator):
 src=C.create_string_buffer(data);out=C.create_string_buffer(100000);dims=C.create_string_buffer(100)
 mt.d.MTXFormReset();assert mt.d.MTXFormSetTranslator(0,translator.encode('ascii'))==0,translator
 ret=mt.d.MTXFormEqn(-3,4,src,len(data),-3,7,out,len(out),b'',dims)
 return ret,out.value.decode('utf-8',errors='replace')

def save(data,index):
 p=work/f'fixed_{index:03d}';obj=C.c_void_p();storage=C.c_void_p();persist=None
 try:
  assert mt.ole.CoCreateInstance(C.byref(cls),None,5,C.byref(iid),C.byref(obj))==0
  persist=qi(obj,'0000010A-0000-0000-C000-000000000046')
  assert mt.ole.StgCreateDocfile(str(p.with_suffix('.bin')),0x1012,0,C.byref(storage))==0
  assert method(persist,5,C.c_long,C.c_void_p)(persist,storage)==0
  src=C.create_string_buffer(data)
  assert mt.d.MTSetEqnFromLangBytes(obj,3,src,len(data))==0
  assert mt.ole.OleSave(persist,storage,1)==0
  assert method(storage,9,C.c_long,C.c_uint)(storage,0)==0
  mt.d.MTXFormReset();assert mt.d.MTXFormSetPrefs(1,b'')==0
  out=C.create_string_buffer(100000);dims=C.create_string_buffer(100)
  assert mt.d.MTXFormEqn(-3,4,src,len(data),-4,6,out,len(out),str(p.with_suffix('.wmf')).encode('mbcs'),dims)==0
  wmf=p.with_suffix('.wmf').read_bytes();left,top,right,bottom,inch=struct.unpack_from('<hhhhH',wmf,6)
  return {'binary':p.with_suffix('.bin').read_bytes(),'wmf':wmf,'width':(right-left)*72/inch,'height':(bottom-top)*72/inch,'baseline':mt.d.MTGetLastDimension(3)/32}
 finally:release(persist);release(storage);release(obj)

report=[];cache={};updated={}
try:
 for i,o in enumerate(body.xpath('//o:OLEObject',namespaces=ns),1):
  target=targets[o.get(q('r:id'))];data=load(parts[target],i)
  n=data.count(bytes.fromhex('02009807ef'))
  original_ret,_=translate(data,'Texvc.tdl')
  fixed=data.replace(bytes.fromhex('02009807ef'),bytes.fromhex('02009802ef'))
  fixedret,fixedtex=translate(fixed,'Texvc.tdl')
  hiddenret,_=translate(fixed,'Texvc (DataObject).tdl')
  assert fixedret==hiddenret==0,(i,fixedret,hiddenret,fixedtex)
  record={'occurrence':i,'inner_spaces':n,'original_texvc_status':original_ret,'fixed_texvc_status':fixedret,'fixed_dataobject_status':hiddenret}
  if n:
   key=hashlib.sha256(fixed).hexdigest()
   if key not in cache:cache[key]=save(fixed,i)
   e=cache[key];updated[target]=e['binary']
   # Change the native equation and its vector preview together, preserving
   # the existing OLE identity and all surrounding document formatting.
   object_el=o.getparent();shape=object_el.find('v:shape',ns)
   assert shape is not None,(i,E.tostring(object_el).decode())
   im=shape.find('v:imagedata',ns);imgtarget=targets[im.get(q('r:id'))]
   updated[imgtarget]=e['wmf']
   style=shape.get('style')
   style=re.sub(r'(?<![-\w])width:[^;]+',f"width:{e['width']:g}pt",style)
   style=re.sub(r'(?<![-\w])height:[^;]+',f"height:{e['height']:g}pt",style)
   shape.set('style',style)
   object_el.set(q('w:dxaOrig'),str(round(e['width']*20)));object_el.set(q('w:dyaOrig'),str(round(e['height']*20)))
   rp=object_el.getparent().find('w:rPr',ns)
   if rp is not None:
    pos=rp.find('w:position',ns)
    if pos is not None:pos.set(q('w:val'),str(round(-e['baseline']*2)))
   record.update({'preview':imgtarget,'width':e['width'],'height':e['height']})
   print('Repaired object',i,'spaces',n,'width',e['width'],'Texvc',original_ret,'->',fixedret,flush=True)
  report.append(record)
finally:mt.close()
assert all(r['original_texvc_status']==0 or r['inner_spaces'] for r in report)
updated['word/document.xml']=E.tostring(body,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(output,'w',ZIP_DEFLATED) as out:
 for item in z.infolist():out.writestr(item,updated.get(item.filename,parts[item.filename]))
result={'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output':str(output),'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'objects_checked':len(report),'objects_repaired':sum(r['inner_spaces']>0 for r in report),'unique_equations_repaired':len(cache),'updated_parts':list(updated),'results':report}
(task/'edit_repair_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['results','updated_parts']},ensure_ascii=False,indent=2),flush=True)

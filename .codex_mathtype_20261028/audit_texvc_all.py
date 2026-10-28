from pathlib import Path
import ctypes as C,json
task=Path(__file__).parent;root=Path(r'C:\Users\Sui\AppData\Local\Temp\jqr_mt_20261028\equations')
manifest=json.loads((task/'equation_manifest.json').read_text(encoding='utf-8'))
d=C.WinDLL(r'D:\WORK_SOFTWARE\mathtype\System\64\MT6.dll')
d.MTAPIConnect.argtypes=[C.c_short,C.c_short];d.MTAPIConnect.restype=C.c_int
assert d.MTAPIConnect(0,5)==0
d.MTXFormSetTranslator.argtypes=[C.c_short,C.c_char_p];d.MTXFormSetTranslator.restype=C.c_int
d.MTXFormEqn.argtypes=[C.c_short,C.c_short,C.c_void_p,C.c_int,C.c_short,C.c_short,C.c_void_p,C.c_int,C.c_char_p,C.c_void_p];d.MTXFormEqn.restype=C.c_int
results=[]
try:
 for key,item in manifest.items():
  data=(root/(key+'.mtef')).read_bytes()
  for changed in [False,True]:
   t=data.replace(bytes.fromhex('02009807ef'),bytes.fromhex('02009802ef')) if changed else data
   src=C.create_string_buffer(t);out=C.create_string_buffer(100000);dims=C.create_string_buffer(100)
   d.MTXFormReset();assert d.MTXFormSetTranslator(0,b'Texvc.tdl')==0
   ret=d.MTXFormEqn(-3,4,src,len(t),-3,7,out,len(out),b'',dims)
   if ret:print(key,'eq',item['number'],'fixed',changed,'return',ret,item['tex'],flush=True)
   results.append({'key':key,'number':item['number'],'fixed':changed,'return':ret})
finally:d.MTAPIDisconnect()
(task/'texvc_all_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('Original failures',sum(r['return']!=0 for r in results if not r['fixed']),'corrected failures',sum(r['return']!=0 for r in results if r['fixed']),flush=True)

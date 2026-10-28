from pathlib import Path
import ctypes as C,json,sys
root=Path(r'C:\Users\Sui\AppData\Local\Temp\jqr_mt_20261028\equations')
d=C.WinDLL(r'D:\WORK_SOFTWARE\mathtype\System\64\MT6.dll')
d.MTAPIConnect.argtypes=[C.c_short,C.c_short];d.MTAPIConnect.restype=C.c_int
connect=d.MTAPIConnect(0,5);assert connect==0,('connect',connect)
d.MTXFormSetTranslator.argtypes=[C.c_short,C.c_char_p];d.MTXFormSetTranslator.restype=C.c_int
d.MTXFormEqn.argtypes=[C.c_short,C.c_short,C.c_void_p,C.c_int,C.c_short,C.c_short,C.c_void_p,C.c_int,C.c_char_p,C.c_void_p];d.MTXFormEqn.restype=C.c_int
d.MTXFormGetStatus.argtypes=[C.c_int];d.MTXFormGetStatus.restype=C.c_int
results=[]
for name in sys.argv[1:] or ['087f131a07dbd9bcc2']:
 data=(root/(name+'.mtef')).read_bytes()
 for variant in ['original','thin-space','no-inner-space']:
  t=data
  if variant=='thin-space':t=t.replace(bytes.fromhex('02009807ef'),bytes.fromhex('02009802ef'))
  if variant=='no-inner-space':t=t.replace(bytes.fromhex('02009807ef'),bytes.fromhex('02009801ef'))
  d.MTXFormReset();r=d.MTXFormSetTranslator(0,b'Texvc.tdl')
  assert r==0,('translator',r)
  src=C.create_string_buffer(t);out=C.create_string_buffer(100000);dims=C.create_string_buffer(100)
  ret=d.MTXFormEqn(-3,4,src,len(t),-3,7,out,len(out),b'',dims)
  result={'key':name,'variant':variant,'ret':ret,'translator_status':d.MTXFormGetStatus(-2),'actual_length':d.MTXFormGetStatus(-1),'tex':out.value.decode('utf-8',errors='replace')}
  print(json.dumps(result,ensure_ascii=False),flush=True);results.append(result)
Path(__file__).with_name('repro_texvc_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
d.MTAPIDisconnect()

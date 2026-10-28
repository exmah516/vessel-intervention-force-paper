import ctypes as C
from pathlib import Path
TASK=Path(__file__).parent
d=C.WinDLL(r'D:\WORK_SOFTWARE\mathtype\System\64\MT6.dll')
d.MTAPIConnect.argtypes=[C.c_short,C.c_short];d.MTAPIConnect.restype=C.c_int
print('CONNECT',d.MTAPIConnect(0,20),flush=True)
d.MTXFormEqn.argtypes=[C.c_short,C.c_short,C.c_void_p,C.c_int,C.c_short,C.c_short,C.c_void_p,C.c_int,C.c_char_p,C.c_void_p];d.MTXFormEqn.restype=C.c_int
d.MTXFormGetStatus.argtypes=[C.c_int];d.MTXFormGetStatus.restype=C.c_int
for i,t in enumerate([r'x^2',r'$x^2$',r'\[x^2\]',r'\frac{a}{b}+c']):
    inp=C.create_string_buffer(t.encode());out=C.create_string_buffer(100000);dims=C.create_string_buffer(100)
    d.MTXFormReset()
    ret=d.MTXFormEqn(-3,7,inp,len(t),-3,4,out,len(out),b'',dims)
    count=d.MTXFormGetStatus(-1)
    print('TRANSFORM',repr(t),ret,'length',count,'data',out.raw[:30].hex(),'dims',dims.raw[:24].hex(),flush=True)
    if ret==0 and count>0:(TASK/f'probe_{i}.mtef').write_bytes(out.raw[:count])
d.MTAPIDisconnect()

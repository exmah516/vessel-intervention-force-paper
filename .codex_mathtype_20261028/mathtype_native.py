import ctypes as C,uuid,struct
from pathlib import Path

class GUID(C.Structure):_fields_=[('data',C.c_ubyte*16)]
def guid(s):
    g=GUID();C.memmove(C.byref(g),uuid.UUID(s).bytes_le,16);return g
def method(obj,index,restype,*args):
    table=C.cast(obj,C.POINTER(C.POINTER(C.c_void_p))).contents
    return C.WINFUNCTYPE(restype,C.c_void_p,*args)(table[index])
def qi(obj,iid):
    out=C.c_void_p();g=guid(iid)
    status=method(obj,0,C.c_long,C.POINTER(GUID),C.POINTER(C.c_void_p))(obj,C.byref(g),C.byref(out))
    assert status==0,(iid,status)
    return out
def release(obj):
    if obj:method(obj,2,C.c_ulong)(obj)

class MathType:
    def __init__(self):
        self.ole=C.OleDLL('ole32');self.ole.CoInitialize(None)
        self.d=C.WinDLL(r'D:\WORK_SOFTWARE\mathtype\System\64\MT6.dll')
        self.d.MTAPIConnect.argtypes=[C.c_short,C.c_short];self.d.MTAPIConnect.restype=C.c_int
        assert self.d.MTAPIConnect(0,20)==0
        self.d.MTSetEqnFromLangStr.argtypes=[C.c_void_p,C.c_short,C.c_void_p,C.c_int];self.d.MTSetEqnFromLangStr.restype=C.c_int
        self.d.MTSetEqnFromLangBytes.argtypes=[C.c_void_p,C.c_short,C.c_void_p,C.c_int];self.d.MTSetEqnFromLangBytes.restype=C.c_int
        self.d.MTGetLangBytesFromEqn.argtypes=[C.c_void_p,C.c_short,C.c_void_p,C.POINTER(C.c_int)];self.d.MTGetLangBytesFromEqn.restype=C.c_int
        self.d.MTXFormEqn.argtypes=[C.c_short,C.c_short,C.c_void_p,C.c_int,C.c_short,C.c_short,C.c_void_p,C.c_int,C.c_char_p,C.c_void_p];self.d.MTXFormEqn.restype=C.c_int
        self.d.MTXFormGetStatus.argtypes=[C.c_int];self.d.MTXFormGetStatus.restype=C.c_int
        self.d.MTGetLangStrFromEqn.argtypes=[C.c_void_p,C.c_short,C.c_void_p,C.POINTER(C.c_int)];self.d.MTGetLangStrFromEqn.restype=C.c_int
        self.d.MTXFormSetPrefs.argtypes=[C.c_short,C.c_char_p];self.d.MTXFormSetPrefs.restype=C.c_int
        self.d.MTGetLastDimension.argtypes=[C.c_short];self.d.MTGetLastDimension.restype=C.c_int
        self.ole.CoCreateInstance.argtypes=[C.POINTER(GUID),C.c_void_p,C.c_uint,C.POINTER(GUID),C.POINTER(C.c_void_p)]
        self.ole.StgCreateDocfile.argtypes=[C.c_wchar_p,C.c_uint,C.c_uint,C.POINTER(C.c_void_p)]
        self.ole.OleSave.argtypes=[C.c_void_p,C.c_void_p,C.c_int]

    def convert(self,tex,path,size_pt=10.5):
        path=Path(path);obj=C.c_void_p();storage=C.c_void_p();persist=None
        cls=guid('0002CE03-0000-0000-C000-000000000046');iid=guid('00020400-0000-0000-C000-000000000046')
        assert self.ole.CoCreateInstance(C.byref(cls),None,5,C.byref(iid),C.byref(obj))==0
        try:
            persist=qi(obj,'0000010A-0000-0000-C000-000000000046')
            assert self.ole.StgCreateDocfile(str(path.with_suffix('.bin')),0x1012,0,C.byref(storage))==0
            assert method(persist,5,C.c_long,C.c_void_p)(persist,storage)==0
            wrapped='$'+tex+'$'
            buf=C.create_unicode_buffer(wrapped)
            ret=self.d.MTSetEqnFromLangStr(obj,1,buf,len(wrapped))
            assert ret==0,('SET',ret,tex)
            dummy=C.create_string_buffer(16)
            size=C.c_int(0)
            ret=self.d.MTGetLangBytesFromEqn(obj,3,dummy,C.byref(size))
            assert ret==0 and size.value>0,('MTEF',ret,size.value,tex)
            out=C.create_string_buffer(max(100000,size.value+2))
            ret=self.d.MTGetLangBytesFromEqn(obj,3,out,C.byref(size))
            assert ret==0
            mtef=out.raw[:size.value]
            self.d.MTXFormReset()
            data=C.create_string_buffer(mtef);dims=C.create_string_buffer(100)
            prefs=Path(r'D:\WORK_SOFTWARE\mathtype\Preferences\Times+Symbol 10.eqp').read_text().replace('Full=10 pt',f'Full={size_pt:g} pt').replace('Vector=Times New Roman,B','Vector=Times New Roman,BI')
            assert self.d.MTXFormSetPrefs(3,prefs.encode('ascii'))==0
            assert self.d.MTXFormEqn(-3,4,data,len(mtef),-3,4,out,len(out),b'',dims)==0
            count=self.d.MTXFormGetStatus(-1);assert count>0
            mtef=out.raw[:count]
            # This MathType TeX importer encodes \, as the private inner
            # space EF07. Texvc/DataObject has no rule for EF07 and fails
            # during interactive OLE editing. Use the standard thin-space
            # record EF02, supported by both clipboard translators.
            mtef=mtef.replace(bytes.fromhex('02009807ef'),bytes.fromhex('02009802ef'))
            data=C.create_string_buffer(mtef)
            release(persist);release(storage);release(obj)
            persist=None;storage=C.c_void_p();obj=C.c_void_p()
            assert self.ole.CoCreateInstance(C.byref(cls),None,5,C.byref(iid),C.byref(obj))==0
            persist=qi(obj,'0000010A-0000-0000-C000-000000000046')
            assert self.ole.StgCreateDocfile(str(path.with_suffix('.bin')),0x1012,0,C.byref(storage))==0
            assert method(persist,5,C.c_long,C.c_void_p)(persist,storage)==0
            assert self.d.MTSetEqnFromLangBytes(obj,3,data,len(mtef))==0
            assert self.ole.OleSave(persist,storage,1)==0
            assert method(storage,9,C.c_long,C.c_uint)(storage,0)==0
            path.with_suffix('.mtef').write_bytes(mtef)
            self.d.MTXFormReset();self.d.MTXFormSetPrefs(1,b'')
            ret=self.d.MTXFormEqn(-3,4,data,len(mtef),-4,6,out,len(out),str(path.with_suffix('.wmf')).encode('mbcs'),dims)
            assert ret==0,('WMF',ret,tex)
            wmf=path.with_suffix('.wmf').read_bytes()
            assert struct.unpack_from('<I',wmf)[0]==0x9ac6cdd7
            left,top,right,bottom,inch=struct.unpack_from('<hhhhH',wmf,6)
            width=(right-left)*72/inch;height=(bottom-top)*72/inch
            baseline=self.d.MTGetLastDimension(3)/32
            n=C.c_int(20000);txt=C.create_string_buffer(n.value*2)
            r=self.d.MTGetLangStrFromEqn(obj,1,txt,C.byref(n))
            return {'tex':tex,'width':width,'height':height,'baseline':baseline,'mtef_bytes':len(mtef),'roundtrip':txt.value.decode('utf-8',errors='replace') if r==0 else None}
        finally:
            release(persist);release(storage);release(obj)

    def close(self):self.d.MTAPIDisconnect();self.ole.CoUninitialize()

if __name__=='__main__':
    import json
    root=Path(r'C:\Users\Sui\AppData\Local\Temp\jqr_mt_20261028')
    mt=MathType()
    try:print(json.dumps(mt.convert(r'\frac{a}{b}+c',root/'native'),ensure_ascii=False),flush=True)
    finally:mt.close()

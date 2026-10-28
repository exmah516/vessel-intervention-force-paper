from pathlib import Path
from zipfile import ZipFile
import struct,re,json

TASK=Path(__file__).parent
with ZipFile(r'D:\WORK_SOFTWARE\mathtype\Office Support\64\MathType Commands 2016.dotm') as z:
    b=z.read('word/vbaProject.bin')
u16=lambda p:struct.unpack_from('<H',b,p)[0]
u32=lambda p:struct.unpack_from('<I',b,p)[0]
ss=1<<u16(30);mini=1<<u16(32);cut=u32(56)
def sector(i):return b[(i+1)*ss:(i+2)*ss]
fatids=list(struct.unpack_from('<109I',b,76));dx=u32(68)
while dx<0xfffffffa:
    vals=struct.unpack('<%dI'%(ss//4),sector(dx));fatids.extend(vals[:-1]);dx=vals[-1]
fat=[]
for i in fatids:
    if i<0xfffffffa:fat.extend(struct.unpack('<%dI'%(ss//4),sector(i)))
def chain(i,table):
    out=[];seen=set()
    while i<0xfffffffa and i not in seen and i<len(table):seen.add(i);out.append(i);i=table[i]
    return out
def read_big(i,size=None):
    out=b''.join(sector(s) for s in chain(i,fat));return out if size is None else out[:size]
dirb=read_big(u32(48));entries=[]
for pos in range(0,len(dirb),128):
    e=dirb[pos:pos+128];ln=struct.unpack_from('<H',e,64)[0]
    if ln>=2:entries.append((e[:ln-2].decode('utf-16le'),e[66],struct.unpack_from('<I',e,116)[0],struct.unpack_from('<Q',e,120)[0]))
root=next(e for e in entries if e[1]==5);ministream=read_big(root[2],root[3]);mfbytes=read_big(u32(60));mf=list(struct.unpack('<%dI'%(len(mfbytes)//4),mfbytes))
def read_stream(e):
    if e[3]>=cut:return read_big(e[2],e[3])
    return b''.join(ministream[i*mini:(i+1)*mini] for i in chain(e[2],mf))[:e[3]]
def decompress(buf,offset):
    if offset>=len(buf) or buf[offset]!=1:raise ValueError()
    out=bytearray();cur=offset+1
    while cur<len(buf):
        start=cur;head=struct.unpack_from('<H',buf,cur)[0];cur+=2;end=min(start+(head&4095)+3,len(buf));base=len(out)
        if (head>>12)&7!=3:raise ValueError()
        if head&32768==0:out.extend(buf[cur:end]);cur=end;continue
        while cur<end:
            flags=buf[cur];cur+=1
            for bit in range(8):
                if cur>=end:break
                if flags&(1<<bit):
                    token=struct.unpack_from('<H',buf,cur)[0];cur+=2;bits=max(4,(len(out)-base-1).bit_length());length=(token&(65535>>bits))+3;distance=(token>>(16-bits))+1
                    if distance>len(out)-base:raise ValueError()
                    for _ in range(length):out.append(out[-distance])
                else:out.append(buf[cur]);cur+=1
        if len(out)>2000000:raise ValueError()
    return bytes(out)
modules={}
for e in entries:
    if e[1]!=2 or e[0].startswith(('__','_VBA')) or e[0] in ['dir','PROJECT','PROJECTwm']:continue
    data=read_stream(e)
    for m in re.finditer(b'\x01',data):
        try:
            dec=decompress(data,m.start())
            if b'Attribute VB_Name' in dec[:200]:modules[e[0]]=dec.decode('cp1252',errors='replace');break
        except (ValueError,IndexError,struct.error,OverflowError):pass
(TASK/'mt_vba.json').write_text(json.dumps(modules,ensure_ascii=False),encoding='utf-8')
for name in ['MTTeXToggle','MTSetData','Declarations64','Declarations','MTLib']:
    lines=modules[name].splitlines()
    for i,line in enumerate(lines):
        if (name=='MTTeXToggle' and ('Function SetMTTeXData' in line or 'Sub SetMTTeXData' in line)) or (name=='MTSetData' and 'Set myObj' in line) or (name=='Declarations64' and ('MTInitAPI Lib "MathPage' in line or 'MTSetEqnFromLangStr Lib "MathPage' in line)) or (name=='Declarations' and 'mtxfmTEXT As' in line) or (name=='MTLib' and 'Function CreateEqn' in line):
            print(name,i+1,'\n'.join(lines[max(0,i-3):i+48]))

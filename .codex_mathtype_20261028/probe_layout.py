from pathlib import Path
import json,re
from PIL import Image,ImageDraw
from convert_equations import normalize
from mathtype_native import MathType
task=Path(__file__).parent
root=Path(r'C:\Users\Sui\AppData\Local\Temp\jqr_mt_20261028')
s=json.loads((task/'source.json').read_text(encoding='utf-8'))
eq={r['number']:r['tex'] for r in s['records'].values() if r['type']=='equation'}
rhs16=re.sub(r'\\begin\{aligned\}|\\end\{aligned\}|&|\\\\','',eq[16]).split('=',1)[1].strip()
one19=re.sub(r'\\begin\{aligned\}|\\end\{aligned\}|&|\\\\','',eq[19])
tests={
 '16original':normalize(eq[16]),
 '16rhs':rhs16,
 '16break':r'\begin{align}&\bm x_k={}\\&'+rhs16+r'\end{align}',
 '16breaknatural':r'\begin{aligned}&\bm x_k={}\\&'+rhs16+r'\end{aligned}',
 '19one':one19,
 '25outerminus':r"\begin{aligned}t_{\mathrm{rec}}&=\inf\{t\ge t_{\mathrm{S8,end}}:|d_F(t')|\le\varepsilon_{\mathrm{tol}},\forall t'\in[t,t+t_{\mathrm{win}}]\}\\&-t_{\mathrm{S8,end}}.\end{aligned}",
 '25leftminus':r"\begin{aligned}&t_{\mathrm{rec}}=\inf\{t\ge t_{\mathrm{S8,end}}:|d_F(t')|\le\varepsilon_{\mathrm{tol}},\forall t'\in[t,t+t_{\mathrm{win}}]\}\\&\quad-t_{\mathrm{S8,end}}.\end{aligned}",
 '25sub':r't_{\mathrm{rec}}=\inf_{\substack{t\ge t_{\mathrm{S8,end}}\\|d_F(t\prime)|\le\varepsilon_{\mathrm{tol}}\\\forall t\prime\in[t,t+t_{\mathrm{win}}]}}t-t_{\mathrm{S8,end}}.',
 '25subprime':r"t_{\mathrm{rec}}=\inf_{\substack{t\ge t_{\mathrm{S8,end}}\\|d_F(t')|\le\varepsilon_{\mathrm{tol}},\ \forall t'\in[t,t+t_{\mathrm{win}}]}}t-t_{\mathrm{S8,end}}.",
 '25set':r'\begin{align}t_{\mathrm{rec}}&=\inf\{t\ge t_{\mathrm{S8,end}}:|d_F(t\prime)|\le\varepsilon_{\mathrm{tol}}\}\\&-t_{\mathrm{S8,end}}.\end{align}',
}
mt=MathType();images=[]
try:
 for name,tex in tests.items():
  p=root/('layout_'+name);r=mt.convert(normalize(tex),p)
  im=Image.open(p.with_suffix('.wmf'));im.load(dpi=216);im=im.convert('RGB')
  red=any(r>170 and g<80 and b<80 for r,g,b in im.getdata())
  print(name,r['width'],r['height'],'RED',red,r['roundtrip'],flush=True)
  images.append((name,r,im))
finally:mt.close()
can=Image.new('RGB',(1100,sum(im.height+55 for _,_,im in images)),'white');d=ImageDraw.Draw(can);y=0
for name,r,im in images:
 d.text((10,y+5),f"{name}: {r['width']:.1f} x {r['height']:.1f}",fill='black');can.paste(im,(15,y+30));y+=im.height+55
can.save(task/'layout_probe.png')

from pathlib import Path
import sys,json,math
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
TASK=Path(__file__).parent
pdf=Path(sys.argv[1] if len(sys.argv)>1 else TASK/'render_v1.pdf')
out=TASK/pdf.stem;out.mkdir(exist_ok=True)
d=pdfium.PdfDocument(str(pdf))
images=[]
for i,page in enumerate(d):
    im=page.render(scale=2).to_pil()
    im.save(out/f'page-{i+1}.png')
    thumb=im.copy();thumb.thumbnail((595,842));images.append(thumb)
sheet=Image.new('RGB',(595*2,872*math.ceil(len(images)/2)),(220,220,220));draw=ImageDraw.Draw(sheet)
for i,im in enumerate(images):
    x=i%2*595;y=i//2*872;sheet.paste(im,(x,y+25));draw.text((x+10,y+6),str(i+1),fill='black')
sheet.save(out/'overview.png')
print('RENDERED',len(images),out)
eqroot=Path(r'C:\Users\Sui\AppData\Local\Temp\jqr_mt_20261028\equations')
manifest=json.loads((TASK/'equation_manifest.json').read_text(encoding='utf-8'))
red=[];equations=[]
for k,item in manifest.items():
    if item['number'] is not None:
        im=Image.open(eqroot/(k+'.wmf'));im.load(dpi=216);im=im.convert('RGB')
        if any(r>170 and g<80 and b<80 for r,g,b in im.getdata()):red.append((item['number'],item['tex']))
        equations.append((item['number'],im))
can=Image.new('RGB',(1400,2800),'white');dr=ImageDraw.Draw(can);heights=[10,10]
for num,im in sorted(equations):
    col=0 if num<=14 else 1;x=700*col;y=heights[col]
    dr.text((x+5,y),str(num),fill='black');can.paste(im,(x+30,y+20));heights[col]+=im.height+45
can.crop((0,0,1400,max(heights))).save(out/'equations.png')
print('RED_EQUATIONS',red)

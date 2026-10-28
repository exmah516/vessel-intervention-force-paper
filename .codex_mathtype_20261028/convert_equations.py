from pathlib import Path
import re,json,hashlib
from mathtype_native import MathType
TASK=Path(__file__).parent
EQ=Path(r'C:\Users\Sui\AppData\Local\Temp\jqr_mt_20261028')/'equations'
EQ.mkdir(exist_ok=True)
source=json.loads((TASK/'source.json').read_text(encoding='utf-8'))

def normalize(t):
    t=re.sub(r'\\bm\s*([a-zA-Z])',r'\\boldsymbol{\1}',t)
    t=t.replace(r'\bm',r'\boldsymbol')
    t=re.sub(r'\{\\rm\s+([^{}]+)\}',r'\\mathrm{\1}',t)
    t=re.sub(r'\\mathrm\s+([a-zA-Z])',r'\\mathrm{\1}',t)
    t=re.sub(r'\\(bigl|bigr|Bigl|Bigr|big|Big)\s*', '',t)
    t=t.replace(r'\!', '').replace(r'\;',r'\,')
    t=re.sub(r'\s+',' ',t).strip()
    t=t.replace('={}&','&=')
    if '&' in t and not any(r'\begin{'+e+'}' in t for e in ['aligned','align','cases']):
        t=r'\begin{aligned}'+t+r'\end{aligned}'
    t=t.replace(r'\begin{aligned}',r'\begin{align}').replace(r'\end{aligned}',r'\end{align}')
    return t

def key(t,size=10.5):
    return hashlib.sha256((f'{size:g}|'+normalize(t)).encode()).hexdigest()[:18]

items={}
def add(t,size=10.5,number=None):
    k=key(t,size)
    items[k]={'key':k,'tex':normalize(t),'size':size,'number':number}
def walk(x,size=10.5):
    if isinstance(x,dict):
        if x.get('t')=='Math':add(x['c'][1],size)
        for k,v in x.items():
            if k.endswith('_ast') or k=='blocks' or k in ['c']:walk(v,size)
    elif isinstance(x,list):
        for v in x:walk(v,size)
walk(source['blocks'])
for r in source['records'].values():
    if r['type']=='equation':add(r['tex'],10.5,r['number'])
    else:
        for k,v in r.items():
            if k.endswith('_ast'):walk(v,9)
        if 'rows' in r:
            for row in r['rows']:
                for cell in row:walk(cell['ast'],9)

def run(selected=None):
    mt=MathType()
    try:
        for i,(k,item) in enumerate(items.items()):
            if selected and item['number'] not in selected:continue
            p=EQ/k;meta=p.with_suffix('.json')
            if meta.exists():
                item.update(json.loads(meta.read_text(encoding='utf-8')));continue
            result=mt.convert(item['tex'],p,item['size']);item.update(result)
            meta.write_text(json.dumps(item,ensure_ascii=False,indent=2),encoding='utf-8')
            if item['number'] is not None or i%20==0:print(i+1,'of',len(items),'eq',item['number'],'width',item['width'],'height',item['height'],flush=True)
    finally:mt.close()
    (TASK/'equation_manifest.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':
    import sys
    run([int(v) for v in sys.argv[1:]] or None)

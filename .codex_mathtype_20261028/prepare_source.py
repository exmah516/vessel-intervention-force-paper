from pathlib import Path
import re,json,subprocess,hashlib
TASK=Path(__file__).parent
BASE=TASK.parent
SOURCE=BASE/'JQR_LaTeX_Template-0507/JQR_LaTeX_Template.tex'
text=SOURCE.read_text(encoding='utf-8')

def uncomment(s):
    return re.sub(r'(?<!\\)%[^\n]*','',s)

def group(s,pos):
    while pos<len(s) and s[pos].isspace():pos+=1
    assert s[pos]=='{',(s[pos:pos+50],pos)
    start=pos+1;level=1;pos+=1
    while level:
        if s[pos]=='{' and (pos==0 or s[pos-1]!='\\'):level+=1
        elif s[pos]=='}' and s[pos-1]!='\\':level-=1
        pos+=1
    return s[start:pos-1],pos

def unwrap(s,command):
    start=0
    while True:
        match=re.search(r'\\'+re.escape(command)+r'\s*\{',s[start:])
        if not match:return s
        a=start+match.start();value,end=group(s,a+len(command)+1)
        s=s[:a]+value+s[end:];start=a

text=uncomment(text)
setup,pos=group(text,text.index(r'\JQRsetup')+len(r'\JQRsetup'))
metadata={}
cursor=0
while True:
    match=re.search(r'([A-Za-z]+)\s*=\s*',setup[cursor:])
    if not match:break
    key=match.group(1);start=cursor+match.end()
    if setup[start]=='{':value,cursor=group(setup,start)
    else:
        end=setup.find(',',start);end=len(setup) if end<0 else end
        value=setup[start:end].strip();cursor=end
    metadata[key]=unwrap(value,'revised')
body=text.split(r'\maketitle',1)[1].split(r'\balance',1)[0]
body=unwrap(body,'revised').replace(r'\revbegin','').replace(r'\revend','\n\n')
body=body.replace(r'\RevisionColor','').replace(r'\begin{AuthorIntroduction}',r'\section*{作者简介}').replace(r'\end{AuthorIntroduction}','')
body=body.replace(r'\Intro','').replace(r'\end{document}','')
body=re.sub(r'\\begin\{enumerate\}\[[^\]]*\]',r'\\begin{enumerate}',body)

bbl=(SOURCE.parent/'JQR_LaTeX_Template.bbl').read_text(encoding='utf-8')
references=[]
matches=list(re.finditer(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',bbl))
for i,m in enumerate(matches):
    value=bbl[m.end():matches[i+1].start() if i+1<len(matches) else bbl.index(r'\end{thebibliography}')]
    value=re.sub(r'\\newblock|\\allowbreak',' ',value)
    value=value.replace(r'\natexlab','')
    references.append({'key':m.group(1),'tex':value.strip(),'number':i+1})
refmap={r['key']:r['number'] for r in references}
aux=(SOURCE.parent/'JQR_LaTeX_Template.aux').read_text(encoding='utf-8')
labels=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}',aux))
body=re.sub(r'\\ucite\{([^}]+)\}',lambda m:r'\textsuperscript{['+','.join(str(refmap[k.strip()]) for k in m.group(1).split(','))+']}',body)
body=re.sub(r'\\eqref\{([^}]+)\}',lambda m:'('+labels[m.group(1)]+')',body)
body=re.sub(r'\\ref\{([^}]+)\}',lambda m:labels[m.group(1)],body)

records={}
def register(value):
    key='JQRBLOCK%03d'%(len(records)+1);records[key]=value;return '\n\n'+key+'\n\n'
def caption(block):
    p=block.index(r'\bicaption')+len(r'\bicaption')
    cn,p=group(block,p);en,p=group(block,p)
    return cn,en
def figure(m):
    b=m.group();cn,en=caption(b);label=re.search(r'\\label\{([^}]+)\}',b).group(1)
    pic=re.search(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',b)
    value={'type':'figure','cn':cn,'en':en,'number':int(labels[label]),'label':label}
    if pic:value['image']=pic.group(1)
    else:
        p=b.index(r'\parbox')+len(r'\parbox');_,p=group(b,p);desc,p=group(b,p)
        value['placeholder']=desc.replace(r'\raggedright','').strip()
    if pic and '[待补' in b:
        value['note']=re.search(r'\[待补[^\]]*\]',b).group()
    return register(value)
body=re.sub(r'\\begin\{figure\}(?:\[[^\]]*\])?[\s\S]*?\\end\{figure\}',figure,body)
def table(m):
    b=m.group();cn,en=caption(b);label=re.search(r'\\label\{([^}]+)\}',b).group(1)
    return register({'type':'table','cn':cn,'en':en,'number':int(labels[label]),'label':label,'tex':b})
body=re.sub(r'\\begin\{table\*\}(?:\[[^\]]*\])?[\s\S]*?\\end\{table\*\}',table,body)

def split_top(s,sep=r'\\'):
    parts=[];begin=0;depth=0;i=0;env=0
    while i<len(s):
        bm=re.match(r'\\begin\{([^}]+)\}',s[i:])
        em=re.match(r'\\end\{([^}]+)\}',s[i:])
        if bm:env+=1;i+=len(bm.group());continue
        if em:env-=1;i+=len(em.group());continue
        if s[i]=='{' and (i==0 or s[i-1]!='\\'):depth+=1
        elif s[i]=='}' and (i==0 or s[i-1]!='\\'):depth-=1
        if depth==0 and env==0 and s.startswith(sep,i):
            parts.append(s[begin:i]);i+=len(sep);begin=i
        else:i+=1
    parts.append(s[begin:]);return parts

equation_counter=0
def eq(m):
    global equation_counter
    env=m.group(1);content=m.group(2)
    chunks=split_top(content) if env=='align' else [content]
    result=[];pending=''
    for chunk in chunks:
        pending+=chunk
        if r'\notag' in chunk:
            pending+=r'\\';continue
        equation_counter+=1
        lab=re.search(r'\\label\{([^}]+)\}',pending)
        label=lab.group(1) if lab else f'eq:anonymous-{equation_counter}'
        if lab:assert int(labels[label])==equation_counter,(label,equation_counter,labels[label])
        formula=re.sub(r'\\label\{[^}]+\}|\\notag','',pending).strip()
        original=formula
        if equation_counter==16:
            # Keep the entire row vector within its paired brackets. The
            # equality is the only external place to break this expression.
            rhs=re.sub(r'\\begin\{aligned\}|\\end\{aligned\}|&|\\\\','',formula).split('=',1)[1].strip()
            formula=r'\begin{aligned}&\bm x_k={}\\&'+rhs+r'\end{aligned}'
        elif equation_counter==19:
            # This full set expression fits the measured column width.
            formula=re.sub(r'\\begin\{aligned\}|\\end\{aligned\}|&|\\\\','',formula)
        elif equation_counter==25:
            # Break only at the external subtraction, with the full set and
            # all its quantified conditions retained on the preceding line.
            formula=r"\begin{aligned}&t_{\rm rec}=\inf\bigl\{t\ge t_{\rm S8,end}:|d_F(t')|\le\varepsilon_{\rm tol},\forall t'\in[t,t+t_{\rm win}]\bigr\}\\&\quad-t_{\rm S8,end}.\end{aligned}"
        result.append(register({'type':'equation','label':label,'number':equation_counter,'tex':formula,'source_tex':original}));pending=''
    assert not pending.strip()
    return ''.join(result)
body=re.sub(r'\\begin\{(equation|align)\}([\s\S]*?)\\end\{\1\}',eq,body)
body=re.sub(r'\\bibliographystyle\{[^}]+\}', '',body)
body=re.sub(r'\\bibliography\{[^}]+\}',lambda m:register({'type':'references'}),body)

# Pandoc parses prose only; original formulas and figure content stay in records.
header=r'\newcommand{\bm}[1]{\boldsymbol{#1}}'+'\n'
def parse(s):
    # Pandoc consumes the numeric token following a prose \quad. Preserve
    # intentional author/address spacing without modifying math expressions.
    pieces=re.split(r'($[^$]*$)',s)
    s=''.join(v if i%2 else re.sub(r'\\(qquad|quad)\s*',lambda m:'\u2003\u2003' if m[1]=='qquad' else '\u2003',v) for i,v in enumerate(pieces))
    result=subprocess.run([r'C:\Program Files\Pandoc\pandoc.exe','-f','latex','-t','json'],input=(header+s).encode('utf-8'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    return json.loads(result.stdout)['blocks']
ast=parse(body)
for r in records.values():
    for key in ['cn','en','placeholder','note']:
        if key in r:r[key+'_ast']=parse(r[key])
    if r['type']=='table':
        b=r['tex'];p=b.index(r'\begin{tabular}')+len(r'\begin{tabular}')
        _,p=group(b,p)
        content=b[p:b.index(r'\end{tabular}')]
        content=re.sub(r'\\(?:toprule|midrule|bottomrule)','',content).strip()
        rows=[]
        for row in split_top(content):
            if not row.strip():continue
            cells=[]
            for cell in split_top(row,sep='&'):
                span=1
                if r'\multicolumn' in cell:
                    p=cell.index(r'\multicolumn')+len(r'\multicolumn')
                    count,p=group(cell,p);_,p=group(cell,p);cell,p=group(cell,p);span=int(count)
                cell=cell.replace(r'\shortstack','')
                cells.append({'span':span,'ast':parse(cell)})
            rows.append(cells)
        r['rows']=rows
for key,value in list(metadata.items()):metadata[key+'_ast']=parse(re.sub(r'\\addr\{([^}]+)\}',r'\\textsuperscript{\1}',value))
for r in references:r['ast']=parse(r['tex'])
result={'source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'metadata':metadata,'records':records,'references':references,'blocks':ast}
(TASK/'source.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(TASK/'prepared.tex').write_text(body,encoding='utf-8')
from collections import Counter
print('BLOCKS',Counter(b['t'] for b in ast),'RECORDS',Counter(b['type'] for b in records.values()),'REFERENCES',len(references))
print('EQUATIONS',[(r['number'],r['label'],r['tex'][:60]) for r in records.values() if r['type']=='equation'])
print('RAW',[(b['t'],b.get('c')) for b in ast if b['t'].startswith('Raw')])

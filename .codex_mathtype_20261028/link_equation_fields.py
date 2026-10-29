from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
from hashlib import sha256
from lxml import etree as E
import argparse
import json
import re

TASK = Path(__file__).parent
BASE = TASK.parent
STEM = '面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_MathType'
SOURCE = BASE / (STEM + '_编辑修复版.docx')
OUTPUT = BASE / (STEM + '_公式引用联动版.docx')
MANIFEST = TASK / 'equation_fields_manifest.json'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'o': 'urn:schemas-microsoft-com:office:office',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
W = '{' + NS['w'] + '}'
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'


def read_doc(path):
    with ZipFile(path) as z:
        return {entry.filename: z.read(entry.filename) for entry in z.infolist()}


def write_doc(path, parts):
    with ZipFile(path, 'w', ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data)


def encode(root):
    return E.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)


def node(tag, **attrs):
    n = E.Element(W + tag)
    for key, value in attrs.items():
        n.set(W + key, str(value))
    return n


def number_font(source_run=None):
    p = deepcopy(source_run.find(W + 'rPr')) if source_run is not None and source_run.find(W + 'rPr') is not None else node('rPr')
    fonts = p.find(W + 'rFonts')
    if fonts is None:
        fonts = node('rFonts')
        p.insert(0, fonts)
    for attr in list(fonts.attrib):
        if attr.split('}')[-1].endswith('Theme'):
            del fonts.attrib[attr]
    for attr, val in {'ascii': 'Times New Roman', 'hAnsi': 'Times New Roman', 'eastAsia': '宋体'}.items():
        fonts.set(W + attr, val)
    return p


def run(text=None, rpr=None, child=None):
    r = node('r')
    if rpr is not None:
        r.append(deepcopy(rpr))
    if text is not None:
        t = node('t')
        t.text = text
        if text[:1].isspace() or text[-1:].isspace():
            t.set(XML_SPACE, 'preserve')
        r.append(t)
    if child is not None:
        r.append(child)
    return r


def field(code, result, rpr):
    begin = node('fldChar', fldCharType='begin', dirty='true')
    instr = node('instrText')
    instr.set(XML_SPACE, 'preserve')
    instr.text = ' ' + code + ' '
    return [run(rpr=rpr, child=begin), run(rpr=rpr, child=instr),
            run(rpr=rpr, child=node('fldChar', fldCharType='separate')),
            run(str(result), rpr=rpr),
            run(rpr=rpr, child=node('fldChar', fldCharType='end'))]


def replace_run(original, new):
    parent = original.getparent()
    pos = parent.index(original)
    parent.remove(original)
    for i, n in enumerate(new):
        parent.insert(pos + i, n)


def build():
    parts = read_doc(SOURCE)
    snapshot = TASK / 'before_equation_fields.docx'
    if not snapshot.exists():
        snapshot.write_bytes(SOURCE.read_bytes())
    root = E.fromstring(parts['word/document.xml'])
    ps = root.xpath('.//w:body/w:p', namespaces=NS)
    labels = []
    for i, p in enumerate(ps):
        text = ''.join(p.xpath('.//w:t/text()', namespaces=NS))
        m = re.fullmatch(r'\s*\((\d+)\)\s*', text)
        if m and p.xpath('.//o:OLEObject', namespaces=NS):
            labels.append((int(m[1]), i, p))
    assert len(labels) == 26, len(labels)
    mapping = {old: i + 1 for i, (old, _, _) in enumerate(labels)}
    manifest = {'source': str(SOURCE), 'source_sha256': sha256(SOURCE.read_bytes()).hexdigest(),
                'output': str(OUTPUT), 'mapping': mapping, 'equations': [], 'references': []}
    for old, index, p in labels:
        name = 'JQR_eq_' + str(old)
        starts = p.xpath('./w:bookmarkStart[@w:name="' + name + '"]', namespaces=NS)
        assert len(starts) == 1, name
        bookmark_id = starts[0].get(W + 'id')
        ends = p.xpath('./w:bookmarkEnd[@w:id="' + bookmark_id + '"]', namespaces=NS)
        assert len(ends) == 1
        p.remove(starts[0])
        p.remove(ends[0])
        ts = p.xpath('./w:r/w:t', namespaces=NS)
        assert len(ts) == 1, name
        source_run = ts[0].getparent()
        rpr = number_font(source_run)
        new = [run('(', rpr), node('bookmarkStart', id=bookmark_id, name=name)]
        new += field('SEQ JQREquation \\* ARABIC', mapping[old], rpr)
        new += [node('bookmarkEnd', id=bookmark_id), run(')', rpr)]
        replace_run(source_run, new)
        manifest['equations'].append({'old': old, 'number': mapping[old], 'paragraph': index,
                                      'bookmark': name, 'bookmark_id': bookmark_id})
    equation_paragraphs = {id(p) for _, _, p in labels}
    for index, p in enumerate(ps):
        if id(p) in equation_paragraphs:
            continue
        for t in list(p.xpath('.//w:t', namespaces=NS)):
            text = t.text or ''
            matches = list(re.finditer(r'式\s*[（(](\d+)[）)]', text))
            if not matches:
                continue
            source_run = t.getparent()
            assert source_run.tag == W + 'r'
            assert len(source_run.xpath('./w:t', namespaces=NS)) == 1
            assert all(c.tag in {W + 't', W + 'rPr'} for c in source_run)
            rpr = source_run.find(W + 'rPr')
            npr = number_font(source_run)
            new = []
            start = 0
            for m in matches:
                old = int(m[1])
                assert old in mapping, ('reference target deleted', old)
                # Only the digits are fields: Chinese prose and paired punctuation stay intact.
                if m.start(1) > start:
                    new.append(run(text[start:m.start(1)], rpr))
                name = 'JQR_eq_' + str(old)
                new += field('REF ' + name + ' \\h', mapping[old], npr)
                manifest['references'].append({'paragraph': index, 'old': old,
                                               'number': mapping[old], 'bookmark': name})
                start = m.end(1)
            if start < len(text):
                new.append(run(text[start:], rpr))
            replace_run(source_run, new)
    assert len(manifest['references']) == 5, len(manifest['references'])
    settings = E.fromstring(parts['word/settings.xml'])
    update = settings.find(W + 'updateFields')
    if update is None:
        update = node('updateFields')
        compat = settings.find(W + 'compat')
        settings.insert(settings.index(compat) + 1 if compat is not None else len(settings), update)
    update.set(W + 'val', 'true')
    parts['word/document.xml'] = encode(root)
    parts['word/settings.xml'] = encode(settings)
    write_doc(OUTPUT, parts)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    audit(OUTPUT)
    print('BUILT', OUTPUT)


def restore_fonts(path):
    parts = read_doc(path)
    root = E.fromstring(parts['word/styles.xml'])
    before = E.fromstring(read_doc(TASK / 'before_equation_fields.docx')['word/styles.xml'])
    fonts_by_name = {}
    for s in before.findall(W + 'style'):
        name = s.find(W + 'name')
        f = s.find(W + 'rPr/' + W + 'rFonts')
        if name is not None and f is not None:
            fonts_by_name[name.get(W + 'val')] = dict(f.attrib)
    count = 0
    for s in root.findall(W + 'style'):
        name = s.find(W + 'name')
        pr = s.find(W + 'rPr')
        if pr is None:
            pr = node('rPr')
            s.append(pr)
        f = pr.find(W + 'rFonts')
        if f is None:
            f = node('rFonts')
            pr.insert(0, f)
        fallback = fonts_by_name.get(name.get(W + 'val') if name is not None else '', {})
        for attr in list(f.attrib):
            if attr.split('}')[-1].endswith('Theme'):
                del f.attrib[attr]
        for attr, default in [('ascii', 'Times New Roman'), ('hAnsi', 'Times New Roman'), ('eastAsia', '宋体')]:
            f.set(W + attr, fallback.get(W + attr, f.get(W + attr, default)))
        count += 1
    parts['word/styles.xml'] = encode(root)
    settings = E.fromstring(parts['word/settings.xml'])
    update = settings.find(W + 'updateFields')
    if update is None:
        update = node('updateFields')
        compat = settings.find(W + 'compat')
        settings.insert(settings.index(compat) + 1 if compat is not None else len(settings), update)
    update.set(W + 'val', 'true')
    parts['word/settings.xml'] = encode(settings)
    write_doc(path, parts)
    print('FONT_DECLARATIONS_RESTORED', count)


def audit(path):
    parts = read_doc(path)
    before = read_doc(TASK / 'before_equation_fields.docx')
    root = E.fromstring(parts['word/document.xml'])
    oldroot = E.fromstring(before['word/document.xml'])
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    mapping = {int(k): v for k, v in manifest['mapping'].items()}
    ps = root.xpath('.//w:body/w:p', namespaces=NS)
    oldps = oldroot.xpath('.//w:body/w:p', namespaces=NS)
    assert len(ps) == len(oldps)
    expected = [''.join(p.xpath('.//w:t/text()', namespaces=NS)) for p in oldps]
    for x in manifest['equations']:
        expected[x['paragraph']] = '(' + str(x['number']) + ')'
    for x in manifest['references']:
        i, old = x['paragraph'], x['old']
        expected[i] = re.sub(r'(式\s*[（(])' + str(old) + r'(?=[）)])', lambda m: m[1] + str(mapping[old]), expected[i])
    actual = [''.join(p.xpath('.//w:t/text()', namespaces=NS)) for p in ps]
    assert actual == expected, [(i, a, b) for i, (a, b) in enumerate(zip(actual, expected)) if a != b]
    ole = root.xpath('.//o:OLEObject', namespaces=NS)
    oldole = oldroot.xpath('.//o:OLEObject', namespaces=NS)
    assert len(ole) == len(oldole) == 168
    # Word may rewrite compound-file bookkeeping on save; native mathematical streams
    # are verified separately if binary serialization changes.
    changed_embeddings = [n for n in before if n.startswith('word/embeddings/') and n.endswith('.bin') and before[n] != parts.get(n)]
    fields = root.xpath('.//w:instrText/text()|.//w:fldSimple/@w:instr', namespaces=NS)
    seqs = [s for s in fields if s.strip().startswith('SEQ JQREquation')]
    refs = [s for s in fields if s.strip().startswith('REF JQR_eq_')]
    assert len(seqs) == 26 and len(refs) == 5, (len(seqs), len(refs))
    assert all('\\h' in s for s in refs)
    assert not root.xpath('.//w:numPr', namespaces=NS)
    assert not E.fromstring(parts['word/styles.xml']).xpath('.//w:numPr', namespaces=NS)
    names = root.xpath('.//w:bookmarkStart/@w:name', namespaces=NS)
    assert len(names) == len(set(names))
    assert all(x['bookmark'] in names for x in manifest['equations'])
    for x in manifest['equations']:
        p = ps[x['paragraph']]
        begin = p.xpath('./w:bookmarkStart[@w:name="' + x['bookmark'] + '"]', namespaces=NS)[0]
        end = p.xpath('./w:bookmarkEnd[@w:id="' + begin.get(W + 'id') + '"]', namespaces=NS)[0]
        content = list(p)[p.index(begin) + 1:p.index(end)]
        assert not any(c.xpath('.//o:OLEObject', namespaces=NS) for c in content)
        assert ''.join(''.join(c.xpath('.//w:t/text()', namespaces=NS)) for c in content) == str(x['number'])
    styles = E.fromstring(parts['word/styles.xml']).findall(W + 'style')
    missing_fonts = []
    for s in styles:
        f = s.find(W + 'rPr/' + W + 'rFonts')
        if f is None or any(f.get(W + a) is None for a in ['ascii', 'hAnsi', 'eastAsia']):
            missing_fonts.append(s.get(W + 'styleId'))
    report = {'path': str(path), 'sha256': sha256(path.read_bytes()).hexdigest(),
              'paragraphs': len(ps), 'equations': len(seqs), 'refs': len(refs),
              'mathtype_objects': len(ole), 'changed_embedding_part_count': len(changed_embeddings),
              'styles': len(styles), 'styles_missing_explicit_fonts': missing_fonts,
              'text_preserved_except_number_fields': True, 'automatic_list_numbering': 0}
    (TASK / 'equation_fields_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['build', 'restore', 'audit'])
    parser.add_argument('path', nargs='?', type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.action == 'build':
        build()
    elif args.action == 'restore':
        restore_fonts(args.path)
        audit(args.path)
    else:
        audit(args.path)

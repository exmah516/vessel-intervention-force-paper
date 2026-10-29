"""Replace layout-only MathType matrices with native relational piles.

Keep the current Word manuscript, field numbering, and actual matrix/cases
structures.  Preserve the mathematical and formatting records byte for byte.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
import argparse
import ctypes as C
import hashlib
import json
import posixpath
import re
from collections import Counter

from mathtype_native import MathType
from mtef_structure import Equation
from probe_native_multiline import change
import repair_current_equations as native

TASK = Path(__file__).parent
SOURCE = TASK.parent / '面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_MathType_公式引用联动版.docx'
OUTPUT = TASK.parent / '面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_MathType_自然多行版.docx'
SNAPSHOT = TASK / 'before_native_multiline.docx'
CACHE = TASK / 'native_multiline_final'
REPORT = TASK / 'native_multiline_audit.json'
EXPECTED_SOURCE = 'fc33dd7b724df51d1b59300300fbeea7ebab7faebf27ec1717d8a24fb0dfd30e'
REPLACE = {1, 2, 3, 11, 13, 14, 17, 20, 22, 23, 26, 27}
NS, Q = native.NS, native.Q
SHA = lambda b: hashlib.sha256(b).hexdigest()


def parts(path):
    with ZipFile(path) as z:
        return {n: z.read(n) for n in z.namelist()}


def encode(root):
    return E.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)


def targets(data):
    return {r.get('Id'): posixpath.normpath('word/' + r.get('Target'))
            for r in E.fromstring(data['word/_rels/document.xml.rels'])
            if r.get('TargetMode') != 'External'}


def math_signature(eq):
    # LINE, PILE and MATRIX are the only intentionally altered records.
    # Check every other record, including font/size/color changes, in order.
    return SHA(b''.join(bytes([r.kind]) + len(r.prefix).to_bytes(4, 'little') + r.prefix
                        for r in eq.walk() if r.kind not in [1, 4, 5]))


def effective_style_signature(eq):
    # The native MathType saver removes redundant color resets (0 then 1
    # with no intervening mathematical content). Compare the effective
    # color of every retained record instead of counting these no-op pairs.
    current_color = b''
    records = []
    for r in eq.walk():
        if r.kind == 15:
            current_color = r.prefix
        elif r.kind not in [1, 4, 5]:
            records.append(bytes([r.kind]) + len(current_color).to_bytes(4, 'little')
                           + current_color + len(r.prefix).to_bytes(4, 'little') + r.prefix)
    return SHA(b''.join(records))


def connect():
    CACHE.mkdir(exist_ok=True)
    native.WORK = CACHE
    mt = MathType()
    mt.ole.StgOpenStorage.argtypes = [C.c_wchar_p, C.c_void_p, C.c_uint,
                                     C.c_void_p, C.c_uint, C.POINTER(C.c_void_p)]
    mt.d.MTXFormSetTranslator.argtypes = [C.c_short, C.c_char_p]
    mt.d.MTXFormSetTranslator.restype = C.c_int
    return mt


def paragraph_of(o):
    return next(a for a in o.iterancestors() if a.tag == Q('w:p'))


def old_number(o):
    names = paragraph_of(o).xpath('./w:bookmarkStart/@w:name', namespaces=NS)
    matched = [int(s.split('_')[-1]) for s in names if s.startswith('JQR_eq_')]
    assert len(matched) <= 1
    return matched[0] if matched else None


def document_contract(data):
    root = E.fromstring(data['word/document.xml'])
    ps = root.xpath('.//w:body/w:p', namespaces=NS)
    instructions = root.xpath('.//w:instrText/text()|.//w:fldSimple/@w:instr', namespaces=NS)
    seq = [s.strip() for s in instructions if s.strip().startswith('SEQ JQREquation')]
    refs = [s.strip() for s in instructions if s.strip().startswith('REF JQR_eq_')]
    ole = root.xpath('.//o:OLEObject', namespaces=NS)
    styles = E.fromstring(data['word/styles.xml'])
    assert len(ps) == 204 and len(seq) == 26 and len(refs) == 5 and len(ole) == 168
    assert all(o.get('ProgID') == 'Equation.DSMT4' for o in ole)
    assert not root.xpath('.//w:numPr', namespaces=NS)
    assert not styles.xpath('.//w:numPr', namespaces=NS)
    missing = []
    for s in styles.findall(Q('w:style')):
        f = s.find('w:rPr/w:rFonts', NS)
        if f is None or any(f.get(Q('w:' + a)) is None for a in ['ascii', 'hAnsi', 'eastAsia']):
            missing.append(s.get(Q('w:styleId')))
    assert not missing, missing
    return {
        'paragraph_texts': [''.join(p.xpath('.//w:t/text()', namespaces=NS)) for p in ps],
        'field_instructions': instructions,
        'equation_numbers': [''.join(paragraph_of(o).xpath('.//w:t/text()', namespaces=NS))
                             for o in ole if old_number(o) is not None],
        'bookmarks': root.xpath('.//w:bookmarkStart/@w:name', namespaces=NS),
    }


def build():
    assert SHA(SOURCE.read_bytes()) == EXPECTED_SOURCE, 'Latest source changed; inspect before proceeding'
    if not SNAPSHOT.exists():
        SNAPSHOT.write_bytes(SOURCE.read_bytes())
    assert SHA(SNAPSHOT.read_bytes()) == EXPECTED_SOURCE
    data = parts(SOURCE)
    before_contract = document_contract(data)
    root = E.fromstring(data['word/document.xml'])
    rel = targets(data)
    ole = root.xpath('.//o:OLEObject', namespaces=NS)
    native_uses = Counter(rel[o.get(Q('r:id'))] for o in ole)
    image_uses = Counter(rel[s] for s in root.xpath('.//v:imagedata/@r:id', namespaces=NS))
    mt = connect()
    report = {'source': str(SOURCE), 'source_sha256': EXPECTED_SOURCE,
              'output': str(OUTPUT), 'objects': []}
    try:
        for i, o in enumerate(ole, 1):
            num = old_number(o)
            target = rel[o.get(Q('r:id'))]
            original = native.read_native(mt, data[target], i)
            assert native.BAD not in original
            eq = Equation.parse(original)
            before = eq.layout()
            sig = math_signature(eq)
            result = {'occurrence': i, 'original_bookmark_number': num,
                      'native_part': target, 'source_mtef_sha256': SHA(original),
                      'math_and_style_signature': sig, 'before_layout': before,
                      'changed': num in REPLACE}
            if num in REPLACE:
                changes = change(eq)
                assert len(changes) == 1, (i, num, changes)
                assert math_signature(eq) == sig, (i, 'Math or style content changed')
                updated = eq.encode()
                assert updated != original and native.BAD not in updated
                for translator in ['Texvc.tdl', 'Texvc (DataObject).tdl']:
                    assert native.translate(mt, updated, translator) == 0, (i, translator)
                output = native.save_native(mt, updated, i)
                assert native_uses[target] == 1
                data[target] = output['binary']
                obj = o.getparent()
                shape = obj.find('v:shape', NS)
                preview = rel[shape.find('v:imagedata', NS).get(Q('r:id'))]
                assert preview.endswith('.wmf') and image_uses[preview] == 1, preview
                data[preview] = output['wmf']
                style = re.sub(r'(?<![-\w])width:[^;]+', f"width:{output['width']:g}pt", shape.get('style'))
                style = re.sub(r'(?<![-\w])height:[^;]+', f"height:{output['height']:g}pt", style)
                shape.set('style', style)
                obj.set(Q('w:dxaOrig'), str(round(output['width'] * 20)))
                obj.set(Q('w:dyaOrig'), str(round(output['height'] * 20)))
                run = obj.getparent()
                rpr = run.find('w:rPr', NS)
                if rpr is None:
                    rpr = E.Element(Q('w:rPr'))
                    run.insert(0, rpr)
                position = rpr.find('w:position', NS)
                if position is None:
                    position = E.SubElement(rpr, Q('w:position'))
                position.set(Q('w:val'), str(round(-output['baseline'] * 2)))
                result.update(preview_part=preview, width=output['width'],
                              height=output['height'], baseline=output['baseline'])
                print('CONVERTED', i, 'bookmark', num, 'native_layout', eq.layout(), flush=True)
            else:
                updated = original
                # Only the actual piecewise definition may retain hjust=0.
                assert num == 21 or not any(x['kind'] == 5 and x['hjust'] == 0 for x in before)
            result.update(output_mtef_sha256=SHA(updated), after_layout=eq.layout())
            report['objects'].append(result)
    finally:
        mt.close()
    data['word/document.xml'] = encode(root)
    assert document_contract(data) == before_contract
    changed = [r for r in report['objects'] if r['changed']]
    assert len(changed) == 12
    report.update(changed_objects=12,
                  converted_multiline_piles=sum(any(x['kind'] == 4 and x['halign'] == 4 for x in r['after_layout']) for r in changed),
                  removed_single_row_wrappers=3,
                  remaining_matrices=sum(x['kind'] == 5 for r in report['objects'] for x in r['after_layout']),
                  preserved_document_text_fields_bookmarks=True)
    assert report['converted_multiline_piles'] == 9 and report['remaining_matrices'] == 3
    with ZipFile(OUTPUT, 'w', ZIP_DEFLATED) as z:
        for name, value in data.items():
            z.writestr(name, value)
    report['built_sha256'] = SHA(OUTPUT.read_bytes())
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('BUILT', OUTPUT, 'changed', len(changed), flush=True)


def verify():
    expected = json.loads(REPORT.read_text(encoding='utf-8'))
    before, after = parts(SNAPSHOT), parts(OUTPUT)
    assert document_contract(before) == document_contract(after), 'Text, fields, numbers or bookmarks changed'
    root = E.fromstring(after['word/document.xml'])
    rel = targets(after)
    result = []
    mt = connect()
    try:
        for i, (o, info) in enumerate(zip(root.xpath('.//o:OLEObject', namespaces=NS), expected['objects'], strict=True), 1):
            data = native.read_native(mt, after[rel[o.get(Q('r:id'))]], i)
            eq = Equation.parse(data)
            if info['changed']:
                raw = (CACHE / f'fixed_{i:03d}.mtef').read_bytes()
                persisted = native.read_native(mt, (CACHE / f'fixed_{i:03d}.bin').read_bytes(), 2000 + i)
                raw_eq = Equation.parse(raw)
                assert math_signature(raw_eq) == info['math_and_style_signature']
                assert raw_eq.signature() == eq.signature(), (i, 'Mathematical records changed')
                assert effective_style_signature(raw_eq) == effective_style_signature(eq), (i, 'Effective styles changed')
                assert data == persisted, (i, 'Word changed the saved MathType native stream')
            else:
                assert SHA(data) == info['output_mtef_sha256'], (i, 'Unmodified expression changed')
                assert math_signature(eq) == info['math_and_style_signature'], (i, 'Math/style signature mismatch')
            assert eq.layout() == info['after_layout'], (i, 'Layout mismatch')
            assert native.BAD not in data
            for translator in ['Texvc.tdl', 'Texvc (DataObject).tdl']:
                assert native.translate(mt, data, translator) == 0, (i, translator)
            result.append({'occurrence': i, 'changed': info['changed'], 'layout': eq.layout(),
                           'math_and_style_preserved': True, 'both_translators_passed': True})
    finally:
        mt.close()
    final = {'path': str(OUTPUT), 'sha256': SHA(OUTPUT.read_bytes()),
             'source_unchanged': SHA(SOURCE.read_bytes()) == EXPECTED_SOURCE,
             'mathtype_objects': len(result), 'changed_objects': 12,
             'native_multiline_conversions': 9, 'single_row_wrappers_removed': 3,
             'text_fields_and_bookmarks_preserved': True, 'all_math_and_styles_preserved': True,
             'both_native_translators_passed': len(result), 'objects': result}
    (TASK / 'native_multiline_verification.json').write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in final.items() if k != 'objects'}, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['build', 'verify'])
    args = parser.parse_args()
    build() if args.action == 'build' else verify()

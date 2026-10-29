from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
from lxml import etree as E
import ctypes as C
import json
import posixpath
from mtef_structure import Equation, Record, line, pile
from mathtype_native import MathType
import repair_current_equations as native

TASK = Path(__file__).parent
SOURCE = TASK.parent / '面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_MathType_公式引用联动版.docx'
PROBE = TASK / 'native_multiline_probes'
PROBE.mkdir(exist_ok=True)
native.WORK = PROBE
NS = native.NS


def aligned_from_matrix(m):
    rows, cols = m.attrs['rows'], m.attrs['cols']
    cells = []
    pending = []
    for c in m.children:
        if c.kind == 1:
            cells.append(line(deepcopy(pending + (c.children or []))))
            pending = []
        else:
            assert c.kind in [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
            pending.append(c)
    if pending:
        cells[-1].children += deepcopy(pending)
    assert len(cells) == rows * cols
    lines = []
    for i in range(rows):
        row_cells = cells[i * cols:(i + 1) * cols]
        contents = []
        for cell in row_cells:
            contents += deepcopy(cell.children or [])
        lines.append(line(contents))
    return pile(lines)


def change(eq):
    found = []
    def visit(records):
        for i, r in enumerate(records):
            # hjust=0 comes from a TeX align/array, rather than an actual bmatrix.
            if r.kind == 5 and r.attrs['hjust'] == 0:
                if r.attrs['rows'] == 1:
                    joined = aligned_from_matrix(r).children[0]
                    records[i:i + 1] = joined.children
                else:
                    records[i] = aligned_from_matrix(r)
                found.append(r.attrs)
                # True nested matrices (hjust=1) are kept intact.
            elif r.children is not None:
                visit(r.children)
    visit(eq.records)
    return found


def main():
    mt = MathType()
    mt.ole.StgOpenStorage.argtypes = [C.c_wchar_p, C.c_void_p, C.c_uint, C.c_void_p, C.c_uint, C.POINTER(C.c_void_p)]
    mt.d.MTXFormSetTranslator.argtypes = [C.c_short, C.c_char_p]
    mt.d.MTXFormSetTranslator.restype = C.c_int
    try:
        with ZipFile(SOURCE) as z:
            root = E.fromstring(z.read('word/document.xml'))
            rels = E.fromstring(z.read('word/_rels/document.xml.rels'))
            targets = {r.get('Id'): posixpath.normpath('word/' + r.get('Target')) for r in rels if r.get('TargetMode') != 'External'}
            for p in root.xpath('.//w:body/w:p', namespaces=NS):
                bookmarks = p.xpath('./w:bookmarkStart/@w:name', namespaces=NS)
                if not any(s.startswith('JQR_eq_') for s in bookmarks):
                    continue
                old = int(next(s for s in bookmarks if s.startswith('JQR_eq_')).split('_')[-1])
                if old not in [1, 2, 11, 13, 14, 17, 20, 21, 22, 23, 26]:
                    continue
                o = p.xpath('.//o:OLEObject', namespaces=NS)[0]
                data = native.read_native(mt, z.read(targets[o.get(native.Q('r:id'))]), old)
                eq = Equation.parse(data)
                signature = eq.signature()
                print('BEFORE', old, eq.layout(), flush=True)
                transforms = change(eq)
                assert eq.signature() == signature
                updated = eq.encode()
                result = native.save_native(mt, updated, old)
                assert native.translate(mt, updated, 'Texvc.tdl') == 0
                assert native.translate(mt, updated, 'Texvc (DataObject).tdl') == 0
                (PROBE / f'eq_{old:02d}.json').write_text(json.dumps({'old': old, 'changed': transforms, 'after': eq.layout(), 'width': result['width'], 'height': result['height'], 'baseline': result['baseline']}, ensure_ascii=False, indent=2), encoding='utf-8')
                print('AFTER', old, result['width'], result['height'], result['baseline'], eq.layout(), flush=True)
    finally:
        mt.close()


if __name__ == '__main__':
    main()

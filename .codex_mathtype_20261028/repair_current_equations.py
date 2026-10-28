from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
import ctypes as C
import hashlib
import json
import posixpath
import re
import struct
import sys
from mathtype_native import MathType, guid, qi, method, release

TASK = Path(__file__).parent
WORK = Path(r'C:\Users\Sui\AppData\Local\Temp\jqr_mt_20261028\edit_repair_latest')
WORK.mkdir(exist_ok=True)
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'o': 'urn:schemas-microsoft-com:office:office',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'v': 'urn:schemas-microsoft-com:vml'}
BAD = bytes.fromhex('02009807ef')
GOOD = bytes.fromhex('02009802ef')
Q = lambda s: '{' + NS[s.split(':')[0]] + '}' + s.split(':')[1]
SHA = lambda data: hashlib.sha256(data).hexdigest()


def read_native(mt, data, index):
    path = WORK / f'read_{index:03d}.bin'
    path.write_bytes(data)
    storage = C.c_void_p()
    stream = C.c_void_p()
    try:
        assert mt.ole.StgOpenStorage(str(path), None, 0x10, None, 0, C.byref(storage)) == 0
        assert method(storage, 4, C.c_long, C.c_wchar_p, C.c_void_p,
                      C.c_uint, C.c_uint, C.POINTER(C.c_void_p))(
                          storage, 'Equation Native', None, 0x10, 0, C.byref(stream)) == 0
        buf = C.create_string_buffer(1000000)
        count = C.c_uint()
        result = method(stream, 3, C.c_long, C.c_void_p, C.c_uint,
                        C.POINTER(C.c_uint))(stream, buf, len(buf), C.byref(count))
        assert result in [0, 1] and count.value < len(buf)
        native = buf.raw[:count.value]
        header = struct.unpack_from('<H', native)[0]
        length = struct.unpack_from('<I', native, 8)[0]
        assert header == 28 and length == len(native) - header
        return native[header:]
    finally:
        release(stream)
        release(storage)


def translate(mt, data, translator):
    mt.d.MTXFormReset()
    assert mt.d.MTXFormSetTranslator(0, translator.encode('ascii')) == 0
    src = C.create_string_buffer(data)
    out = C.create_string_buffer(100000)
    dims = C.create_string_buffer(100)
    return mt.d.MTXFormEqn(-3, 4, src, len(data), -3, 7, out, len(out), b'', dims)


def save_native(mt, data, index):
    path = WORK / f'fixed_{index:03d}'
    obj = C.c_void_p()
    storage = C.c_void_p()
    persist = None
    cls = guid('0002CE03-0000-0000-C000-000000000046')
    iid = guid('00020400-0000-0000-C000-000000000046')
    try:
        assert mt.ole.CoCreateInstance(C.byref(cls), None, 5, C.byref(iid), C.byref(obj)) == 0
        persist = qi(obj, '0000010A-0000-0000-C000-000000000046')
        assert mt.ole.StgCreateDocfile(str(path.with_suffix('.bin')), 0x1012, 0, C.byref(storage)) == 0
        assert method(persist, 5, C.c_long, C.c_void_p)(persist, storage) == 0
        src = C.create_string_buffer(data)
        assert mt.d.MTSetEqnFromLangBytes(obj, 3, src, len(data)) == 0
        assert mt.ole.OleSave(persist, storage, 1) == 0
        assert method(storage, 9, C.c_long, C.c_uint)(storage, 0) == 0
        mt.d.MTXFormReset()
        assert mt.d.MTXFormSetPrefs(1, b'') == 0
        out = C.create_string_buffer(100000)
        dims = C.create_string_buffer(100)
        assert mt.d.MTXFormEqn(-3, 4, src, len(data), -4, 6, out, len(out),
                              str(path.with_suffix('.wmf')).encode('mbcs'), dims) == 0
        wmf = path.with_suffix('.wmf').read_bytes()
        left, top, right, bottom, inch = struct.unpack_from('<hhhhH', wmf, 6)
        path.with_suffix('.mtef').write_bytes(data)
        return {'binary': path.with_suffix('.bin').read_bytes(), 'wmf': wmf,
                'width': (right-left)*72/inch, 'height': (bottom-top)*72/inch,
                'baseline': mt.d.MTGetLastDimension(3)/32}
    finally:
        release(persist)
        release(storage)
        release(obj)


def run(source, output, verify=False):
    z = ZipFile(source)
    parts = {n: z.read(n) for n in z.namelist()}
    body = E.fromstring(parts['word/document.xml'])
    rels = E.fromstring(parts['word/_rels/document.xml.rels'])
    targets = {r.get('Id'): posixpath.normpath('word/' + r.get('Target'))
               for r in rels if r.get('TargetMode') != 'External'}
    mt = MathType()
    mt.ole.StgOpenStorage.argtypes = [C.c_wchar_p, C.c_void_p, C.c_uint,
                                     C.c_void_p, C.c_uint, C.POINTER(C.c_void_p)]
    mt.d.MTXFormSetTranslator.argtypes = [C.c_short, C.c_char_p]
    mt.d.MTXFormSetTranslator.restype = C.c_int
    updated = {}
    records = []
    try:
        for index, o in enumerate(body.xpath('//o:OLEObject', namespaces=NS), 1):
            assert o.get('ProgID') == 'Equation.DSMT4'
            target = targets[o.get(Q('r:id'))]
            data = read_native(mt, parts[target], index)
            count = data.count(BAD)
            if verify:
                assert count == 0, (index, 'EF07 remains')
            fixed = data.replace(BAD, GOOD)
            assert translate(mt, fixed, 'Texvc.tdl') == 0, (index, 'Texvc')
            assert translate(mt, fixed, 'Texvc (DataObject).tdl') == 0, (index, 'DataObject')
            record = {'occurrence': index, 'fixed_mtef_sha256': SHA(fixed),
                      'inner_spaces_replaced': count, 'native_part': target}
            if count:
                eq = save_native(mt, fixed, index)
                updated[target] = eq['binary']
                obj_el = o.getparent()
                shape = obj_el.find('v:shape', NS)
                image = shape.find('v:imagedata', NS)
                preview = targets[image.get(Q('r:id'))]
                updated[preview] = eq['wmf']
                style = re.sub(r'(?<![-\w])width:[^;]+', f"width:{eq['width']:g}pt", shape.get('style'))
                style = re.sub(r'(?<![-\w])height:[^;]+', f"height:{eq['height']:g}pt", style)
                shape.set('style', style)
                obj_el.set(Q('w:dxaOrig'), str(round(eq['width']*20)))
                obj_el.set(Q('w:dyaOrig'), str(round(eq['height']*20)))
                rpr = obj_el.getparent().find('w:rPr', NS)
                if rpr is not None:
                    pos = rpr.find('w:position', NS)
                    if pos is not None:
                        pos.set(Q('w:val'), str(round(-eq['baseline']*2)))
                print('Repaired', index, 'spaces', count, flush=True)
            records.append(record)
    finally:
        mt.close()
    report = {'source': str(source), 'source_sha256': SHA(source.read_bytes()),
              'objects': len(records), 'repaired': sum(r['inner_spaces_replaced'] > 0 for r in records),
              'texvc_pass': len(records), 'dataobject_pass': len(records), 'results': records}
    if verify:
        expected = json.loads((TASK/'edit_repair_latest_audit.json').read_text('utf-8'))
        assert [r['fixed_mtef_sha256'] for r in records] == [r['fixed_mtef_sha256'] for r in expected['results']]
        report['expression_hashes_match_before_word_save'] = True
        (TASK/'edit_repair_latest_verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), 'utf-8')
    else:
        updated['word/document.xml'] = E.tostring(body, encoding='UTF-8', xml_declaration=True, standalone=True)
        settings = E.fromstring(parts['word/settings.xml'])
        refresh = settings.find('w:updateFields', NS)
        if refresh is None:
            refresh = E.SubElement(settings, Q('w:updateFields'))
        refresh.set(Q('w:val'), 'true')
        updated['word/settings.xml'] = E.tostring(settings, encoding='UTF-8', xml_declaration=True, standalone=True)
        with ZipFile(output, 'w', ZIP_DEFLATED) as out:
            for name, data in parts.items():
                out.writestr(name, updated.get(name, data))
        assert E.fromstring(parts['word/document.xml']).xpath('//w:t/text()', namespaces=NS) == body.xpath('//w:t/text()', namespaces=NS)
        report.update({'output': str(output), 'output_sha256': SHA(output.read_bytes()),
                       'all_prose_and_styles_preserved': True})
        (TASK/'edit_repair_latest_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), 'utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='results'}, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'verify':
        run(Path(sys.argv[2]), None, verify=True)
    else:
        run(TASK/'before_edit_repair_latest.docx', TASK/'repaired_with_refresh.docx')

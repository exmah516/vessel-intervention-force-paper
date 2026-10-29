"""Read and preserve MTEF5 records; layout mutations use MathType's native piles."""
from dataclasses import dataclass, field
import struct


@dataclass
class Record:
    kind: int
    prefix: bytes
    children: list | None = None
    attrs: dict = field(default_factory=dict)

    def encode(self):
        if self.children is None:
            return self.prefix
        return self.prefix + b''.join(x.encode() for x in self.children) + b'\0'

    def walk(self):
        yield self
        for c in self.children or []:
            yield from c.walk()


class Reader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def byte(self):
        b = self.data[self.pos]
        self.pos += 1
        return b

    def uint(self):
        b = self.byte()
        if b == 255:
            b = struct.unpack_from('<H', self.data, self.pos)[0]
            self.pos += 2
        return b

    def string(self):
        start = self.pos
        self.pos = self.data.index(0, start) + 1
        return self.data[start:self.pos - 1]

    def nudge(self, opts):
        if opts & 8:
            a, b = self.byte(), self.byte()
            if a == b == 128:
                self.pos += 4

    def dims(self):
        count = self.byte()
        end_count = 0
        while end_count < count:
            b = self.byte()
            end_count += (b >> 4 == 15) + (b & 15 == 15)
        assert end_count == count

    def records(self):
        result = []
        while self.data[self.pos] != 0:
            result.append(self.record())
        self.pos += 1
        return result

    def record(self):
        start = self.pos
        k = self.byte()
        attrs = {}
        children = False
        if k in [1, 2, 3, 4, 5, 6]:
            opts = self.byte()
            attrs['opts'] = opts
            self.nudge(opts)
            if k == 1:
                if opts & 4:
                    attrs['line_spacing'] = struct.unpack_from('<H', self.data, self.pos)[0]
                    self.pos += 2
                if opts & 2:
                    self.record()
                children = not (opts & 1)
            elif k == 2:
                attrs['typeface'] = self.uint() - 128
                if not opts & 32:
                    attrs['char'] = struct.unpack_from('<H', self.data, self.pos)[0]
                    self.pos += 2
                if opts & 4:
                    self.pos += 1
                if opts & 16:
                    self.pos += 2
                children = bool(opts & 1)
            elif k == 3:
                attrs['selector'] = self.byte()
                variation = self.byte()
                if variation & 128:
                    variation = (variation & 127) | self.byte() << 8
                attrs['variation'] = variation
                attrs['template_options'] = self.byte()
                children = True
            elif k == 4:
                attrs['halign'], attrs['valign'] = self.byte(), self.byte()
                if opts & 2:
                    self.record()
                children = True
            elif k == 5:
                attrs['valign'], attrs['hjust'], attrs['vjust'] = self.byte(), self.byte(), self.byte()
                attrs['rows'], attrs['cols'] = self.byte(), self.byte()
                self.pos += (attrs['rows'] + 4) // 4 + (attrs['cols'] + 4) // 4
                children = True
            elif k == 6:
                attrs['embell'] = self.byte()
        elif k == 7:
            count = self.byte()
            attrs['stops'] = []
            for _ in range(count):
                align = self.byte()
                offset = struct.unpack_from('<H', self.data, self.pos)[0]
                self.pos += 2
                attrs['stops'].append((align, offset))
        elif k == 8:
            self.uint()
            self.pos += 1
        elif k == 9:
            size = self.byte()
            if size == 101:
                self.pos += 2
            elif size == 100:
                self.pos += 3
            else:
                self.pos += 1
        elif k in [10, 11, 12, 13, 14]:
            pass
        elif k == 15:
            self.uint()
        elif k == 16:
            opts = self.byte()
            self.pos += 8 if opts & 1 else 6
            if opts & 4:
                self.string()
        elif k == 17:
            self.uint()
            self.string()
        elif k == 18:
            self.byte()
            self.dims()
            self.dims()
            count = self.byte()
            for _ in range(count):
                if self.uint():
                    self.byte()
        elif k == 19:
            self.string()
        elif k >= 100:
            self.pos += self.uint()
        else:
            raise ValueError(('unknown record', k, start, self.data[start:start + 24].hex()))
        prefix = self.data[start:self.pos]
        child_list = self.records() if children else None
        record = Record(k, prefix, child_list, attrs)
        assert record.encode() == self.data[start:self.pos]
        return record


@dataclass
class Equation:
    header: bytes
    records: list

    @classmethod
    def parse(cls, data):
        reader = Reader(data)
        assert reader.data[0] == 5
        reader.pos = 5
        reader.string()
        reader.byte()
        header = data[:reader.pos]
        records = reader.records()
        assert reader.pos == len(data), (reader.pos, len(data))
        result = cls(header, records)
        assert result.encode() == data
        return result

    def encode(self):
        return self.header + b''.join(x.encode() for x in self.records) + b'\0'

    def walk(self):
        for r in self.records:
            yield from r.walk()

    def signature(self):
        """All mathematical character/template/embellishment records, in order."""
        return [(r.kind, r.prefix) for r in self.walk() if r.kind in [2, 3, 6]]

    def layout(self):
        return [{'kind': r.kind, **r.attrs} for r in self.walk() if r.kind in [4, 5]]


def line(children):
    return Record(1, b'\x01\x00', children, {'opts': 0})


def pile(lines, halign=4, valign=1):
    return Record(4, bytes([4, 0, halign, valign]), lines,
                  {'opts': 0, 'halign': halign, 'valign': valign})

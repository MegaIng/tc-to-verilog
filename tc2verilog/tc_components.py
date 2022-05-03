from functools import cached_property
from math import ceil
from pathlib import Path
from typing import ClassVar as _ClassVar

from tc2verilog.base_tc_component import TCComponent as _TCComponent, Out as _Out, OutTri as _OutTri, In as _In, \
    InSquare as _InSquare, Unbuffered as _Unbuffered, Size as _Size, NeedsClock as _NeedsClock, \
    IOComponent as _IOComponent, generate_sizes as _generate_sizes, size_hole as _size


# region BitComponents
from tc2verilog.memory_files import MemoryFile, ComponentMemoryFile, FileRomMemoryFile, translate_path


class Not(_TCComponent):
    pins = [
        _In("in", (-1, 0), 1),

        _Out("out", (1, 0), 1),
    ]


class Nand(_TCComponent):
    pins = [
        _In("in0", (-1, 1), 1),
        _In("in1", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


class And(_TCComponent):
    pins = [
        _In("in0", (-1, 1), 1),
        _In("in1", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


class And3(_TCComponent):
    pins = [
        _In("in0", (-1, 1), 1),
        _In("in1", (-1, 0), 1),
        _In("in2", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


class Or(_TCComponent):
    pins = [
        _In("in0", (-1, 1), 1),
        _In("in1", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


class Xor(_TCComponent):
    pins = [
        _In("in0", (-1, 1), 1),
        _In("in1", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


class Xnor(_TCComponent):
    pins = [
        _In("in0", (-1, 1), 1),
        _In("in1", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


class Or3(_TCComponent):
    pins = [
        _In("in0", (-1, 1), 1),
        _In("in1", (-1, 0), 1),
        _In("in2", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


class Nor(_TCComponent):
    pins = [
        _In("in0", (-1, 1), 1),
        _In("in1", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


class Decoder1(_TCComponent):
    pins = [
        _In("sel", (-1, 0), 1),
        _Out("out0", (1, 0), 1),
        _Out("out1", (1, 1), 1),
    ]


class Decoder2(_TCComponent):
    pins = [
        _In("sel0", (-1, -1), 1),
        _In("sel1", (-1, 0), 1),

        _Out("out0", (1, -1), 1),
        _Out("out1", (1, 0), 1),
        _Out("out2", (1, 1), 1),
        _Out("out3", (1, 2), 1),
    ]


class Decoder3(_TCComponent):
    pins = [
        _In("dis", (0, -4), 1),
        _In("sel0", (-1, -3), 1),
        _In("sel1", (-1, -2), 1),
        _In("sel2", (-1, -1), 1),

        _Out("out0", (1, -3), 1),
        _Out("out1", (1, -2), 1),
        _Out("out2", (1, -1), 1),
        _Out("out3", (1, 0), 1),
        _Out("out4", (1, 1), 1),
        _Out("out5", (1, 2), 1),
        _Out("out6", (1, 3), 1),
        _Out("out7", (1, 4), 1),
    ]


class FullAdder(_TCComponent):
    pins = [
        _In("in0", (-1, 0), 1),
        _In("in1", (-1, 1), 1),
        _In("ci", (-1, -1), 1),

        _Out("out", (1, 0), 1),
        _Out("co", (1, 1), 1),
    ]


# endregion

# region MultiBit Gates

@_generate_sizes()
class _And(_TCComponent):
    pins = [
        _In("in0", (-1, -1), _size),
        _In("in1", (-1, 0), _size),

        _Out("out", (1, 0), _size),
    ]


@_generate_sizes()
class _Add(_TCComponent):
    pins = [
        _In("in0", (-1, 1), _size),
        _In("in1", (-1, 0), _size),
        _In("ci", (-1, -1), 1),

        _Out("out", (1, -1), _size),
        _Out("co", (1, 0), 1),
    ]


@_generate_sizes(1, 8, 16, 32, 64)
class _Buffer(_TCComponent):
    pins = [
        _In("in", (-1, 0), _size),

        _Out("out", (1, 0), _size),
    ]


@_generate_sizes()
class _Equal(_TCComponent):
    pins = [
        _In("in0", (-1, -1), _size),
        _In("in1", (-1, 0), _size),

        _Out("out", (1, 0), 1),
    ]


@_generate_sizes()
class _LessI(_TCComponent):
    pins = [
        _In("in0", (-1, -1), _size),
        _In("in1", (-1, 0), _size),

        _Out("out", (1, 0), 1),
    ]


@_generate_sizes()
class _LessU(_TCComponent):
    pins = [
        _In("in0", (-1, -1), _size),
        _In("in1", (-1, 0), _size),

        _Out("out", (1, 0), 1),
    ]


@_generate_sizes()
class _Mul(_TCComponent):
    pins = [
        _In("in0", (-1, -1), _size),
        _In("in1", (-1, 0), _size),

        _Out("out0", (1, -1), _size),
        _Out("out1", (1, 0), _size),
    ]


@_generate_sizes()
class _Mux(_TCComponent):
    pins = [
        _In("sel", (-1, -1), 1),
        _In("in0", (-1, 0), _size),
        _In("in1", (-1, 1), _size),

        _Out("out", (1, 0), _size),
    ]


@_generate_sizes()
class _Nand(_TCComponent):
    pins = [
        _In("in0", (-1, -1), _size),
        _In("in1", (-1, 0), _size),

        _Out("out", (1, 0), _size),
    ]


@_generate_sizes()
class _Not(_TCComponent):
    pins = [
        _In("in", (-1, 0), _size),

        _Out("out", (1, 0), _size),
    ]


@_generate_sizes()
class _Neg(_TCComponent):
    pins = [
        _In("in", (-1, 0), _size),

        _Out("out", (1, 0), _size),
    ]


@_generate_sizes()
class _Nor(_TCComponent):
    pins = [
        _In("in0", (-1, -1), _size),
        _In("in1", (-1, 0), _size),

        _Out("out", (1, 0), _size),
    ]


@_generate_sizes()
class _Or(_TCComponent):
    pins = [
        _In("in0", (-1, -1), _size),
        _In("in1", (-1, 0), _size),

        _Out("out", (1, 0), _size),
    ]


@_generate_sizes()
class _Shl(_TCComponent):
    pins = [
        _In("in", (-1, -1), _size),
        _In("shift", (-1, 0), 8),

        _Out("out", (1, 0), _size),
    ]


@_generate_sizes()
class _Shr(_TCComponent):
    pins = [
        _In("in", (-1, -1), _size),
        _In("shift", (-1, 0), 8),

        _Out("out", (1, 0), _size),
    ]


@_generate_sizes(1, 8, 16, 32, 64)
class _Switch(_TCComponent):
    pins = [
        _In("en", (0, -1), 1),
        _In("in", (-1, 0), _size),

        _OutTri("out", (1, 0), _size),
    ]


@_generate_sizes()
class _Xnor(_TCComponent):
    pins = [
        _In("in0", (-1, -1), _size),
        _In("in1", (-1, 0), _size),

        _Out("out", (1, 0), _size),
    ]


@_generate_sizes()
class _Xor(_TCComponent):
    pins = [
        _In("in0", (-1, -1), _size),
        _In("in1", (-1, 0), _size),

        _Out("out", (1, 0), _size),
    ]


# endregion

# region Constants

class Off(_TCComponent):
    pins = [
        _Out("out", (1, 0), 1),
    ]

    @property
    def value(self):
        return 0

    verilog_name = "Constant"

    @property
    def parameters(self):
        return {"BIT_WIDTH": 1, "value": f"1'b{self.value}"}


class On(_TCComponent):
    pins = [
        _Out("out", (1, 0), 1),
    ]

    @property
    def value(self):
        return 1

    verilog_name = "Constant"

    @property
    def parameters(self):
        return {"BIT_WIDTH": 1, "value": f"1'b{self.value}"}


@_generate_sizes()
class _Constant(_TCComponent):
    pins = [
        _Out("out", (_size(1, 2, 2, 3), 0), _size),
    ]

    @property
    def value(self):
        return int(self.custom_string) & (2 ** 64 - 1) if self.custom_string else 0

    @property
    def parameters(self):
        return {"BIT_WIDTH": self.size, "value": f"{self.size}'d{self.value}"}


# endregion

# region Splitters & Makers


class Splitter8(_TCComponent):
    pins = [
        _In("in", (-1, 0), 8),
        _Out("out0", (1, -3), 1),
        _Out("out1", (1, -2), 1),
        _Out("out2", (1, -1), 1),
        _Out("out3", (1, 0), 1),
        _Out("out4", (1, 1), 1),
        _Out("out5", (1, 2), 1),
        _Out("out6", (1, 3), 1),
        _Out("out7", (1, 4), 1),
    ]


class Maker8(_TCComponent):
    pins = [
        _In("in0", (-1, -3), 1),
        _In("in1", (-1, -2), 1),
        _In("in2", (-1, -1), 1),
        _In("in3", (-1, 0), 1),
        _In("in4", (-1, 1), 1),
        _In("in5", (-1, 2), 1),
        _In("in6", (-1, 3), 1),
        _In("in7", (-1, 4), 1),
        _Out("out", (1, 0), 8),
    ]


class Splitter16(_TCComponent):
    pins = [
        _In("in", (-1, 0), 16),
        _Out("out0", (1, -1), 8),
        _Out("out1", (1, 0), 8),
    ]


class Maker16(_TCComponent):
    pins = [
        _In("in0", (-1, -1), 8),
        _In("in1", (-1, 0), 8),
        _Out("out", (1, 0), 16),
    ]


class Splitter32(_TCComponent):
    pins = [
        _In("in", (-1, 0), 32),
        _Out("out0", (1, -1), 8),
        _Out("out1", (1, 0), 8),
        _Out("out2", (1, 1), 8),
        _Out("out3", (1, 2), 8),
    ]


class Maker32(_TCComponent):
    pins = [
        _In("in0", (-1, -1), 8),
        _In("in1", (-1, 0), 8),
        _In("in2", (-1, 1), 8),
        _In("in3", (-1, 2), 8),
        _Out("out", (1, 0), 32),
    ]


class Splitter64(_TCComponent):
    pins = [
        _In("in", (-1, 0), 64),
        _Out("out0", (1, -3), 8),
        _Out("out1", (1, -2), 8),
        _Out("out2", (1, -1), 8),
        _Out("out3", (1, 0), 8),
        _Out("out4", (1, 1), 8),
        _Out("out5", (1, 2), 8),
        _Out("out6", (1, 3), 8),
        _Out("out7", (1, 4), 8),
    ]


class Maker64(_TCComponent):
    pins = [
        _In("in0", (-1, -3), 8),
        _In("in1", (-1, -2), 8),
        _In("in2", (-1, -1), 8),
        _In("in3", (-1, 0), 8),
        _In("in4", (-1, 1), 8),
        _In("in5", (-1, 2), 8),
        _In("in6", (-1, 3), 8),
        _In("in7", (-1, 4), 8),
        _Out("out", (1, 0), 64),
    ]


# endregion

# region Memory

class SRLatch(_TCComponent):
    pins = [
        _In("s", (-1, -1), 1),
        _In("r", (-1, 1), 1),
        _Out("q", (1, -1), 1),
        _Out("qn", (1, 1), 1),
    ]


class BitMemory(_NeedsClock):
    pins = [
        _InSquare("save", (-1, -1), 1),
        _InSquare("in", (-1, 1), 1),
        _Out("out", (1, 0), 1),
    ]


@_generate_sizes()
class _Counter(_NeedsClock):
    pins = [
        _InSquare("save", (_size(-1, -2, -2, -3), -1), 1),
        _InSquare("in", (_size(-1, - 2, -2, - 3), 0), _size),
        _Out("out", (_size(1, 2, 2, 3), 0), _size),
    ]

    @property
    def value(self):
        return int(self.custom_string)

    @property
    def parameters(self):
        return {"count": f"{self.size}'d{self.value}"}


@_generate_sizes()
class _Register(_NeedsClock):
    pins = [
        _In("load", (_size(-1, - 2, -2, - 3), -1), 1),
        _InSquare("save", (_size(-1, -2, -2, -3), 0), 1),
        _InSquare("in", (_size(-1, - 2, -2, - 3), 1), _size),
        _Out("out", (_size(1, 2, 2, 3), 0), _size),
    ]


@_generate_sizes(1, 8, 16, 32, 64)
class _DelayLine(_NeedsClock):
    pins = [
        _InSquare("in", (_size(-1, -1, - 2, -2, - 3), 0), _size),
        _Out("out", (_size(1, 1, 2, 2, 3), 0), _size),
    ]


class Ram(_NeedsClock):
    pins = [
        _In("load", (-13, -7), 1),
        _InSquare("save", (-13, -6), 1),
        _In("address", (-13, -5), 8),
        _InSquare("in", (-13, -4), 8),
        _Out("out", (13, -7), 8),
    ]


class Stack(_NeedsClock):
    pins = [
        _In("pop", (-13, -7), 1),
        _InSquare("push", (-13, -6), 1),
        _InSquare("in", (-13, -5), 8),
        _Out("out", (13, -7), 8),
    ]


class FastRam(_NeedsClock):
    pins = [
        _In("load", (-13, -7), 1),
        _InSquare("save", (-13, -6), 1),
        _In("address", (-13, -5), 16),
        _InSquare("in0", (-13, -4), 64),
        _InSquare("in1", (-13, -3), 64),
        _InSquare("in2", (-13, -2), 64),
        _InSquare("in3", (-13, -1), 64),
        _OutTri("out0", (13, -7), 64),
        _OutTri("out1", (13, -6), 64),
        _OutTri("out2", (13, -5), 64),
        _OutTri("out3", (13, -4), 64),
    ]

    @property
    def word_size(self) -> _Size:
        return 8 * (2 ** int(self.custom_string.split(':')[1]))

    @property
    def byte_count(self) -> int:
        return int(self.custom_string.split(':')[0])

    @property
    def word_count(self):
        return (self.byte_count + self.word_size - 1) // self.word_size  # ceil division

    @property
    def parameters(self):
        return {
            'BIT_WIDTH': self.word_size,
            'MEM_WORDS': self.word_count,

        }


class CheapRam(FastRam):
    verilog_name = "FastRam"


class CheapRamLat(_NeedsClock):
    pins = [
        _InSquare("load", (-13, -7), 1),
        _InSquare("save", (-13, -6), 1),
        _InSquare("address", (-13, -5), 16),
        _InSquare("in0", (-13, -4), 64),
        _InSquare("in1", (-13, -3), 64),
        _InSquare("in2", (-13, -2), 64),
        _InSquare("in3", (-13, -1), 64),
        _OutTri("ready", (13, -7), 1),
        _OutTri("out0", (13, -6), 64),
        _OutTri("out1", (13, -5), 64),
        _OutTri("out2", (13, -4), 64),
        _OutTri("out3", (13, -3), 64),
    ]


class Rom(_NeedsClock):
    pins = [
        _In("load", (-13, -7), 1),
        _InSquare("save", (-13, -6), 1),
        _In("address", (-13, -5), 16),
        _InSquare("in", (-13, -4), 64),
        _OutTri("out", (13, -7), 64),
    ]

    @property
    def word_size(self) -> _Size:
        return 8 * (2 ** int(self.custom_string.split(':')[1]))

    @property
    def byte_count(self) -> int:
        return int(self.custom_string.split(':')[0])

    @property
    def word_count(self):
        return (self.byte_count + self.word_size - 1) // self.word_size  # ceil division

    @property
    def parameters(self):
        return {
            'BIT_WIDTH': self.word_size,
            'MEM_WORDS': self.word_count,
            'ARG_SIG': f'"HEX_FILE_{self.name_id}=%s"',
            'HEX_FILE': self.default_file_name,

        }

    @property
    def default_file_name(self):
        return f'{self.name_id}.s{self.byte_count}.m{self.word_size}'

    @property
    def memory_files(self):
        yield ComponentMemoryFile(self.default_file_name, self.word_size, self.word_count, f"{self.permanent_id}.rom")


class Hdd(_NeedsClock):
    pins = [
        _In("seek", (-13, -7), 8),
        _In("load", (-13, -6), 1),
        _InSquare("save", (-13, -5), 1),
        _InSquare("in", (-13, -4), 64),
        _OutTri("out", (13, -7), 64),
    ]

    @property
    def word_count(self):
        return int(self.custom_string) if self.custom_string else 256

    @property
    def parameters(self):
        return {
            'MEM_WORDS': self.word_count,
            'ARG_SIG': f'"HEX_FILE_{self.name_id}=%s"',
            'HEX_FILE': f'"{self.default_file_name}"',
        }

    @property
    def default_file_name(self):
        return f'{self.name_id}.s{self.word_count}.m64'

    @property
    def memory_files(self):
        yield ComponentMemoryFile(self.default_file_name, 64, self.word_count, f"{self.permanent_id}.hdd")


class DualLoadRam(_NeedsClock):
    pins = [
        _In("load0", (-13, -7), 1),
        _InSquare("save", (-13, -6), 1),
        _In("address0", (-13, -5), 16),
        _InSquare("in", (-13, -4), 64),
        _In("load1", (-13, -3), 1),
        _In("address1", (-13, -2), 16),
        _OutTri("out0", (13, -7), 64),
        _OutTri("out1", (13, -6), 64),
    ]

    @property
    def word_size(self) -> _Size:
        return 8 * (2 ** int(self.custom_string.split(':')[1]))

    @property
    def byte_count(self) -> int:
        return int(self.custom_string.split(':')[0])

    @property
    def word_count(self):
        return (self.byte_count + self.word_size - 1) // self.word_size  # ceil division

    @property
    def parameters(self):
        return {
            'BIT_WIDTH': self.word_size,
            'MEM_WORDS': self.word_count,

        }


# endregion

# region IO Components


class Clock(_TCComponent):
    pins = [
        _In("en", (0, -1), 1),
        _OutTri("out", (1, 0), 64),
    ]


# noinspection PyPep8Naming
class Program8_1(_NeedsClock):
    pins = [
        _In("address", (-13, -7), 8),
        _Out("out", (13, -7), 8),
    ]

    @property
    def parameters(self):
        return {
            "MEM_BYTES": 256,
            "ARG_SIG": f'"HEX_FILE_{self.name_id}=%s"',
            "HEX_FILE": f'"{self.default_file_name}"',
        }

    @property
    def default_file_name(self):
        return f'{self.name_id}.s256.m8'

    @property
    def memory_files(self):
        yield MemoryFile(self.default_file_name, 8, 256)


# noinspection PyPep8Naming
class Program8_4(_NeedsClock):
    pins = [
        _In("address", (-13, -7), 8),
        _Out("out0", (13, -7), 8),
        _Out("out1", (13, -6), 8),
        _Out("out2", (13, -5), 8),
        _Out("out3", (13, -4), 8),
    ]

    @property
    def parameters(self):
        return {
            "MEM_BYTES": 256,
            "ARG_SIG": f'"HEX_FILE_{self.name_id}=%s"',
            "HEX_FILE": f'"{self.default_file_name}"',
        }

    @property
    def default_file_name(self):
        return f'{self.name_id}.s256.m8'

    @property
    def memory_files(self):
        yield MemoryFile(self.default_file_name, 8, 256)


class ProgramWord(_NeedsClock):
    pins = [
        _In("address", (-13, -7), 16),
        _Out("out0", (13, -7), 8),
        _Out("out1", (13, -6), 8),
        _Out("out2", (13, -5), 8),
        _Out("out3", (13, -4), 8),
    ]

    @property
    def word_size(self) -> _Size:
        return 8 * (2 ** int(self.custom_string))

    @property
    def parameters(self):
        return {
            "BIT_WIDTH": self.word_size,
            "MEM_WORDS": 0,
            "ARG_SIG": f'"HEX_FILE_{self.name_id}=%s"',
            "HEX_FILE": f'"{self.default_file_name}"',
        }

    @property
    def default_file_name(self):
        return f'{self.name_id}.s65536.m{self.word_size}'

    @property
    def memory_files(self):
        yield MemoryFile(self.default_file_name, self.word_size, 0)


class FileRom(_NeedsClock):
    pins = [
        _In("en", (-3, -1), 1),
        _In("address", (-4, 0), 64),
        _OutTri("out", (4, 0), 64),
    ]

    @cached_property
    def configured_path(self) -> Path | None:
        p = translate_path(self.custom_string)
        if p.exists():
            return p
        else:
            return None

    @property
    def file_size(self) -> int:
        p = self.configured_path
        if p is None:
            return 0
        else:
            return p.stat().st_size

    @property
    def parameters(self):
        return {
            "MEM_BYTES": 256,
            "ARG_SIG": f'"HEX_FILE_{self.name_id}=%s"',
            "HEX_FILE": f'"{self.default_file_name}"',
            "FILE_BYTES": self.file_size,
        }

    @property
    def default_file_name(self):
        return f'{self.name_id}.file_rom.m8'

    @property
    def memory_files(self):
        p = self.configured_path
        if p is None:
            yield MemoryFile(self.default_file_name, 8, 0)
        else:
            yield FileRomMemoryFile(self.default_file_name, 8, self.file_size, p)


class Halt(_TCComponent):
    pins = [_In("en", (-1, 0), 1)]


# endregion

# region Input Gates


class _SimpleInput(_IOComponent):
    pass


class Input1(_SimpleInput):
    size = 1
    pins = [_Out("value", (1, 0), 1)]


class Input2Pin(_SimpleInput):
    size = 1
    pins = [
        _Out("value0", (1, -1), 1),
        _Out("value1", (1, 1), 1),
    ]


class Input3Pin(_SimpleInput):
    size = 1
    pins = [
        _Out("value0", (1, -2), 1),
        _Out("value1", (1, -1), 1),
        _Out("value2", (1, 0), 1),
    ]


class Input4Pin(_SimpleInput):
    size = 1
    pins = [
        _Out("value0", (1, -2), 1),
        _Out("value1", (1, -1), 1),
        _Out("value2", (1, 0), 1),
        _Out("value3", (1, 1), 1),
    ]


class Input8(_SimpleInput):
    size = 8
    pins = [_Out("value", (1, 0), 8)]


class Input16(_SimpleInput):
    size = 16
    pins = [_Out("value", (2, 0), 16)]


class Input32(_SimpleInput):
    size = 32
    pins = [_Out("value", (2, 0), 32)]


class Input64(_SimpleInput):
    size = 64
    pins = [_Out("value", (3, 0), 64)]


# noinspection PyPep8Naming
class Input1_1B(_IOComponent):
    pins = [
        _In("control", (0, 1), 1),
        _OutTri("value", (1, 0), 8),
    ]


# endregion

# region Output Gates


class _SimpleOutput(_IOComponent):
    pass


class Output1(_SimpleOutput):
    size = 1
    pins = [_In("value", (-1, 0), 1)]


class Output2Pin(_SimpleOutput):
    size = 1
    pins = [
        _In("value0", (-1, -1), 1),
        _In("value1", (-1, 0), 1)
    ]


class Output3Pin(_SimpleOutput):
    size = 1
    pins = [
        _In("value0", (-1, -1), 1),
        _In("value1", (-1, 0), 1),
        _In("value2", (-1, 1), 1)
    ]


class Output4Pin(_SimpleOutput):
    size = 1
    pins = [
        _In("value0", (-1, -2), 1),
        _In("value1", (-1, -1), 1),
        _In("value2", (-1, 0), 1),
        _In("value3", (-1, 1), 1),
    ]


class Output1Sum(Output1):
    pass


class Output1Car(Output1):
    pass


class Output8(_SimpleOutput):
    size = 8
    pins = [_In("value", (-1, 0), 8)]


class Output16(_SimpleOutput):
    size = 16
    pins = [_In("value", (-2, 0), 16)]


class Output32(_SimpleOutput):
    size = 32
    pins = [_In("value", (-2, 0), 32)]


class Output64(_SimpleOutput):
    size = 64
    pins = [_In("value", (-3, 0), 64)]


# noinspection PyPep8Naming
class Output1_1B(_IOComponent):
    pins = [
        _In("control", (0, 1), 1),
        _In("value", (-1, 0), 8),
    ]

# endregion

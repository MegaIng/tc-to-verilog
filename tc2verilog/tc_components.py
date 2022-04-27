from typing import ClassVar as _ClassVar

from tc2verilog.base_tc_component import TCComponent as _TCComponent, Out as _Out, OutTri as _OutTri, In as _In, \
    InSquare as _InSquare, Unbuffered as _Unbuffered, Size as _Size, NeedsClock as _NeedsClock, \
    IOComponent as _IOComponent, generate_sizes as _generate_sizes, size_hole as _size


class On(_TCComponent):
    pins = [
        _Out("value", (1, 0), 1),
    ]


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


class Or(_TCComponent):
    pins = [
        _In("in0", (-1, 1), 1),
        _In("in1", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


class Nor(_TCComponent):
    pins = [
        _In("in0", (-1, 1), 1),
        _In("in1", (-1, -1), 1),

        _Out("out", (2, 0), 1),
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


@_generate_sizes(1, 8, 16, 32, 64)
class _Buffer(_TCComponent):
    pins = [
        _In("in", (-1, 0), _size),

        _Out("out", (1, 0), _size),
    ]


@_generate_sizes()
class _Constant(_TCComponent):
    pins = [
        _Out("out", (1, 0), _size),
    ]

    @property
    def value(self):
        return int(self.custom_string)

    @property
    def parameters(self):
        return f".value('d{self.value})"


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


# region Input Gates


class _SimpleInput(_IOComponent):
    verilog_type = "input wire"


class Input1(_SimpleInput):
    size = 1
    pins = [_Out("value", (1, 0), 1)]


# endregion

# region Output Gates


class _SimpleOutput(_IOComponent):
    verilog_type = "output wire"


class Output1(_SimpleOutput):
    size = 1
    pins = [_In("value wire", (-1, 0), 1)]


class Output1Sum(Output1):
    pass


class Output1Car(Output1):
    pass


class Output8(_SimpleOutput):
    size = 8
    pins = [_In("value wire", (-1, 0), 8)]

# endregion

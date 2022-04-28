from typing import ClassVar as _ClassVar

from tc2verilog.base_tc_component import TCComponent as _TCComponent, Out as _Out, OutTri as _OutTri, In as _In, \
    InSquare as _InSquare, Unbuffered as _Unbuffered, Size as _Size, NeedsClock as _NeedsClock, \
    IOComponent as _IOComponent, generate_sizes as _generate_sizes, size_hole as _size


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
        return f".size('d1), .value(1'b{self.value})"


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
        return f".size('d1), .value(1'b{self.value})"


class Constant8(_TCComponent):
    pins = [
        _Out("out", (1, 0), 8),
    ]

    @property
    def value(self):
        return int(self.custom_string) & (2**64-1)

    verilog_name = "Constant"

    @property
    def parameters(self):
        return f".size('d8), .value(8'd{self.value})"


class Constant16(_TCComponent):
    pins = [
        _Out("out", (2, 0), 16),
    ]

    @property
    def value(self):
        return int(self.custom_string) & (2**64-1)

    verilog_name = "Constant"

    @property
    def parameters(self):
        return f".size('d16), .value(16'd{self.value})"


class Constant32(_TCComponent):
    pins = [
        _Out("out", (2, 0), 32),
    ]

    @property
    def value(self):
        return int(self.custom_string) & (2**64-1)

    verilog_name = "Constant"

    @property
    def parameters(self):
        return f".size('d32), .value(32'd{self.value})"


class Constant64(_TCComponent):
    pins = [
        _Out("out", (3, 0), 64),
    ]

    @property
    def value(self):
        return int(self.custom_string) & (2**64-1)

    verilog_name = "Constant"

    @property
    def parameters(self):
        return f".size('d64), .value(64'd{self.value})"

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


# end region

# region Input Gates


class _SimpleInput(_IOComponent):
    verilog_type = "input wire"


class Input1(_SimpleInput):
    size = 1
    pins = [_Out("value", (1, 0), 1)]


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


class Output16(_SimpleOutput):
    size = 16
    pins = [_In("value wire", (-2, 0), 16)]


class Output32(_SimpleOutput):
    size = 32
    pins = [_In("value wire", (-2, 0), 32)]


class Output64(_SimpleOutput):
    size = 64
    pins = [_In("value wire", (-3, 0), 64)]

# endregion

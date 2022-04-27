from typing import ClassVar as _ClassVar

from tc2verilog.tc_schematics import TCComponent as _TCComponent, Out as _Out, OutTri as _OutTri, In as _In, \
    InSquare as _InSquare, Unbuffered as _Unbuffered, Size as _Size, NeedsClock as _NeedsClock, \
    IOComponent as _IOComponent


# region Bit Gates

class Off(_TCComponent):
    pins = [
        _Out("value", (1, 0), 1),
    ]


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
        _In("a", (-1, 1), 1),
        _In("b", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


class And(_TCComponent):
    pins = [
        _In("a", (-1, 1), 1),
        _In("b", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


class Or(_TCComponent):
    pins = [
        _In("a", (-1, 1), 1),
        _In("b", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


class Nor(_TCComponent):
    pins = [
        _In("a", (-1, 1), 1),
        _In("b", (-1, -1), 1),

        _Out("out", (2, 0), 1),
    ]


# endregion

# region Byte Gates

class Register8(_NeedsClock):
    pins = [
        _In("load", (-1, -1), 1),
        _InSquare("save", (-1, 0), 1),
        _InSquare("save_value", (-1, 1), 8),
        _OutTri("load_value", (1, 0), 8),
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


# endregion

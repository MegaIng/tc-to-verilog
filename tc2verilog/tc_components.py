from tc2verilog.tc_schematics import TCComponent as _TCComponent, Out as _Out, OutTri as _OutTri, In as _In, \
    InSquare as _InSquare, Unbuffered as _Unbuffered


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

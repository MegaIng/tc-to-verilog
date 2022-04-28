import sys
from dataclasses import dataclass
from typing import ClassVar, TypeAlias, Literal

Size: TypeAlias = Literal[1, 8, 16, 32, 64]


@dataclass
class TCPin:
    name: str
    rel_pos: tuple[int, int]
    size: Size


@dataclass
class In(TCPin):
    pass


@dataclass
class InSquare(In):
    pass


@dataclass
class Out(TCPin):
    pass


@dataclass
class OutTri(Out):
    pass


@dataclass
class Unbuffered(Out, In):
    pass


@dataclass
class TCComponent:
    raw_nim_data: dict

    pins: ClassVar[list[TCPin]]

    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def x(self) -> int:
        return self.raw_nim_data["position"]["x"]

    @property
    def y(self) -> int:
        return self.raw_nim_data["position"]["y"]

    @property
    def rotation(self) -> int:
        return self.raw_nim_data["rotation"]

    @property
    def permanent_id(self) -> int:
        return self.raw_nim_data["permanent_id"]

    @property
    def custom_string(self) -> str:
        return self.raw_nim_data["custom_string"]

    @property
    def verilog_name(self):
        return f"TC_{type(self).__name__}"

    parameters = None

    @property
    def positioned_pins(self) -> list[tuple[tuple[int, int], TCPin]]:
        (fxx, fxy), (fyx, fyy) = {
            0: ((1, 0), (0, 1)),
            1: ((0, -1), (1, 0)),
            2: ((-1, 0), (0, -1)),
            3: ((0, 1), (-1, 0)),
        }[self.rotation]
        return [((self.x + p.rel_pos[0] * fxx + p.rel_pos[1] * fxy,
                  self.y + p.rel_pos[0] * fyx + p.rel_pos[1] * fyy
                  ), p) for p in self.pins]


class NeedsClock(TCComponent):
    needs_clock: bool = True


class IOComponent(TCComponent):
    size: ClassVar[Size]
    verilog_type: ClassVar[str]

    @property
    def verilog_size_type(self):
        return f"{self.verilog_type} [{self.size - 1}:0]"


class _SizeHole:
    pass


size_hole = _SizeHole()


def _generate_sized_class(base, size: int):
    size_param = f".size('d{size})"

    class SizedSubclass(base):
        pins = [
            type(p)(p.name, p.rel_pos, p.size if p.size is not size_hole else size)
            for p in base.pins
        ]

        @property
        def verilog_name(self):
            return "TC_" + base.__name__.removeprefix('_')

        @property
        def parameters(self):
            sp = super(SizedSubclass, self).parameters
            if sp is None:
                return size_param
            else:
                return f"{sp}, {size_param}"

    SizedSubclass.__name__ = f"{base.__name__.removeprefix('_')}{size}"
    SizedSubclass.__qualname__ = base.__qualname__.replace(base.__name__, SizedSubclass.__name__)

    return SizedSubclass


def generate_sizes(*sizes: int):
    if not sizes:
        sizes = (8, 16, 32, 64)

    def wrapper(cls):
        m = sys.modules[cls.__module__]
        for size in sizes:
            new_cls = _generate_sized_class(cls, size)
            setattr(m, new_cls.__name__, new_cls)
        return cls

    return wrapper

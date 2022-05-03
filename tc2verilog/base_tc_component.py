import sys
from dataclasses import dataclass
from typing import ClassVar, TypeAlias, Literal, TYPE_CHECKING, TypeVar, Callable

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
    name: str = None

    memory_files = ()

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
        return type(self).__name__

    @property
    def name_id(self):
        return self.name if self.name is not None else hex(self.permanent_id)[2:]

    @property
    def parameters(self):
        return {}

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

    @property
    def above_topleft(self):
        (fxx, fxy), (fyx, fyy) = {
            0: ((1, 0), (0, 1)),
            1: ((0, -1), (1, 0)),
            2: ((-1, 0), (0, -1)),
            3: ((0, 1), (-1, 0)),
        }[self.rotation]
        rel_pos = min(p.rel_pos for p in self.pins)
        rel_pos = rel_pos[0], rel_pos[1] - 1
        return (self.x + rel_pos[0] * fxx + rel_pos[1] * fxy,
                self.y + rel_pos[0] * fyx + rel_pos[1] * fyy)


class NeedsClock(TCComponent):
    needs_clock: bool = True


class IOComponent(TCComponent):
    size: ClassVar[Size]


if TYPE_CHECKING:
    T = TypeVar('T')

    size_hole: Size | Callable[[int, ...], int]
else:
    # noinspection PyPep8Naming
    class size_hole:
        def __init__(self, *values):
            self.values = values


def _fill_holes(size, i, obj):
    if isinstance(obj, size_hole):
        return obj.values[i]
    elif obj is size_hole:
        return size
    elif isinstance(obj, (tuple, list)):
        return type(obj)(_fill_holes(size, i, e) for e in obj)
    else:
        assert isinstance(obj, (int, str))
        return obj


def _generate_sized_class(base, i, size: int):
    size_param = {'BIT_WIDTH': size}

    class SizedSubclass(base):
        pins = [
            type(p)(p.name, _fill_holes(size, i, p.rel_pos), _fill_holes(size, i, p.size))
            for p in base.pins
        ]

        verilog_name = base.__name__.removeprefix('_')

        @property
        def parameters(self):
            sp = super(SizedSubclass, self).parameters
            if sp is None:
                return size_param
            else:
                return sp | size_param

    SizedSubclass.__name__ = f"{base.__name__.removeprefix('_')}{size}"
    SizedSubclass.__qualname__ = base.__qualname__.replace(base.__name__, SizedSubclass.__name__)
    SizedSubclass.size = size

    return SizedSubclass


def generate_sizes(*sizes: int):
    if not sizes:
        sizes = (8, 16, 32, 64)

    def wrapper(cls):
        m = sys.modules[cls.__module__]
        for i, size in enumerate(sizes):
            new_cls = _generate_sized_class(cls, i, size)
            setattr(m, new_cls.__name__, new_cls)
        return cls

    return wrapper

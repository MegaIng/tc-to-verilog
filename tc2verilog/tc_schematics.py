import os
import sys
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from pprint import pprint

try:
    import nimporter
except ImportError:
    print("Couldn't import nimporter, assuming save_monger is available anyway.")

import tc2verilog.save_monger as save_monger
from dataclasses import dataclass
from typing import Literal, TypeAlias, ClassVar, cast

Size: TypeAlias = Literal[1, 8, 16, 32, 64]


@dataclass
class TCPin:
    name: str
    pos: tuple[int, int]
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
class OutTri(TCPin):
    pass


@dataclass
class Unbuffered(TCPin):
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


@dataclass
class TCWire:
    raw_nim_data: dict

    @property
    def color(self) -> int:
        return self.raw_nim_data["color"]

    @property
    def comment(self) -> str:
        return self.raw_nim_data["comment"]

    @property
    def kind(self) -> Size:
        k = int(self.raw_nim_data["kind"][3:])
        assert k in (1, 8, 16, 32, 64)
        return cast(Size, k)

    @cached_property
    def path(self) -> list[tuple[int, int]]:
        return [(p['x'], p['y']) for p in self.raw_nim_data["path"]]

    @property
    def start(self) -> tuple[int, int]:
        return self.path[0]

    @property
    def end(self) -> tuple[int, int]:
        return self.path[-1]


@dataclass
class TCSchematic:
    raw_nim_data: dict

    @cached_property
    def wires(self) -> list[TCWire]:
        return [TCWire(w) for w in self.raw_nim_data["wires"]]

    @cached_property
    def components(self) -> list[TCComponent]:
        return [TCComponent(w) for w in self.raw_nim_data["components"]]

    @classmethod
    def open_level(cls, level_name: str, save_name: str):
        return cls(save_monger.parse_state((SCHEMATICS / level_name / save_name / "circuit.data").read_bytes()))


def get_path():
    match sys.platform.lower():
        case "windows" | "win32":
            potential_paths = [Path(os.path.expandvars(r"%APPDATA%\Godot\app_userdata\Turing Complete"))]
        case "darwin":
            potential_paths = [Path("~/Library/Application Support/Godot/app_userdata/Turing Complete").expanduser()]
        case "linux":
            potential_paths = [
                Path("~/.local/share/godot/app_userdata/Turing Complete").expanduser(),
                # for wsl
                Path(os.path.expandvars("/mnt/c/Users/${USER}/AppData/Roaming/godot/app_userdata/Turing Complete/")),
            ]
        case _:
            print(f"Don't know where to find Turing Complete save on {sys.platform=}")
            return None
    for base_path in potential_paths:
        if base_path.exists():
            break
    else:
        print("You need Turing Complete installed to use everything here")
        return None
    return base_path


BASE_PATH = get_path()

SCHEMATICS = BASE_PATH / "schematics"

# state = save_monger.parse_state((SCHEMATICS / "not_gate" / "Default" / "circuit.data").read_bytes())
# pprint(state)

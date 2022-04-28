import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from pprint import pprint

from tc2verilog.base_tc_component import TCComponent, TCPin, IOComponent, Size

try:
    import nimporter
except ImportError:
    print("Couldn't import nimporter, assuming save_monger is available anyway.")

# noinspection PyUnresolvedReferences
import tc2verilog.save_monger as save_monger
from dataclasses import dataclass
from typing import Literal, TypeAlias, ClassVar, cast


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
        return [getattr(tc_components, c["kind"])(c) for c in self.raw_nim_data["components"]]

    @classmethod
    def open_level(cls, level_name: str, save_name: str):
        return cls(save_monger.parse_state((SCHEMATICS / level_name / save_name / "circuit.data").read_bytes()))

    @cached_property
    def wire_map(self) -> dict[tuple[int, int], set[tuple[int, int]]]:
        points = defaultdict(set)
        for wire in self.wires:
            s = {wire.start, wire.end, *points[wire.start], *points[wire.end]}
            for p in s:
                points[p] = s
        return points

    @cached_property
    def pin_map(self) -> dict[tuple[int, int], tuple[TCComponent, TCPin, int]]:
        pins = {}
        for com in self.components:
            for i, (pos, pin) in enumerate(com.positioned_pins):
                assert pos not in pins, pos
                pins[pos] = (com, pin, i)
        return pins

    @cached_property
    def named_io_by_name(self) -> dict[str, IOComponent]:
        out = {}
        for com in self.components:
            if isinstance(com, (tc_components._SimpleInput, tc_components._SimpleOutput)):
                if com.custom_string:
                    name = com.custom_string.partition(":")[-1]
                else:
                    name = f"{type(com).__name__}x{com.x % 512:03}y{com.y % 512:03}"
                out[name] = com
        return out

    @cached_property
    def named_pins_by_position(self) -> dict[tuple[int, int], tuple[str, TCComponent]]:
        out = {}
        for name, com in self.named_io_by_name.items():
            out[com.pos] = name, com
        return out


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

from tc2verilog import tc_components

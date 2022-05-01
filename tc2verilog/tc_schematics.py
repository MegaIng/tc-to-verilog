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


@dataclass(eq=False)
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


IGNORE_COMPONENTS = {
    "Screen"
}


@dataclass(eq=False)
class TCSchematic:
    raw_nim_data: dict
    io_mapping: dict[str, tuple[str, dict[str, str] | None]] | None = None

    @cached_property
    def wires(self) -> list[TCWire]:
        return [TCWire(w) for w in self.raw_nim_data["wires"]]

    @cached_property
    def components(self) -> list[TCComponent]:
        out = []
        used_labels = set()
        for c in self.raw_nim_data["components"]:
            if c["kind"] not in IGNORE_COMPONENTS:
                obj = getattr(tc_components, c["kind"])(c)
                if len(self.wires_by_position[obj.above_topleft]) == 1:
                    wire, = self.wires_by_position[obj.above_topleft]
                    if wire.comment:
                        assert wire.comment not in used_labels, wire.comment
                        obj.name = wire.comment
                        used_labels.add(wire.comment)
                out.append(obj)
        return out

    @classmethod
    def open_level(cls, level_name: str, save_name: str,
                   io_mapping: dict[str, tuple[str, dict[str, str] | None]] = None):
        return cls(save_monger.parse_state((SCHEMATICS / level_name / save_name / "circuit.data").read_bytes()),
                   io_mapping)

    @cached_property
    def wire_map(self) -> dict[tuple[int, int], set[tuple[int, int]]]:
        points = defaultdict(set)
        for wire in self.wires:
            s = {wire.start, wire.end, *points[wire.start], *points[wire.end]}
            for p in s:
                points[p] = s
        return points

    @cached_property
    def wires_by_position(self) -> dict[tuple[int, int], set[TCWire]]:
        positions = defaultdict(set)
        for wire in self.wires:
            positions[wire.start].add(wire)
            positions[wire.end].add(wire)
        out = defaultdict(set)
        for p, group in self.wire_map.items():
            out[p] = set.union(*(positions[i] for i in group))
        return out

    @cached_property
    def pin_map(self) -> dict[tuple[int, int], tuple[TCComponent, TCPin, int]]:
        pins = {}
        for com in self.components:
            for i, (pos, pin) in enumerate(com.positioned_pins):
                assert pos not in pins, (pos, com)
                pins[pos] = (com, pin, i)
        return pins

    @cached_property
    def named_io_com_by_name(self) -> dict[str, IOComponent]:
        out = {}
        for com in self.components:
            if isinstance(com, (IOComponent)):
                if com.custom_string:
                    name = com.custom_string.partition(":")[-1]
                else:
                    name = f"{type(com).__name__}x{com.x % 512:03}y{com.y % 512:03}"
                out[name] = com
        if self.io_mapping is not None:
            assert len(self.io_mapping) == len(out), (list(out), list(self.io_mapping))
            new_out = {}
            for (base_name, (exp_io, _)), com in zip(self.io_mapping.items(), out.values()):
                assert exp_io == type(com).__name__, (exp_io, type(com).__name__)
                new_out[base_name] = com
            out = new_out
        return out

    @cached_property
    def named_io_pin_by_name(self) -> dict[str, tuple[IOComponent, TCPin, tuple[int, int]]]:
        out = {}
        for base_name, com in self.named_io_com_by_name.items():
            for pos, pin in com.positioned_pins:
                if self.io_mapping is not None and self.io_mapping[base_name][1] is not None:
                    name = self.io_mapping[base_name][1][pin.name]
                else:
                    name = f"{base_name}_{pin.name}"
                out[name] = com, pin, pos
        return out

    @cached_property
    def named_io_com_by_position(self) -> dict[tuple[int, int], tuple[str, TCComponent]]:
        out = {}
        for name, com in self.named_io_com_by_name.items():
            out[com.pos] = name, com
        return out


ON_WSL = False


def get_path():
    global ON_WSL
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
            if "/mnt/c/Users" in str(base_path):
                ON_WSL = True
            break
    else:
        print("You need Turing Complete installed to use everything here")
        return None
    return base_path


BASE_PATH = get_path()

SCHEMATICS = BASE_PATH / "schematics"

from tc2verilog import tc_components

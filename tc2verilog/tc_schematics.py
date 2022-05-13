import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from pprint import pprint

from tc2verilog.base_tc_component import TCComponent, TCPin, IOComponent, Size, NeedsClock as _NeedsClock

# noinspection PyUnresolvedReferences
import save_monger
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


@dataclass(eq=False)
class WireBundle:
    wires: list[TCWire]

    @property
    def positions(self):
        return {p for w in self.wires for p in (w.start, w.end)}

    def get_safe_name(self, i: int):
        return normalize_name(self.get_name(i))

    def get_name(self, i: int):
        for wire in self.wires:
            if wire.comment != "":
                return f"{wire.comment} {i}"
        return f"wire {i}"


IGNORE_COMPONENTS = {
    "Screen",
    "ProbeMemoryBit",
    "ProbeMemoryWord",
    "ProbeWireBit",
    "ProbeWireWord",
}


def normalize_name(name):
    non_legal = r"[^a-zA-Z0-9_\$]"
    name = re.sub(non_legal, "_", name)
    return name


@dataclass(eq=False)
class TCSchematic:
    raw_nim_data: dict

    @property
    def save_version(self):
        return self.raw_nim_data["save_version"]

    @property
    def custom_component_id(self):
        return self.raw_nim_data["save_version"]

    @cached_property
    def wires(self) -> list[TCWire]:
        return [TCWire(w) for w in self.raw_nim_data["wires"]]

    @cached_property
    def components(self) -> list[TCComponent]:
        from tc2verilog import tc_components
        out = []
        used_labels = set()
        for c in self.raw_nim_data["components"]:
            if c["kind"] in IGNORE_COMPONENTS:
                continue
            if c["kind"] == "Custom":
                obj = custom_component_classes[c["custom_id"]](c)
            else:
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
    def open_level(cls, level_name: str, save_name: str):
        return cls(save_monger.parse_state((SCHEMATICS / level_name / save_name / "circuit.data").read_bytes()), )

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
    def wire_bundles(self) -> list[WireBundle]:
        out = []
        seen = set()
        for wire_set in self.wires_by_position.values():
            if wire_set and seen.isdisjoint(wire_set):
                seen.add(next(iter(wire_set)))
                out.append(WireBundle(list(wire_set)))
        return out

    @cached_property
    def pin_map(self) -> dict[tuple[int, int], tuple[TCComponent, TCPin, int]]:
        pins = {}
        for com in self.components:
            for i, (pos, pin) in enumerate(com.positioned_pins):
                assert pos not in pins, (pos, com)
                pins[pos] = (com, pin, i)
        return pins


CC_PATHS = {}


def _load_cc_meta():
    base = SCHEMATICS / "component_factory"
    for circuit_path in base.rglob("circuit.data"):
        meta = save_monger.parse_state(circuit_path.read_bytes(), True)
        CC_PATHS[meta["save_version"]] = circuit_path


CC_SCHEMATICS = {}


def _get_cc_schematic(cc_id):
    if not CC_PATHS:
        _load_cc_meta()
    if cc_id not in CC_SCHEMATICS:
        assert cc_id in CC_PATHS, cc_id
        CC_SCHEMATICS[cc_id] = TCSchematic(save_monger.parse_state(CC_PATHS[cc_id].read_bytes()))
    return CC_SCHEMATICS[cc_id]


custom_component_classes = {}


class CustomComponent(_NeedsClock):
    def __init_subclass__(cls, **kwargs):
        custom_component_classes[kwargs["custom_id"]] = cls

    @cached_property
    def schematic(self) -> TCSchematic:
        return _get_cc_schematic(self.custom_id)

    @cached_property
    def custom_id(self) -> int:
        return self.raw_nim_data["custom_id"]

    @property
    def pins(self):
        raise ValueError(f"This custom component {type(self).__name__} does not have it's pins specified")

    @property
    def verilog_name(self):
        return f"Custom_{self.custom_id}"


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

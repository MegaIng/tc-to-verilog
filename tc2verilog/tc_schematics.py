import os
import re
import sys
from ast import literal_eval
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from functools import cached_property, partial
from operator import attrgetter
from pathlib import Path
from pprint import pprint

from tc2verilog.base_tc_component import TCComponent, TCPin, IOComponent, Size, NeedsClock as _NeedsClock, In, InSquare, \
    Out, OutTri, Unbuffered

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
    name = re.sub(non_legal, "_", str(name))
    non_legal_starts = r"[^a-zA-Z]"
    if re.match(non_legal_starts, name):
        name = "_" + name
    return name


@dataclass(eq=False)
class TCSchematic:
    raw_nim_data: dict

    @property
    def save_version(self):
        return self.raw_nim_data["save_version"]

    @property
    def dependencies(self):
        return self.raw_nim_data["dependencies"]

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
                obj = Custom(c)
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


PIN_TYPES = {
    0: None,
    1: None,  # Shape
    2: partial(In, size=1),
    3: partial(In, size=8),
    4: partial(In, size=16),
    5: partial(In, size=32),
    6: partial(In, size=64),
    7: partial(InSquare, size=1),
    8: partial(InSquare, size=8),
    9: partial(InSquare, size=16),
    10: partial(InSquare, size=32),
    11: partial(InSquare, size=64),
    12: partial(Out, size=1),
    13: partial(Out, size=8),
    14: partial(Out, size=16),
    15: partial(Out, size=32),
    16: partial(Out, size=64),
    17: partial(OutTri, size=1),
    18: partial(OutTri, size=8),
    19: partial(OutTri, size=16),
    20: partial(OutTri, size=32),
    21: partial(OutTri, size=64),
    22: partial(Unbuffered, size=1),
    23: partial(Unbuffered, size=8),
    24: partial(Unbuffered, size=16),
    25: partial(Unbuffered, size=32),
    26: partial(Unbuffered, size=64),
    27: None,  # 1 bit memory probe
    28: None,  # word memory probe
    29: None,  # 1 bit wire probe
    30: None,  # word wire probe
}


@dataclass
class CustomComponentShape:
    raw: list[list[int]]

    def pair_up(self, schematic: TCSchematic):
        io_components = []
        for component in schematic.components:
            if isinstance(component, IOComponent):
                io_components.append(component)
        io_components.sort(key=attrgetter('pos'))
        # print(list(map(attrgetter('pos'), io_components)))
        # pprint([[self.raw[j][i] for j in range(len(self.raw))] for i in range(len(self.raw[0]))], width=100)
        i = 0
        for x, row in enumerate(self.raw):
            for y, v in enumerate(row):
                assert v in PIN_TYPES, v
                if PIN_TYPES[v] is None:
                    continue
                yield PIN_TYPES[v], (x - 15, y - 15), io_components[i]
                i += 1


@dataclass
class CustomComponentInfo:
    cid: int
    path: Path
    shape: CustomComponentShape | None

    @cached_property
    def schematic(self):
        return TCSchematic(save_monger.parse_state(self.path.read_bytes()))

    @cached_property
    def paired_pins(self):
        return tuple(self.shape.pair_up(self.schematic))

    @cached_property
    def rel_path(self):
        return self.path.relative_to(SCHEMATICS / "component_factory").parent


CUSTOM_COMPONENTS: dict[int, CustomComponentInfo] = {}


def _load_cc_meta():
    custom_designs = {}
    cd_path = BASE_PATH / "custom_designs.txt"
    if cd_path.is_file():
        lines = cd_path.read_text().splitlines()
        for data, shape, _ in zip(lines[0::3], lines[1::3], lines[2::3]):
            cid, time = map(literal_eval, data.split())
            shape = literal_eval(shape)
            custom_designs[cid] = time, CustomComponentShape(shape)
    else:
        print("custom_designs.txt is not generated. Can't use custom components. Type "
              "`export_custom_designs` into the console, which is accessed in the main menu by pressing `q`")

    base = SCHEMATICS / "component_factory"
    for circuit_path in base.rglob("circuit.data"):
        meta = save_monger.parse_state(circuit_path.read_bytes(), True)
        shape = None
        if meta['save_version'] in custom_designs:
            mtime = int(circuit_path.stat().st_mtime)
            if mtime > custom_designs[meta['save_version']][0]:
                print(f"Custom Component {str(circuit_path.relative_to(base).parent)!r} was modified after"
                      f" custom_designs.txt was generated")
            else:
                shape = custom_designs[meta['save_version']][1]
        CUSTOM_COMPONENTS[meta['save_version']] = CustomComponentInfo(meta['save_version'], circuit_path, shape)


def get_cc_info(cc_id) -> CustomComponentInfo:
    if not CUSTOM_COMPONENTS:
        _load_cc_meta()
    return CUSTOM_COMPONENTS[cc_id]


custom_component_classes = {}


@dataclass
class Custom(_NeedsClock):

    def __init_subclass__(cls, **kwargs):
        custom_component_classes[kwargs["custom_id"]] = cls

    @cached_property
    def schematic(self) -> TCSchematic:
        return get_cc_info(self.custom_id).schematic

    @cached_property
    def custom_id(self) -> int:
        return self.raw_nim_data["custom_id"]

    @cached_property
    def custom_info(self) -> CustomComponentInfo:
        return get_cc_info(self.custom_id)

    @cached_property
    def pins(self):
        return [f(name=normalize_name(c.io_name), rel_pos=rel_pos)
                for (f, rel_pos, c) in self.custom_info.paired_pins]

    @property
    def verilog_name(self):
        return normalize_name(self.custom_info.rel_path)


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

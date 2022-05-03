from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Iterator

from tc2verilog.base_tc_component import TCComponent, TCPin, In, OutTri, Out, IOComponent, NeedsClock
from tc2verilog.memory_files import MemoryFile
from tc2verilog.tc_schematics import TCSchematic


@dataclass
class Wire:
    name: str
    size: int
    sources: list[tuple[TCComponent, TCPin, int]]
    targets: list[tuple[TCComponent, TCPin, int]]

    @property
    def subwires(self):
        if len(self.sources) > 1:
            return [self.name, *(f"{self.name}_{i}" for i in range(len(self.sources)))]
        else:
            return [self.name]

    def name_for(self, desc: tuple[TCComponent, TCPin]):
        if len(self.sources) > 1:
            for i, (tcc, tcp, _) in enumerate(self.sources):
                if desc == (tcc, tcp):
                    return f"{self.name}_{i}"
            raise ValueError(desc)
        else:
            return self.name


class VerilogBuilder:
    pass


@dataclass
class VerilogModule:
    module_name: str
    schematic: TCSchematic
    counter: int = 0

    _line_sep = "\n    "

    @cached_property
    def _verilog_wires(self) -> tuple[dict[tuple[int, int], Wire], dict[str, Wire]]:
        groups = defaultdict(list)
        for pos, pin in self.schematic.pin_map.items():
            if self.schematic.wire_map[pos]:
                groups[frozenset(self.schematic.wire_map[pos])].append((pos, pin))
        wires_by_position = {}
        wires_by_name = {}
        for i, group in enumerate(groups.values()):
            sources = [p[1] for p in group if isinstance(p[1][1], (Out, OutTri))]
            targets = [p[1] for p in group if isinstance(p[1][1], (In))]
            assert len(group) == len(sources) + len(targets), (group)
            sizes = {p[1].size for p in sources}
            size = max(sizes, default=1)
            wire = wires_by_name[f"wire{i}"] = Wire(f"wire{i}", size, sources, targets)
            for pos, _ in group:
                wires_by_position[pos] = wire
        return wires_by_position, wires_by_name

    @cached_property
    def wires_by_position(self) -> dict[tuple[int, int], Wire]:
        return self._verilog_wires[0]

    @cached_property
    def wires_by_name(self) -> dict[str, Wire]:
        return self._verilog_wires[1]

    def _build_wires(self):
        wires = [
            f"wire [{wire.size - 1}:0] {name};"
            for wire in self.wires_by_name.values()
            for name in wire.subwires
        ]
        tri_state_wires = [
            f"assign {wire.name} = {' | '.join(wire.subwires[1:])};"
            for wire in self.wires_by_name.values()
            if len(wire.sources) > 1
        ]
        return "\n    ".join(wires), "\n     ".join(tri_state_wires)

    def _connect_wire_port(self, wire: Wire, pin: TCPin, pin_name, desc):
        if isinstance(pin, In):
            target, source = wire, pin
            target_name = wire.name_for(desc)
        else:
            target, source = pin, wire
            target_name = pin_name
        if target.size > source.size:
            value = f"{{{{{target.size - source.size}{{1'b0}}}}, {source.name}}}"
        elif target.size == source.size:
            value = source.name
        else:
            value = f"{source.name}[{target.size - 1}:0]"
        return f"assign {target_name} = {value}"

    def _build_ports(self):
        ports = [("clk", "input wire"), ("rst", "input wire")]
        port_wires = []
        for name, (com, pin, pos) in self.schematic.named_io_pin_by_name.items():
            if pos in self.wires_by_position:
                wire = self.wires_by_position[pos]
            else:
                wire = None
            if isinstance(pin, Out):
                ports.append((name, f"input wire [{pin.size - 1}:0]"))
            else:
                ports.append((name, f"output wire [{pin.size - 1}:0]"))
            if wire:
                port_wires.append(self._connect_wire_port(wire, pin, name, (com, pin)))
        return (
            ", ".join(n for n, _ in ports),
            self._line_sep.join(f'{t} {n};' for n, t in ports),
            self._line_sep.join(port_wires)
        )

    def _build_parameters(self, component):
        if not component.parameters:
            return ""
        return f" # ({', '.join(f'.{n}({v})' for n, v in component.parameters.items())})"

    def _connect_wire_submodule(self, wire: Wire, port: TCPin, comp):
        if isinstance(port, In):
            if port.size > wire.size:
                value = f"{{{{{port.size - wire.size}{{1'b0}}}}, {wire.name}}}"
            elif port.size == wire.size:
                value = wire.name
            else:
                value = f"{wire.name}[{port.size - 1}:0]"
        else:
            if port.size > wire.size:
                raise ValueError("This should never happen; the wires should be large enough to accommodate all inputs")
            elif port.size == wire.size:
                value = wire.name_for((comp, port))
            else:
                value = f"{wire.name_for((comp, port))}[{port.size-1}:0]"
        value = f".{port.name}({value})"
        return value

    def _build_submodule(self, component: TCComponent):
        arguments = [
            self._connect_wire_submodule(self.wires_by_position[pos], p, component)
            if t else f".{p.name}({p.size}'d0)"
            for pos, p in component.positioned_pins
            if (t := (pos in self.wires_by_position)) or isinstance(p, In)
        ]
        if isinstance(component, NeedsClock):
            arguments = ['.clk(clk)', '.rst(rst)'] + arguments
        self.counter += 1
        params = self._build_parameters(component)
        if component.name is not None:
            return f"TC_{component.verilog_name}{params} {component.name} ({', '.join(arguments)});"
        else:
            return f"TC_{component.verilog_name}{params} {type(component).__name__}_{self.counter} ({', '.join(arguments)});"

    def _build_submodules(self):
        return self._line_sep.join(
            self._build_submodule(component)
            for component in self.schematic.components
            if not isinstance(component, IOComponent)
        )

    def full_verilog(self) -> str:
        module_name = self.module_name
        port_names, port_decls, port_wires_assigns = self._build_ports()
        wire_declarations, tri_state_joins = self._build_wires()
        sub_modules = self._build_submodules()
        return f"""
module {module_name}(
    {port_names}
);
    {port_decls}

    {wire_declarations}
    
    {tri_state_joins}

    {port_wires_assigns}

    {sub_modules}

endmodule
"""

    def memory_files(self) -> Iterator[MemoryFile]:
        for component in self.schematic.components:
            yield from component.memory_files


def output_verilog(out_folder: Path, module_name: str, schematic: TCSchematic, schematic_folder=None):
    out_folder.mkdir(parents=True, exist_ok=True)

    module = VerilogModule(module_name, schematic)

    (out_folder / f"{module_name}.v").write_text(module.full_verilog())

    for file in module.memory_files():
        (out_folder / file.out_file).write_text(file.get_hex_content(schematic_folder))

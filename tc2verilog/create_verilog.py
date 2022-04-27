from _operator import itemgetter
from collections import defaultdict
from dataclasses import dataclass

from tc2verilog.tc_schematics import TCSchematic, TCComponent, TCPin, In, OutTri, Out, IOComponent


@dataclass
class Wire:
    wire_name: str
    wire_size: int
    sources: list[tuple[TCComponent, TCPin, int]]
    targets: list[tuple[TCComponent, TCPin, int]]


def create_wires(schematic: TCSchematic) -> tuple[dict[tuple[int, int], Wire], dict[str, Wire]]:
    groups = defaultdict(list)
    for pos, pin in schematic.pin_map.items():
        groups[frozenset(schematic.wire_map[pos])].append((pos, pin))
    wires_by_position = {}
    wires_by_name = {}
    for i, group in enumerate(groups.values()):
        sources = [p[1] for p in group if isinstance(p[1][1], (Out, OutTri))]
        targets = [p[1] for p in group if isinstance(p[1][1], (In))]
        assert len(group) == len(sources) + len(targets), (group)
        sizes = {p[1][1].size for p in group}
        assert len(sizes) == 1, sizes
        size, = sizes
        wire = wires_by_name[f"wire{i}"] = Wire(f"wire{i}", size, sources, targets)
        for pos, _ in group:
            wires_by_position[pos] = wire
    return wires_by_position, wires_by_name


def output_verilog(name: str, schematic: TCSchematic) -> str:
    counter = 0

    def build_submodule(component: TCComponent):
        nonlocal counter
        arguments = [
            f'.{p.name}({wires_by_position[pos].wire_name})'
            for pos, p in component.positioned_pins
        ]
        counter += 1
        return f"{component.verilog_name} {component.verilog_name}_{counter} ({', '.join(arguments)});"

    wires_by_position, wires_by_name = create_wires(schematic)

    wires = [
        f"wire [{wire.wire_size-1}:0] {wire.wire_name};"
        for wire in wires_by_name.values()
    ]
    wire_strings = "\n    ".join(wires)
    ports = (
        ("clock", "input wire"), ("reset", "input wire"),
        *sorted(((name, pin.verilog_type) for name, pin in schematic.named_io_by_name.items())),
    )
    port_string = ',\n    '.join(f'{t} {name}' for name, t in ports)

    sub_modules = [
        build_submodule(component)
        for component in schematic.components
        if not isinstance(component, IOComponent)
    ]
    sub_modules_strings = '\n    '.join(sub_modules)

    port_wires = []
    for name, pin in schematic.named_io_by_name.items():
        pos, p = pin.positioned_pins[0]
        wire = wires_by_position[pos]
        if isinstance(p, Out):
            port_wires.append(f"assign {wire.wire_name} = {name};")
        else:
            port_wires.append(f"assign {name} = {wire.wire_name};")
    port_wire_string = '\n    '.join(port_wires)

    return f"""
module {name}(
    {port_string}
);
    {wire_strings}
    
    {port_wire_string}
    
    {sub_modules_strings}
    
endmodule
"""

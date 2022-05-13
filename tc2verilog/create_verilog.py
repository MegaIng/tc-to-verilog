from __future__ import annotations

from _operator import itemgetter
from abc import abstractmethod, ABC
from builtins import abs
from collections import defaultdict
from dataclasses import dataclass, field
from os import PathLike
from pathlib import Path
from typing import Iterator, TypeAlias, Callable, Any, Sequence

import json

from tc2verilog.base_tc_component import TCComponent, In, Out, OutTri, Unbuffered
from tc2verilog.memory_files import MemoryFile
from tc2verilog.tc_components import _Input, _SimpleInput, Input1_1B, Output1_1B, _SimpleOutput, _OutputSSz, \
    _Bidirectional
from tc2verilog.tc_schematics import TCSchematic, normalize_name, get_cc_info, LevelInfo

"""
A Generator handles some specific type of objects, possibly calling sub generators in the process,
calling methods on a VerilogModule instance in the process, building the needed statements in the process.

VerilogModule
-> add_wire(name: str) -> (Target, Source)
-> add_in_port(name: str, size: int) -> Source
-> add_out_port(name: str, size: int) -> Target
-> add_submodule(...<Everything needed to construct a VerilogSubmodule instance>...)
-> add_assign(target: SignalTarget, source: SignalSource)


- VerilogWire/VerilogInPort/VerilogOutPort
  - name
  - size
- VerilogAssign
  - sources: list[Source]
  - target: Target
- VerilogSubmodule
    - module_name
    - name
    - parameters: dict[str, VerilogValue]
    - inputs: dict[str, tuple[Source, int]]
    - outputs: dict[str, tuple[Target, int]]

Sources are:
- Normal Wires
- Tristate Wires
- Input ports (normal input and bidirectional)
- FixedValueSource

Targets are:
- Normal wires
- Tristate wires
- output ports (normal output, tristate output x2, bidirectional)

"""


class VerilogValue(ABC):
    @abstractmethod
    def get_verilog(self, module: VerilogModule) -> str:
        pass


@dataclass
class VInt(VerilogValue):
    value: int
    size: int = None

    def get_verilog(self, module: VerilogModule):
        if self.size is None:
            return str(self.value)
        else:
            return f"{self.size}'d{self.value}"


@dataclass
class VUUID(VerilogValue):
    value: int

    def get_verilog(self, module: VerilogModule):
        return f"{self.value} ^ UUID"


@dataclass
class VString(VerilogValue):
    value: str

    def get_verilog(self, module: VerilogModule):
        return f'"{self.value}"'


@dataclass(eq=False)
class Target:
    name: str


@dataclass(eq=False)
class Source:
    name: str


@dataclass
class FullOutput:
    modules: dict[str, VerilogModule] = field(default_factory=dict)
    component_info: defaultdict[str, list[dict[str, Any]]] = field(default_factory=lambda: defaultdict(list))
    pin_info: defaultdict[str, dict[str, dict[str, Any]]] = field(default_factory=lambda: defaultdict(dict))
    memory_files: list[MemoryFile] = field(default_factory=list)

    def add_component_info(self, module_name: str, info: dict[str, Any]):
        self.component_info[module_name].append(info)

    def add_pin_info(self, module_name: str, pin_name: str, info: dict[str, Any]):
        assert pin_name not in self.pin_info[module_name], pin_name
        self.pin_info[module_name][pin_name] = info

    def add_module(self, name: str) -> VerilogModule:
        if name in self.modules:
            raise ValueError(f"Duplicate module name {name!r}")
        self.modules[name] = m = VerilogModule(self, name)
        return m

    def add_memory_file(self, memory_files: Sequence[MemoryFile], schematic_folder=None):
        for mf in memory_files:
            if schematic_folder is not None:
                mf.schematic_folder = schematic_folder
            self.memory_files.append(mf)

    def generate_recursive(self, level_name: str, schematic_name: str, prefix: str = ''):
        print(level_name, schematic_name)
        schematic = TCSchematic.open_level(level_name, schematic_name)
        if normalize_name(prefix + str(schematic_name)) in self.modules:
            return
        module = self.add_module(normalize_name(prefix + str(schematic_name)))
        gen = SchematicGenerator(schematic)
        gen.generate(module)
        for cc_id in schematic.dependencies:
            cc_info = get_cc_info(cc_id)
            self.generate_recursive("component_factory", cc_info.rel_path, prefix='TC_')

    def output_to(self, folder: Path, assume_level: LevelInfo = 86):
        folder.mkdir(parents=True, exist_ok=True)
        for name, module in self.modules.items():
            path = folder / f"{name}.v"
            path.write_text(module.get_verilog())
        for memory_file in self.memory_files:
            (folder / memory_file.out_file).write_bytes(memory_file.get_padded_content(assume_level.enum_number))
        with (folder / "components.json").open("w") as f:
            json.dump({
                "modules": {
                    name: {
                        "components": self.component_info[name],
                        "pins": self.pin_info[name],
                    }
                    for name in self.modules
                }
            }, f, indent=2)


STANDARD_PARAMETERS_TO_VERILOG: dict[str, Callable[[Any], VerilogValue]] = {
    "BIT_WIDTH": VInt,
    "BIT_DEPTH": VInt,
    "FILE_BYTES": VInt,

    "ARG_SIG": VString,
    "HEX_FILE": VString,

    "value": lambda t: VInt(*t),
    "count": lambda t: VInt(*t),
}

STANDARD_PARAMETERS_TO_JSON: dict[str, Callable[[Any], Any] | None] = {
    "BIT_WIDTH": lambda d: d,
    "BIT_DEPTH": lambda d: d,
    "FILE_BYTES": lambda d: d,

    "ARG_SIG": lambda d: d,
    "HEX_FILE": lambda d: d,

    "value": lambda t: t[0],
    "count": lambda t: t[0],
}


@dataclass
class _VerilogWire:
    name: str
    output: Source
    input: Target
    size: int = 1

    def get_verilog(self, module: VerilogModule):
        return f"wire [{self.size - 1}:0] {self.name};"


@dataclass
class _VerilogInPort:
    name: str
    size: int
    output: Source

    def get_verilog(self, module: VerilogModule):
        return f"input wire [{self.size - 1}:0] {self.name};"


@dataclass
class _VerilogOutPort:
    name: str
    size: int
    input: Target

    def get_verilog(self, module: VerilogModule):
        return f"output wire [{self.size - 1}:0] {self.name};"


@dataclass
class _VerilogSubmodule:
    module_name: str
    name: str
    parameters: dict[str, VerilogValue]
    inputs: dict[str, tuple[Source, int]]
    outputs: dict[str, tuple[Target, int]]

    def _format_parameters(self, module: VerilogModule) -> str:
        assert all(isinstance(v, VerilogValue) for v in self.parameters.values()), self.parameters
        if not self.parameters:
            return ""
        out = [f'.{name}({value.get_verilog(module)})' for name, value in self.parameters.items()]
        return f' # ({", ".join(out)})'

    def _format_ports(self, module: VerilogModule) -> str:
        out = []
        for name, (source, size) in self.inputs.items():
            out.append(f'.{name}({module.get_source_verilog(source, size)})')
        for name, (target, size) in self.outputs.items():
            out.append(f'.{name}({module.get_target_verilog(target, size)})')
        return f'({", ".join(out)})'

    def get_verilog(self, module: VerilogModule) -> str:
        return f"{self.module_name}{self._format_parameters(module)} {self.name} {self._format_ports(module)};"


@dataclass
class _VerilogAssign:
    target: Target
    sources: list[Source]

    def get_verilog(self, module: VerilogModule):
        ts = module.get_target_size(self.target)
        sources = [module.get_source_verilog(s, ts) for s in self.sources]
        return f"assign {module.get_target_verilog(self.target, ts)} = {' | '.join(sources)};"


@dataclass
class _VerilogConstant:
    value: int
    size: int
    source: Source


@dataclass
class VerilogModule:
    full_output: FullOutput
    name: str
    _source_definitions: dict[Source, _VerilogWire | _VerilogInPort | _VerilogConstant] = field(default_factory=dict)
    _target_definitions: dict[Target, _VerilogWire | _VerilogOutPort] = field(default_factory=dict)
    _assigns: dict[Target, _VerilogAssign] = field(default_factory=dict)
    _wires: list[_VerilogWire] = field(default_factory=list)
    _ports: list[_VerilogInPort | _VerilogOutPort] = field(default_factory=list)
    _submodules: list[_VerilogSubmodule] = field(default_factory=list)

    def get_constant(self, size: int, value: int) -> Source:
        self._source_definitions[s] = _VerilogConstant(value, size, s := Source(f"{size}'d{value}"))
        return s

    def add_wire(self, name: str) -> (Target, Source):
        self._wires.append(w := _VerilogWire(name, s := Source(name), t := Target(name)))
        self._source_definitions[s] = w
        self._target_definitions[t] = w
        return t, s

    def add_output(self, name: str, size: int) -> Target:
        self._ports.append(p := _VerilogOutPort(name, size, t := Target(name)))
        self._target_definitions[t] = p
        return t

    def add_input(self, name: str, size: int) -> Source:
        self._ports.append(p := _VerilogInPort(name, size, s := Source(name)))
        self._source_definitions[s] = p
        return s

    def _register_target(self, source: Source, size: int = None):
        obj = self._source_definitions[source]

    def _register_source(self, target: Target, size: int = None):
        obj = self._target_definitions[target]
        if isinstance(obj, _VerilogWire):
            if size is not None:
                obj.size = max(obj.size, size)

    def add_assign(self, source: Source, target: Target):
        if target in self._assigns:
            self._assigns[target].sources.append(source)
        else:
            self._assigns[target] = _VerilogAssign(target, [source])
        self._register_target(source, self.get_target_size(target))
        self._register_source(target, self.get_source_size(source))

    def add_submodule(self, module_name: str, name: str, parameters: dict[str, VerilogValue],
                      inputs: dict[str, tuple[Source, int]], outputs: dict[str, tuple[Target, int]]):
        self._submodules.append(_VerilogSubmodule(module_name, name, parameters, inputs, outputs))
        for port, (source, size) in inputs.items():
            self._register_target(source, size)
        for port, (target, size) in outputs.items():
            self._register_source(target, size)

    def split_wire(self, wire_target: Target, wire_source: Source) -> (Source, Target):
        """
        wire_target ----------------------wire---------------------> wire_source
        wire_target --wire--> split_source ?? split_target --wire--> wire_source
        """
        old_wire = self._source_definitions[wire_source]
        assert isinstance(old_wire, _VerilogWire), old_wire
        split_source, split_target = Source(f"split_source"), Target(f"split_target")
        old_wire.input = wire_target
        old_wire.output = split_source

        new_wire = _VerilogWire(f"{old_wire.name}_split", wire_source, split_target, old_wire.size)
        self._wires.append(new_wire)

        old_wire.input.name = old_wire.output.name = old_wire.name
        new_wire.input.name = new_wire.output.name = new_wire.name

        self._source_definitions[old_wire.output] = old_wire
        self._source_definitions[new_wire.output] = new_wire

        self._target_definitions[old_wire.input] = old_wire
        self._target_definitions[new_wire.input] = new_wire

        return split_source, split_target

    def get_source_verilog(self, source: Source, size: int) -> str:
        obj = self._source_definitions[source]
        if obj.size == size:
            return source.name
        elif obj.size < size:
            return f"{{{{{size - obj.size}{{1'b0}}}}, {source.name}}}"
        else:
            return f"{source.name}[{size - 1}:0]"

    def get_target_size(self, target: Target) -> int:
        obj = self._target_definitions[target]
        return obj.size

    def get_source_size(self, source: Source) -> int:
        obj = self._source_definitions[source]
        return obj.size

    def get_target_verilog(self, target: Target, size: int) -> str:
        obj = self._target_definitions[target]
        if obj.size == size:
            return target.name
        elif obj.size > size:
            return f"{target.name}[{size - 1}:0]"
        else:
            raise NotImplementedError(target, obj, size)

    def add_component_info(self, info: dict[str, Any]):
        self.full_output.add_component_info(self.name, info)

    def add_pin_info(self, pin_name: str, info: dict[str, Any]):
        self.full_output.add_pin_info(self.name, pin_name, info)

    def get_verilog(self) -> str:
        ports = ', '.join(('clk', 'rst',
                           *(p.name for p in self._ports)))
        port_definitions = '\n    '.join((
            'input wire clk;',
            'input wire rst;',
            *(p.get_verilog(self) for p in self._ports)))
        wire_definitions = '\n    '.join(w.get_verilog(self) for w in self._wires)
        submodules = '\n    '.join(s.get_verilog(self) for s in self._submodules)
        assigns = '\n    '.join(a.get_verilog(self) for a in self._assigns.values())
        return f"""
module {self.name}(
    {ports}
);
    parameter UUID = 0;
    parameter NAME = "";
    {port_definitions}
    
    {wire_definitions}
    
    {assigns}
    
    {submodules}
    
endmodule
"""


@dataclass
class SchematicGenerator:
    schematic: TCSchematic
    sources_by_position: dict[tuple[int, int], Source] = field(default=None, init=False, repr=False, compare=False)
    targets_by_position: dict[tuple[int, int], Target] = field(default=None, init=False, repr=False, compare=False)

    def generate(self, module: VerilogModule):
        self.sources_by_position = {}
        self.targets_by_position = {}
        for i, tc_wire in enumerate(self.schematic.wire_bundles):
            target, source = module.add_wire(tc_wire.get_safe_name(i))
            for p in tc_wire.positions:
                self.sources_by_position[p] = source
                self.targets_by_position[p] = target

        for i, tc_component in enumerate(self.schematic.components):
            self.get_generator(i, tc_component).generate(module)

    def get_generator(self, i: int, comp: TCComponent) -> ComponentGenerator:
        matching = []
        for p, ts, cls in generator_registry:
            if isinstance(comp, ts):
                matching.append((p, cls))
        cutoff = max(matching, key=itemgetter(0), default=0)[0]
        matching = [cls for p, cls in matching if p >= cutoff]
        if len(matching) == 0:
            raise ValueError(f"No generator found for {type(comp).__name__}")
        if len(matching) > 1:
            raise ValueError(f"Multiple generators found for {type(comp).__name__} with same priority: {matching}")
        return matching[0](i, self, comp)


generator_registry: list[
    tuple[float, type | tuple[type, ...], Callable[[int, SchematicGenerator, TCComponent], ComponentGenerator]]] = []


@dataclass
class ComponentGenerator(ABC):
    i: int
    base: SchematicGenerator
    component: TCComponent

    def __init_subclass__(cls, **kwargs):
        if "components" in kwargs:
            generator_registry.append((kwargs.pop("priority"), kwargs.pop("components"), cls))

    def output_component_info(self, module: VerilogModule, **extra):
        info = {
            "kind": type(self.component).__name__,
            "id": hex(self.component.permanent_id),
            "name": self.component.name_id,
            "position": self.component.pos,
            "rotation": self.component.rotation,
        }
        info.update(extra)
        module.add_component_info(info)

    @abstractmethod
    def generate(self, module: VerilogModule):
        raise NotImplementedError


class SimpleInputGenerator(ComponentGenerator, priority=1, components=_SimpleInput):
    def generate(self, module: VerilogModule):
        for pos, port in self.component.positioned_pins:
            match port:
                case Out(name, _, size):
                    source = module.add_input(pin_name := normalize_name(self.component.io_name), size)
                    target = self.base.targets_by_position[pos]
                    module.add_assign(source, target)
                    module.add_pin_info(pin_name, {
                        'position': pos,
                        'bit_width': size,
                        'kind': "input",
                        'name': name
                    })
                case _:
                    raise ValueError(port)


class SimpleOutputGenerator(ComponentGenerator, priority=1, components=_SimpleOutput):
    component: _SimpleOutput

    def generate(self, module: VerilogModule):
        for pos, port in self.component.positioned_pins:
            match port:
                case In(name, _, size):
                    target = module.add_output(pin_name := normalize_name(self.component.io_name), size)
                    source = self.base.sources_by_position[pos]
                    module.add_assign(source, target)
                    module.add_pin_info(pin_name, {
                        'position': pos,
                        'bit_width': size,
                        'kind': "output",
                        'name': name
                    })
                case _:
                    raise ValueError(port)


class ArchInputGenerator(ComponentGenerator, priority=1, components=Input1_1B):
    def generate(self, module: VerilogModule):
        (cont_pos, cont_port), (value_pos, value_port) = self.component.positioned_pins

        source = self.base.sources_by_position[cont_pos]
        target = module.add_output(f"arch_in_control", 1)
        module.add_assign(source, target)
        module.add_pin_info("arch_in_control", {
            'position': cont_pos,
            'bit_width': 1,
            'kind': "output",
            'name': f"arch_in_control"
        })

        source = module.add_input(f"arch_in_value", 8)
        target = self.base.targets_by_position[value_pos]
        module.add_assign(source, target)
        module.add_pin_info("arch_in_value", {
            'position': value_pos,
            'bit_width': 8,
            'kind': "input",
            'name': f"arch_in_value"
        })


class ArchOutputGenerator(ComponentGenerator, priority=1, components=Output1_1B):
    def generate(self, module: VerilogModule):
        (cont_pos, cont_port), (value_pos, value_port) = self.component.positioned_pins

        source = self.base.sources_by_position[cont_pos]
        target = module.add_output(f"arch_out_control", 1)
        module.add_assign(source, target)
        module.add_pin_info("arch_out_control", {
            'position': cont_pos,
            'bit_width': 1,
            'kind': "output",
            'name': f"arch_out_control"
        })

        source = self.base.sources_by_position[value_pos]
        target = module.add_output(f"arch_out_value", 8)
        module.add_assign(source, target)
        module.add_pin_info("arch_out_value", {
            'position': value_pos,
            'bit_width': 8,
            'kind': "output",
            'name': f"arch_out_value"
        })


class TriStateOutputGenerator(ComponentGenerator, priority=1, components=_OutputSSz):
    component: _OutputSSz

    def generate(self, module: VerilogModule):
        (cont_pos, cont_port), (value_pos, value_port) = self.component.positioned_pins

        cont_source = self.base.sources_by_position[cont_pos]
        value_source = self.base.sources_by_position[value_pos]

        out_target = module.add_output(pin_name := normalize_name(self.component.io_name), self.component.size)
        module.add_pin_info(pin_name, {
            'position': value_pos,
            'bit_width': self.component.size,
            'kind': "output",
            'name': "in"
        })

        module.add_submodule(
            module_name="TC_Switch",
            name=normalize_name(f"Switch_Output{self.component.size}z_{self.component.name_id}_{self.i}"),
            parameters={
                "UUID": VUUID(self.component.permanent_id),
                "NAME": VString(self.component.name_id),
                "BIT_WIDTH": VInt(self.component.size),
            },
            inputs={
                "en": (cont_source, 1),
                "in": (value_source, self.component.size),
            },
            outputs={
                "out": (out_target, self.component.size)
            }
        )


class BidirectionalPinGenerator(ComponentGenerator, priority=1, components=_Bidirectional):
    component: _Bidirectional

    def generate(self, module: VerilogModule):
        (value_pos, value_port), = self.component.positioned_pins
        out_target = module.add_output(pin_name := normalize_name(f"{self.component.io_name}_uout"),
                                       self.component.size)
        module.add_pin_info(pin_name, {
            'position': value_pos,
            'bit_width': self.component.size,
            'kind': "bidirectional_output",
            'name': "uout"
        })
        in_source = module.add_input(pin_name := normalize_name(f"{self.component.io_name}_uin"), self.component.size)
        module.add_pin_info(pin_name, {
            'position': value_pos,
            'bit_width': self.component.size,
            'kind': "bidirectional_input",
            'name': "uin"
        })

        if not (value_pos in self.base.sources_by_position and value_pos in self.base.targets_by_position):
            return
        value_source = self.base.sources_by_position[value_pos]
        value_target = self.base.targets_by_position[value_pos]
        split_source, split_target = module.split_wire(value_target, value_source)
        module.add_assign(split_source, out_target)
        module.add_assign(in_source, split_target)
        module.add_assign(split_source, split_target)


class SimpleComponentGenerator(ComponentGenerator, priority=0, components=TCComponent):
    def generate_parent_unbuffered(self, module: VerilogModule, name: str, wire_target: Target,
                                   wire_source: Source) -> tuple[tuple[str, Source], tuple[str, Target]]:
        temp_target, temp_source = module.add_wire(f"unbuffered_{self.component.name_id}_{self.i}_{name}_temp")
        split_source, split_target = module.split_wire(wire_target, wire_source)
        module.add_assign(split_source, split_target)
        module.add_assign(temp_source, split_target)
        return (f"{name}_uin", wire_source), (f"{name}_uout", temp_target)

    def generate(self, module: VerilogModule):
        inputs: dict[str, tuple[Source, int]] = {}
        outputs: dict[str, tuple[Target, int]] = {}
        for pos, port in self.component.positioned_pins:
            match port:
                case In(name, _, size):
                    if pos in self.base.sources_by_position:
                        inputs[name] = self.base.sources_by_position[pos], size
                    else:
                        inputs[name] = module.get_constant(size, 0), size
                case Out(name, _, size):
                    if pos in self.base.targets_by_position:
                        outputs[name] = self.base.targets_by_position[pos], size
                case Unbuffered(name, _, size):
                    if pos not in self.base.sources_by_position:
                        continue
                    if pos not in self.base.targets_by_position:
                        continue
                    source = self.base.sources_by_position[pos]
                    target = self.base.targets_by_position[pos]
                    inp, out = self.generate_parent_unbuffered(module, name, target, source)
                    inputs[inp[0]] = inp[1], size
                    outputs[out[0]] = out[1], size
                case _:
                    raise NotImplementedError(port)

        module.add_submodule(
            module_name=(m_name := "TC_" + self.component.verilog_name),
            name=(v_name := normalize_name(f"{self.component.verilog_name}_{self.component.name_id}_{self.i}")),
            parameters={
                "UUID": VUUID(self.component.permanent_id),
                "NAME": VString(self.component.name_id),
                **{name: STANDARD_PARAMETERS_TO_VERILOG[name](v)
                   for name, v in self.component.parameters.items()}
            },
            inputs=inputs,
            outputs=outputs
        )
        parameters = {name: f(v) for name, v in self.component.parameters.items()
                      if (f := STANDARD_PARAMETERS_TO_JSON[name]) is not None}
        self.output_component_info(
            module,
            module_name=m_name,
            verilog_name=v_name,
            **parameters
        )
        module.full_output.add_memory_file(self.component.memory_files, self.base.schematic.folder)

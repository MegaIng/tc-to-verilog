from pathlib import Path
from pprint import pprint

from tc2verilog.base_tc_component import In, Out, InSquare, OutTri
from tc2verilog.create_verilog import output_verilog
from tc2verilog.tc_schematics import TCSchematic, SCHEMATICS, CustomComponent, CC_PATHS, _load_cc_meta, \
    custom_component_classes


# schematic = TCSchematic.open_level("decoder3", "Default", {
#     "in": ("Input3Pin", {"value0": "a", "value1": "b", "value2": "c"}),
#     "out_0": ("Output4Pin", {"value0": "out_000", "value1": "out_001", "value2": "out_010", "value3": "out_011"}),
#     "out_1": ("Output4Pin", {"value0": "out_100", "value1": "out_101", "value2": "out_110", "value3": "out_111"}),
# })
#
# print(output_verilog("decoder3", schematic), file=open("decoder3.v", "w"))


# schematic = TCSchematic.open_level("architecture/ASIC", "ai_showdown", {
#     "arch_out": ("Output1_1B", None),
#     "arch_in": ("Input1_1B", None),
# })
#
# print(output_verilog("test_ai_showdown", schematic), file=open("ai_showdown.v", "w"))

class COND(CustomComponent, custom_id=2868461077671670126):
    pins = [
        In("Condition", (-1, -1), 8),
        In("Input", (-1, 0), 8),
        Out("Result", (2, 0), 1),
    ]


class ALU(CustomComponent, custom_id=378087704930129977):
    pins = [
        In("Instruction", (-1, -1), 8),
        In("Input 1", (-1, 0), 8),
        In("Input 2", (-1, 1), 8),
        Out("Output", (2, 0), 8),
    ]


class DEC(CustomComponent, custom_id=3095061992549240963):
    pins = [
        In("OPCODE", (-1, 0), 8),
        Out("IMMEDIATE", (1, -1), 1),
        Out("CALCULATION", (1, 0), 1),
        Out("COPY", (1, 1), 1),
        Out("CONDITION", (1, 2), 1),
    ]


class RegisterPlus(CustomComponent, custom_id=688062441):
    pins = [
        In("Load", (-1, -1), 1),
        InSquare("Save", (-1, 0), 1),
        InSquare("Save Value", (-1, 1), 8),
        OutTri("Output", (1, 0), 8),
        Out("Always output", (1, 1), 8),
    ]


from pprint import pprint
from tc2verilog.tc_schematics import CC_PATHS, _load_cc_meta

_load_cc_meta()
pprint(CC_PATHS)
schematic = TCSchematic.open_level("architecture", "OVERTURE", {
    "arch_out": ("Output1_1B", None),
    "arch_in": ("Input1_1B", None),
})

output_verilog(Path("out", "OVERTURE"), "OVERTURE", schematic, SCHEMATICS / "architecture" / "OVERTURE")


for cid, cls in custom_component_classes.items():
    print(cls)
    schematic = TCSchematic.open_level("component_factory", f"OVERTURE/{cls.__name__}")
    output_verilog(Path("out", "OVERTURE"), f"TC_{schematic.custom_component_id}", schematic)

#
# schematic = TCSchematic.open_level("component_factory/tc-to-veri", "test_constant")
#
#
# print(output_verilog("test_constant", schematic), file=open("test_constants.v", "w"))

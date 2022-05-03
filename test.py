from pathlib import Path
from pprint import pprint

from tc2verilog.create_verilog import output_verilog
from tc2verilog.tc_schematics import TCSchematic, SCHEMATICS

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

schematic = TCSchematic.open_level("architecture", "OVERTURE", {
    "arch_out": ("Output1_1B", None),
    "arch_in": ("Input1_1B", None),
})

print(output_verilog("OVERTURE", schematic), file=open("OVERTURE.v", "w"))
output_verilog(Path("out", "test"), "test", schematic, SCHEMATICS / "architecture" / "test")

#
# schematic = TCSchematic.open_level("component_factory/tc-to-veri", "test_constant")
#
#
# print(output_verilog("test_constant", schematic), file=open("test_constants.v", "w"))

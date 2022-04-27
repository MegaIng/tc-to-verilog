from tc2verilog.create_verilog import output_verilog
from tc2verilog.tc_schematics import TCSchematic

# schematic = TCSchematic.open_level("full_adder", "Default")
#
#
# print(output_verilog("full_adder", schematic))


schematic = TCSchematic.open_level("component_factory/tc-to-veri", "test_constant")


print(output_verilog("test_constant", schematic), file=open("test_constants.v", "w"))

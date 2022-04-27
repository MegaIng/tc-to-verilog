from tc2verilog.create_verilog import output_verilog
from tc2verilog.tc_schematics import TCSchematic

schematic = TCSchematic.open_level("full_adder", "Default")


print(output_verilog("full_adder", schematic))

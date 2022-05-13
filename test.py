from pprint import pprint

from tc2verilog.create_verilog import *

schematic = TCSchematic.open_level("architecture", "ASIC/planet_names")

# pprint(schematic.raw_nim_data["components"])
# schematic = TCSchematic.open_level("component_factory", "OVERTURE/RegisterPlus")

# pprint(schematic.raw_nim_data["components"])
output = FullOutput()
print(schematic.save_version)

module = output.add_module("planet_names")

SchematicGenerator(schematic).generate(module)
print(module.get_verilog(), file=open("test.v", "w"))
print(module.get_verilog())

pprint(output.component_info)
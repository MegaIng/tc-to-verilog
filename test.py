from pathlib import Path
from pprint import pprint

from tc2verilog.create_verilog import *


# pprint(schematic.raw_nim_data["components"])
# schematic = TCSchematic.open_level("component_factory", "OVERTURE/RegisterPlus")

# pprint(schematic.raw_nim_data["components"])
output = FullOutput()
output.generate_recursive("architecture", "OVERTURE")
output.output_to(Path('out', 'OVERTURE'))

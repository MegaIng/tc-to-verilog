from pprint import pprint

from tc2verilog.create_verilog import *
from tc2verilog.tc_schematics import levels

output = FullOutput()

output.generate_recursive("architecture", "test")
output.output_to(Path('out', 'test'), assume_level=levels.lookup("sandbox"))

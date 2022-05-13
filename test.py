from pprint import pprint

from tc2verilog.create_verilog import *
from tc2verilog.tc_schematics import CUSTOM_COMPONENTS, _load_cc_meta, get_cc_info

_load_cc_meta()
# pprint(CUSTOM_COMPONENTS, width=300, depth=2)
# pprint(get_cc_info(1996601331511151107), width=300)
# pprint(get_cc_info(1996601331511151107).paired_pins, width=300)

output = FullOutput()
# output.generate_recursive("architecture", "test 2")
# output.output_to(Path('out', 'test 2'))
#
output.generate_recursive("architecture", "Grape ETCa")
output.output_to(Path('out', 'Grape ETCa'))

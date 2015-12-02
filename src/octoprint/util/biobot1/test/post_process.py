
from octoprint.util import biobot1

filename = './test_files/biobots_part_lattice.gcode'
e1_pos = 0
e1_Zoffset = 2

e2_pos = 17
e2_Zoffset = 4

X_offset = 49

biobot1.post_process(filename,
                     e1_pos, e1_Zoffset,
                     e2_pos, e2_Zoffset,
                     X_offset)

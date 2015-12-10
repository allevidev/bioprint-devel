#!/usr/bin/env python

# WARNING: This script changes its input file in-place
# This is a Slic3r post-processing script to add
# M106 after E1.000 lines and M107, M126, M127 after each E peak.

# pseudocode
# when there is a clear change in extruder required
# stop extrusion
# move dual extruder stepper to a known angle in steps for "E1"
# move in X as much as the extruders are offset (direction!)
# move dual extruder stepper to a known angle in steps for "E2"
# start extrusion
# resume motion script


import re

# from octoprint.settings import settings

e_rate = 100.00
x_rate = 1800.00

e_pattern = 'E([+-]?\d+(?:\.\d+)?)'
g_pattern = 'G([+-]?\d+(?:\.\d+)?)'
m_pattern = 'M([+-]?\d+(?:\.\d+)?)'
t_pattern = 'T(\d+\.\d+|\.\d+|\d+)'
z_pattern = 'Z([+-]?\d+(?:\.\d+)?)'

def g_code(line):
    '''
    Identify and returns M code on a line, for example returns
    28 for this line: "G28"
    If no G found it returns None
    '''
    if line.strip().startswith(';'):
        return None
    res = re.findall(g_pattern, line.upper())
    return None if res == [] else int(res[0])

def m_code(line):
    '''
    Identify and returns M code on a line, for example returns
    109 for this line: "M104 S200"
    If no M found it returns None
    '''
    if line.strip().startswith(';'):
        return None
    res = re.findall(m_pattern, line.upper())
    return None if res == [] else int(res[0])


def e_value(line):
    '''
    Identify and returns the value of E on a line, for example
    returns 1.81780 for this line: "G1 X13.932 Y45.135 E1.81780"
    If no E found it return None
    '''
    if line.strip().startswith(';'):
        return None
    res = re.findall(e_pattern, line.upper())
    return None if res == [] else float(res[0])


def remove_e(line):
    '''
    Remove the E value from a line, for example
    returns "G1 X13.932 Y45.135" on input "G1 X13.932 Y45.135 E1.81780"
    '''
    return ' '.join(filter(lambda x: x != '', [i.strip() if e_value(i) is None else ''.strip() for i in line.split(' ')]))


def t_value(line):
    '''
    Identify and returns the value of E on a line, for example
    returns 1.81780 for this line: "G1 X13.932 Y45.135 E1.81780"
    If no E found it return None
    '''
    if line.strip().startswith(';'):
        return None
    res = re.findall(t_pattern, line.upper())
    return None if res == [] else float(res[0])


def z_value(line):
    '''
    Identify and returns the value of Z on a line, for example
    returns 1.81780 for this line "G1 Z1.81780"
    If no Z found it returns None
    '''
    if line.strip().startswith(';'):
        return None
    res = re.findall(z_pattern, line.upper())
    return None if res == [] else float(res[0])


def next_z(z_vals, lines, ind):
    '''
    Returns the next z-value just after item ind.
    It skips lines without Z values.
    It returns the value and its container line.
    '''
    for i in range(ind + 1, len(z_vals)):
        if z_vals[i] is not None:
            return z_vals[i], lines[i]
    return None, None


def home_xy():
    return 'G28 X Y'


def home_z():
    return 'G28 Z'


def home_e():
    return 'G28 E'


def start_extrude(extruder, e0_pos, e1_pos):
    if extruder is 0:
        onPin = 16
        target = e0_pos
    elif extruder is 1:
        onPin = 17
        target = e1_pos
    commands = [
        'G1 E' + str(target) + ' F100',
        'M400 ; wait for commands to complete',
        'M42 P' + str(onPin) + ' S255 ; turn extruder ' + str(extruder) + ' on']
    return '\n'.join(commands)


def stop_extrude(extruder, e0_pos, e1_pos):
    mid_pos = e0_pos + (e1_pos - e0_pos) / 2
    if extruder is 0:
        offPin = 16
    elif extruder is 1:
        offPin = 17
    commands = [
        'M400 ; wait for commands to complete',
        'M42 P' + str(offPin) + ' S0' 
        ' ; turn extruder ' + str(extruder) + ' off']
    return '\n'.join(commands)

def mid_position(e0_pos, e1_pos):
    mid_pos = e0_pos + (e1_pos - e0_pos) / 2
    commands = [
        'G1 E' + str(mid_pos) + ' F100' 
    ]
    return '\n'.join(commands)


def switch_extruder(extruder, e0_pos, e1_pos, X_offset):
    mid_pos = e0_pos + (e1_pos - e0_pos) / 2
    if extruder is 0:
        onPin = 16
        offPin = 17
        direction = -1
        target = e0_pos
    elif extruder is 1:
        onPin = 17
        offPin = 16
        direction = 1
        target = e1_pos

    commands = [
        'T0 ; ensure we keep T0 active to prevent changing pressure',
        'M400 ; wait for commands to complete',
        'G1 E' + str(mid_pos) + ' F' + str(e_rate) +
        ' ; move extruder to midpoint',
        'M400 ; wait for commands to complete',
        'G1 X' + str(direction * X_offset) + ' F' + str(x_rate) +
        ' ; move over by x offset',
        'M400 ; wait for commands to complete',
        'G1 E' + str(target) + ' F' + str(e_rate) + ' ; move extruder ' + str(extruder) + ' into position',
        ]

    return '\n'.join(commands)


def post_process(filename, e0_pos, e0_Zoffset,
                 e1_pos, e1_Zoffset,
                 X_offset, e_start):
    '''
    Read a gcode file and add M106 after E1.000 lines and
    M107, M126, M127 after each E peak.
    '''
    fName, fType = str.split(filename, '.')
    with open(filename, 'r') as f:
        with open(fName + '_processed.' + fType, 'w') as o:
            active_e = e_start
            for i, line in enumerate(f):
                if g_code(line) == 28:
                    o.write(home_z() + '\n')
                    o.write(home_e() + '\n')
                    o.write(home_xy() + '\n')
                    o.write(mid_position(e0_pos, e1_pos) + '\n')
                elif m_code(line) == 104 or m_code(line) == 109 or m_code(line) == 107 or m_code(line) == 190:
                    next
                else:
                    if e_value(line) is not None:
                        if e_value(line) == 0.0:
                            o.write(stop_extrude(active_e, e0_pos, e1_pos) + '\n')
                        elif e_value(line) == 1.0:
                            o.write(start_extrude(active_e, e0_pos, e1_pos) + '\n')
                        else:
                            o.write(remove_e(line) + '\n')
                    elif line.startswith('T') and t_value(line) is not None:
                        active_e = int(t_value(line))
                        o.write(switch_extruder(active_e, e0_pos, e1_pos, X_offset) + '\n')
                    elif z_value(line) is not None:
                        z_offset = e0_Zoffset if active_e == 0 else e1_Zoffset    
                        z_offset_comment = '; Extruder ' + str(active_e) + \
                                           ' Z Offset of ' + str(z_offset) + ' added.\n'
                        o.write(' '.join(['Z' + str(z_offset + z_value(i)) 
                                            if z_value(i.strip()) is not None else i.strip() 
                                            for i in line.split(' ')] +
                                            [z_offset_comment]))
                    else:
                        o.write(line)
        o.close()
    f.close()


filename = '/Users/karanhiremath/Documents/Programming/BioBots/bioprint/src/octoprint/util/biobot1/test_files/biobots_part_lattice (1).gcode'
# filename = '/Users/karanhiremath/Documents/Programming/BioBots/bioprint/src/octoprint/util/biobot1/test_files/1STCYLINDER.gcode'
e0_pos = 20
e0_Zoffset = 12.4

e1_pos = 0
e1_Zoffset = 4

X_offset = 49
e_start = 0

post_process(filename, e0_pos, e0_Zoffset, e1_pos, e1_Zoffset, X_offset, e_start)

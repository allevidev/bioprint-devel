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


import re, os

# from octoprint.settings import settings

e_rate = 1000.00
x_rate = 1800.00

e0_Xctr = 56
e0_Yctr = 90

e1_Xctr = 105
e1_Yctr = 90

x_pattern = 'X([+-]?\d+(?:\.\d+)?)'
y_pattern = 'Y([+-]?\d+(?:\.\d+)?)'
e_pattern = 'E([+-]?\d+(?:\.\d+)?)'
g_pattern = 'G([+-]?\d+(?:\.\d+)?)'
t_pattern = 'T(\d+\.\d+|\.\d+|\d+)'
z_pattern = 'Z([+-]?\d+(?:\.\d+)?)'
m_pattern = 'M([+-]?\d+(?:\.\d+)?)'


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


def g_value(line):
    '''
    Identify and returns the value of E on a line, for example
    returns 1.81780 for this line: "G1 X13.932 Y45.135 E1.81780"
    If no E found it return None
    '''
    if line.strip().startswith(';'):
        return None
    res = re.findall(g_pattern, line.upper())
    return None if res == [] else float(res[0])


def x_value(line):
    '''
    Identify and returns the value of X on a line, for example
    returns 1.81780 for this line "G1 X1.81780"
    If no X found it returns None
    '''
    if line.strip().startswith(';'):
        return None
    res = re.findall(x_pattern, line.upper())
    return None if res == [] else float(res[0])


def y_value(line):
    '''
    Identify and returns the value of Y on a line, for example
    returns 1.81780 for this line "G1 Y1.81780"
    If no Y found it returns None
    '''
    if line.strip().startswith(';'):
        return None
    res = re.findall(y_pattern, line.upper())
    return None if res == [] else float(res[0])


def remove_e(line):
    '''
    Remove the E value from a line, for example
    returns "G1 X13.932 Y45.135" on input "G1 X13.932 Y45.135 E1.81780"
    '''
    return ' '.join(filter(lambda x: x != '', [i.strip() if e_value(i) is None else ''.strip() for i in line.split(' ')]))


def g1_modify(line, x_offset, y_offset, z_offset):
    '''
    Remove the E value from a line, for example
    returns "G1 X13.932 Y45.135" on input "G1 X13.932 Y45.135 E1.81780"
    '''
    command = []
    for i in line.split(' '):
        if x_value(i) is not None:
            command.append('X' + str(x_value(i) + x_offset))
        elif y_value(i) is not None:
            command.append('Y' + str(y_value(i) + y_offset))
        elif z_value(i) is not None:
            command.append('Z' + str(z_value(i) + z_offset))
        elif e_value(i) is not None:
            next
        else:
            command.append(i)
    command.append('; X offset of ' + str(x_offset) + ' Y offset of ' + str(y_offset) + ' and Z offset of ' + str(z_offset) + ' added.')
    return ' '.join(command)


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


def m_value(line):
    if line.strip().startswith(';'):
        return None
    res = re.findall(m_pattern, line.upper())
    return None if res == [] else float(res[0])    

def start_extrude(extruder, e0_pos, e1_pos):
    mid = (e0_pos - e1_pos) / 2
    if extruder is 0:
        onPin = 16
        target = e0_pos
    elif extruder is 1:
        onPin = 17
        target = e1_pos
    commands = [
        'G1 E' + str(target) + ' ; Move extruder to E' + str(extruder) + ' position of ' + str(target),
        'M400 ; wait for commands to complete',
        'M42 P' + str(onPin) + ' S255 ; turn extruder ' + str(extruder) + ' on']
    return '\n'.join(commands)


def stop_extrude(extruder, e0_pos, e1_pos):
    mid = (e0_pos - e1_pos) / 2
    if extruder is 0:
        offPin = 16
    elif extruder is 1:
        offPin = 17
    commands = [
        'M400 ; wait for commands to complete',
        'M42 P' + str(offPin) + ' S0' 
        ' ; turn extruder ' + str(extruder) + ' off',
        'G1 E' + str(mid)]
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
        'G91',
        'G1 X' + str(direction * X_offset) + ' F' + str(x_rate) +
        ' ; move over by x offset',
        'G90',
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
                if m_value(line) == 190.0 or m_value(line) == 104.0 or m_value(line) == 109.0:
                    next
                else:
                    print i, g_value(line)
                    if g_value(line) is not None:
                        if g_value(line) == 28.0:
                            o.write('G1 Z45\n')
                            o.write('G1 E' + str(e1_pos) + '\n')
                            o.write('G28 X Y\n')
                            o.write('G21\n')
                            o.write('G1 X' + str(e0_Xctr) + ' Y' + str(e0_Yctr) + ' F1000\n')
                        else:
                            if x_value(line) is not None or y_value(line) is not None or z_value(line) is not None:    
                                if active_e == 0:
                                    o.write(g1_modify(line, e0_Xctr, e0_Yctr, e0_Zoffset) + '\n')
                                elif active_e == 1:
                                    o.write(g1_modify(line, e1_Xctr, e1_Yctr, e1_Zoffset) + '\n')
                            elif e_value(line) is not None:
                                if e_value(line) == 0.0:    
                                    o.write(stop_extrude(active_e, e0_pos, e1_pos) + '\n')
                                elif e_value(line) == 1.0:
                                    o.write(start_extrude(active_e, e0_pos, e1_pos) + '\n')
                                else:
                                    o.write(remove_e(line) + '\n')
                            else:
                                o.write(line)
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


# filename = '/Users/karanhiremath/Documents/Programming/BioBots/bioprint/src/octoprint/util/biobot1/test_files/biobots_part_lattice.gcode'
filename = os.path.dirname(os.path.realpath(__file__)) + '/test_files/PediatricBronchi.gcode'
e0_pos = 36.20
e0_Zoffset = 0

e1_pos = 10.2
e1_Zoffset = 0

X_offset = 49
e_start = 0


post_process(filename, e0_pos, e0_Zoffset, e1_pos, e1_Zoffset, X_offset, e_start)

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

e_rate = 100.00
x_rate = 1800.00

e_pattern = 'E(\d+\.\d+|\.\d+|\d+)'
t_pattern = 'T(\d+\.\d+|\.\d+|\d+)'


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


def next_e(e_vals, lines, ind):
    '''
    Returns the next e-value just after item ind.
    It skips lines without E values.
    It returns the value and its container line.
    '''
    for i in range(ind + 1, len(e_vals)):
        if e_vals[i] is not None:
            return e_vals[i], lines[i]
    return None, None


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


def next_t(t_vals, lines, ind):
    '''
    Returns the next e-value just after item ind.
    It skips lines without E values.
    It returns the value and its container line.
    '''
    for i in range(ind + 1, len(t_vals)):
        if t_vals[i] is not None:
            return t_vals[i], lines[i]
    return None, None


def z_value(line):
    '''
    Identify and returns the value of Z on a line, for example
    returns 1.81780 for this line "G1 Z1.81780"
    If no Z found it returns None
    '''


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


def switch_extruder(extruder, e1_pos, e2_pos, X_offset):
    mid_pos = e1_pos + (e2_pos - e1_pos) / 2
    if extruder is 0:
        onPin = 16
        offPin = 17
        direction = -1
        target = e1_pos
    elif extruder is 1:
        onPin = 17
        offPin = 16
        direction = 1
        target = e2_pos

    commands = [
        'T0',
        'M400',
        'M42 P' + offPin + 'S0',
        'G1 E' + mid_pos + ' F' + e_rate,
        'M400',
        'G1 X' + direction * X_offset + ' F' + x_rate,
        'M400',
        'G1 E' + target + ' F' + e_rate,
        'M400',
        'M42 P' + onPin + 'S255']

    return commands.join('\n')


def post_process(filename, e1_pos, e1_Zoffset, e2_pos, e2_Zoffset, X_offset):
    '''
    Read a gcode file and add M106 after E1.000 lines and
    M107, M126, M127 after each E peak.
    '''
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            print i, line
    # lines = f.read().split('\n')
    # f.close()
    # if lines[-1] == '':
    #     lines.pop()
    # t_vals = [t_value(i) for i in lines]
    # result = []
    # pt = None

    # #checking for T0 and T1 lines
    # for j, line in enumerate(lines):
    #     result.append(line)
    #     t = t_vals[j]
    #     result.append(switch_extruder(t))

    #     pt = t if t is not None else pt

    # f = open(filename + '', 'w')
    # f.write('\n'.join(result))
    # f.close()


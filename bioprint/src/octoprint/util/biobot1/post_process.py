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
import time
import datetime

# from octoprint.settings import settings

e_rate = 1000.00
x_rate = 2000.00

wellPlatePositions = {
    1: {
        "A": {
            0: {
                0: {
                    "X": 56,
                    "Y": 90
                },
                1: {
                    "X": 104.33,
                    "Y": 90
                }
            }
        }
    },
    24: {
        "A": {
            0: {
                0: {
                    "X": 11.20,
                    "Y": 63.00
                },
                1: {
                    "X": 59.53,
                    "Y": 63.00
                }
            },
            1: {
                0: {
                    "X": 30.5,
                    "Y": 63.00
                },
                1: {
                    "X": 78.83,
                    "Y": 63.00
                }
            },
            2: {
                0: {
                    "X": 49.8,
                    "Y": 63.00
                },
                1: {
                    "X": 98.13,
                    "Y": 63.00
                }
            },
            3: {
                0: {
                    "X": 69.1,
                    "Y": 63.00
                },
                1: {
                    "X": 117.43,
                    "Y": 63.00
                }
            },
            4: {
                0: {
                    "X": 88.4,
                    "Y": 63.00
                },
                1: {
                    "X": 136.73,
                    "Y": 63.00
                }
            },
            5: {
                0: {
                    "X": 107.7,
                    "Y": 63.00
                },
                1: {
                    "X": None,
                    "Y": None
                }
            },
        },
        "B": {
            0: {
                0: {
                    "X": 11.20,
                    "Y": 82.3
                },
                1: {
                    "X": 59.53,
                    "Y": 82.3
                }
            },
            1: {
                0: {
                    "X": 30.5,
                    "Y": 82.3
                },
                1: {
                    "X": 78.83,
                    "Y": 82.3
                }
            },
            2: {
                0: {
                    "X": 49.8,
                    "Y": 82.3
                },
                1: {
                    "X": 98.13,
                    "Y": 82.3
                }
            },
            3: {
                0: {
                    "X": 69.1,
                    "Y": 82.3
                },
                1: {
                    "X": 117.43,
                    "Y": 82.3
                }
            },
            4: {
                0: {
                    "X": 88.4,
                    "Y": 82.3
                },
                1: {
                    "X": 136.73,
                    "Y": 82.3
                }
            },
            5: {
                0: {
                    "X": 107.7,
                    "Y": 82.3
                },
                1: {
                    "X": None,
                    "Y": None
                }
            },
        },
        "C": {
            0: {
                0: {
                    "X": 11.20,
                    "Y": 101.6
                },
                1: {
                    "X": 59.53,
                    "Y": 101.6
                }
            },
            1: {
                0: {
                    "X": 30.5,
                    "Y": 101.6
                },
                1: {
                    "X": 78.83,
                    "Y": 101.6
                }
            },
            2: {
                0: {
                    "X": 49.8,
                    "Y": 101.6
                },
                1: {
                    "X": 98.13,
                    "Y": 101.6
                }
            },
            3: {
                0: {
                    "X": 69.1,
                    "Y": 101.6
                },
                1: {
                    "X": 117.43,
                    "Y": 101.6
                }
            },
            4: {
                0: {
                    "X": 88.4,
                    "Y": 101.6
                },
                1: {
                    "X": 136.73,
                    "Y": 101.6
                }
            },
            5: {
                0: {
                    "X": 107.7,
                    "Y": 101.6
                },
                1: {
                    "X": None,
                    "Y": None
                }
            },
        },
    }
}

e0_Xctr = 56
e0_Yctr = 90

e1_Xctr = 104.33
e1_Yctr = 90

mid = 24

x_pattern = 'X([+-]?\d+(?:\.\d+)?)'
y_pattern = 'Y([+-]?\d+(?:\.\d+)?)'
e_pattern = 'E([+-]?\d+(?:\.\d+)?)'
g_pattern = 'G([+-]?\d+(?:\.\d+)?)'
t_pattern = 'T(\d+\.\d+|\.\d+|\d+)'
z_pattern = 'Z([+-]?\d+(?:\.\d+)?)'
m_pattern = 'M([+-]?\d+(?:\.\d+)?)'

e0_pos = 24
e1_pos = 24


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


def g1_modify(line, x_offset, y_offset):
    '''
    Remove the E value from a line, for example
    returns "G1 X13.932 Y45.135" on input "G1 X13.932 Y45.135 E1.81780"
    '''
    command = []
    if x_offset is not None and y_offset is not None:
        for i in line.split(' '):
            if x_value(i) is not None:
                command.append('X' + str(x_value(i) + x_offset))
            elif y_value(i) is not None:
                command.append('Y' + str(y_value(i) + y_offset))
            elif z_value(i) is not None:
                command.append('Z' + str(z_value(i)))
            elif e_value(i) is not None:
                next
            else:
                command.append(i)
   # command.append('; X offset of ' + str(x_offset) + ' Y offset of ' + str(y_offset) + ' and Z offset of ' + str(z_offset) + ' added.')
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
    if extruder is 0:
        onPin = 16
        target = e0_pos
    elif extruder is 1:
        onPin = 17
        target = e1_pos
    commands = [
        'G1 E' + str(target) + ' ; Move extruder to E' + str(extruder) + ' position of ' + str(target),
        'M400 ; wait for commands to complete',
        'M42 P' + str(onPin) + ' S255 ; turn extruder ' + str(extruder) + ' on',
        'M400 ; wait for commands to complete']
    return '\n'.join(commands)


def stop_extrude(extruder, e0_pos, e1_pos):
    if extruder is 0:
        offPin = 16
    elif extruder is 1:
        offPin = 17
    commands = [
        'M400 ; wait for commands to complete',
        'M42 P' + str(offPin) + ' S0' 
        ' ; turn extruder ' + str(extruder) + ' off',
        'M400',
        'G1 E' + str(mid) + ' F1000 ; Move extruder to mid point']
    return '\n'.join(commands)


def switch_extruder(extruder, e0_pos, e1_pos):
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
        'G1 E' + str(mid) + ' F' + str(e_rate) +
        ' ; move extruder to midpoint',
        'M400 ; wait for commands to complete'
        ]

    return '\n'.join(commands)

def crosslink(x, y, cl_duration, cl_intensity):
    commands = [
        'G1 E' + str(mid) + ' F' + str(e_rate),
        'G1 X' + str(x) + ' Y' + str(y),
        'M400',
        'M42 P4 S' + str(cl_intensity) + ' ; CROSSLINK HERE',
        'G4 P' + str(cl_duration),
        'M42 P4 S0'
    ]

    return '\n'.join(commands)


def post_process(payload, positions, wellPlate, cl_params):
    '''
    Read a gcode file and add M106 after E1.000 lines and
    M107, M126, M127 after each E peak.
    '''
    rows = sorted(wellPlatePositions[wellPlate].keys())

    e0_pos = positions["tool0"]
    e1_pos = positions["tool1"]
    filename = str(payload["file"])

    fName = '.'.join(str.split(filename, '.')[0:-1])
    fType = str.split(filename, '.')[-1]
    timeformat = '%Y-%m-%d-%H-%M-%S'
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(timeformat)
    outputFile = fName + '_processed_'+ timestamp + '.' + fType
    
    with open(filename, 'r') as f:
        if f.readline() is "; POST PROCESSED":
            f.close()
            return payload

    with open(outputFile, 'w') as o:
        o.write('; POST PROCESSED\n')
        active_e = 0
        last_e = 0
        extruding = False
        for r in rows:
            columns = sorted(wellPlatePositions[wellPlate][r].keys())
            for c in columns:
                layer = 0
                e0_Xctr = wellPlatePositions[wellPlate][r][c][0]["X"]
                e0_Yctr = wellPlatePositions[wellPlate][r][c][0]["Y"]

                e1_Xctr = wellPlatePositions[wellPlate][r][c][1]["X"]
                e1_Yctr = wellPlatePositions[wellPlate][r][c][1]["Y"]
                with open(filename, 'r') as f:
                    for i, line in enumerate(f):
                        if z_value(line) is not None:
                            layer += 1
                            if cl_params["cl_layers"] != 0:
                                if layer % cl_params["cl_layers"] == 0 and layer != 0:
                                    o.write(crosslink(e1_Xctr, e1_Yctr, cl_params["cl_duration"], cl_params["cl_intensity"]) + '\n')
                        if m_value(line) == 190.0 or m_value(line) == 104.0 or m_value(line) == 109.0:
                            next
                        else:
                            if g_value(line) is not None:
                                if g_value(line) == 28.0:
                                    o.write('G1 Z45\n')
                                    o.write('G1 E' + str(e1_pos) + '\n')
                                    o.write('G28 X Y\n')
                                    o.write('G21\n')
                                    o.write('G1 X' + str(e0_Xctr) + ' Y' + str(e0_Yctr) + ' F1000\n')
                                elif g_value(line) == 1 or e_value(line) is not None:
                                    if e_value(line) is not None:
                                        d_e = e_value(line) - last_e
                                        if d_e > 0:
                                            if not extruding:
                                                o.write(start_extrude(active_e, e0_pos, e1_pos) + '\n')
                                                extruding = not extruding
                                            if active_e == 0:
                                                o.write(g1_modify(line, e0_Xctr, e0_Yctr) + '\n')
                                            elif active_e == 1:
                                                o.write(g1_modify(line, e1_Xctr, e1_Yctr) + '\n')
                                            last_e = e_value(line)
                                            next
                                        elif d_e < 0:
                                            if active_e == 0:
                                                o.write(g1_modify(line, e0_Xctr, e0_Yctr) + '\n')
                                            elif active_e == 1:
                                                o.write(g1_modify(line, e1_Xctr, e1_Yctr) + '\n')
                                            if extruding:
                                                o.write(stop_extrude(active_e, e0_pos, e1_pos) + '\n')   
                                                extruding = not extruding
                                            last_e = e_value(line)
                                            next
                                    elif g_value(line) == 1:
                                        if active_e == 0:
                                            o.write(g1_modify(line, e0_Xctr, e0_Yctr) + '\n')
                                        elif active_e == 1:
                                            o.write(g1_modify(line, e1_Xctr, e1_Yctr) + '\n')
                                else:
                                    o.write(line)
                            elif line.startswith('T') and t_value(line) is not None:
                                active_e = int(t_value(line))
                                o.write(switch_extruder(active_e, e0_pos, e1_pos) + '\n')
                            elif m_value(line) == 106.0:
                                o.write(start_extrude(active_e, e0_pos, e1_pos) + '\n')
                            elif m_value(line) == 107.0:
                                o.write(stop_extrude(active_e, e0_pos, e1_pos) + '\n')
                            else:
                                o.write(line)
                if cl_params["cl_end"]:
                    o.write(crosslink(e1_Xctr, e1_Yctr, cl_params["cl_end_duration"], cl_params["cl_end_intensity"])+ '\n')
                f.close()
    o.close()
    
    return {
        "file": outputFile,
        "filename": payload["filename"],
        "origin": payload["origin"]
    }

test_payload = {
    'origin': 'local', 
    'file': '/Users/karanhiremath/Downloads/PediatricBronchi.gcode',
    'filename': u'/Users/karanhiremath/Downloads/PediatricBronchi.gcode'
}

test_positions = {
    "tool0": 24,
    "tool1": 24
}

cl_params = {
    "cl_layers": 3,
    "cl_duration": 200,
    "cl_intensity": 10,
    "cl_end": True,
    "cl_end_duration": 2000
}

# post_process(test_payload, test_positions, 1, cl_params)

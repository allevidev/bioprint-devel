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


import boto3
import datetime
import time
import re
import requests
import json
from flask.ext.login import current_user

analytics = True
# biobots_url = 'http://data.biobots.io/'
biobots_url = 'http://data.biobots.io'

def connected_to_biobots(url='http://data.biobots.io/', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

# from bioprint.settings import settings

e_rate = 1000.00
x_rate = 2000.00

x_travel = 48.33

wellPlatePositions_old = {
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

mid = 22

x_pattern = 'X([+-]?\d+(?:\.\d+)?)'
y_pattern = 'Y([+-]?\d+(?:\.\d+)?)'
e_pattern = 'E([+-]?\d+(?:\.\d+)?)'
g_pattern = 'G([+-]?\d+(?:\.\d+)?)'
t_pattern = 'T(\d+\.\d+|\.\d+|\d+)'
z_pattern = 'Z([+-]?\d+(?:\.\d+)?)'
m_pattern = 'M([+-]?\d+(?:\.\d+)?)'
post_process_pattern = 'POST PROCESSED'

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


def g1_modify(line, active_e, x_ctr, y_ctr):
    '''
    Remove the E value from a line, for example
    returns "G1 X13.932 Y45.135" on input "G1 X13.932 Y45.135 E1.81780"
    '''
    command = []
    for i in line.split(' '):
        if x_value(i) is not None:
            command.append('X' + str(x_value(i) + x_ctr[active_e]))
        elif y_value(i) is not None:
            print y_value(i), y_ctr[active_e], y_value(i) + y_ctr[active_e]
            command.append('Y' + str(y_value(i) + y_ctr[active_e]))
        elif z_value(i) is not None:
            next
            # command.append('Z' + str(z_value(i)))
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

def post_processed_check(line):
    if line.strip().startswith(';'):
        res = re.findall(post_process_pattern, line.upper())
        return False if res == [] else True


def start_extrude(active_e, layer_z):
    onPin = 16
    commands = [
        'G1 Z' + str(layer_z[active_e]),
        'M42 P' + str(onPin) + ' S255 ; turn extruder ' + str(active_e) + ' on']
    return '\n'.join(commands)


def stop_extrude(active_e):
    offPin = 16
    commands = [
        'M42 P' + str(offPin) + ' S0' 
        ' ; turn extruder ' + str(active_e) + ' off']
    return '\n'.join(commands)


def switch_extruder(active_e):
    
    commands = [
        'C1 S0 ; uncap the extruder',
        'T' + str(active_e) + ' ; switch the extruder',
        'C1 S255 ; cap the extruder'
        ]

    return '\n'.join(commands)

def crosslink(cl_x, cl_y, target_x, target_y, z, wellplate, cl_duration, cl_intensity):
    cl_z = {
        1: 0,
        6: 10,
        12: 10,
        24: 10,
        96: 10
    }
    commands = [
        'G1 Z50 F1000',
        'G1 E' + str(mid),
        'G1 X' + str(cl_x) + ' Y' + str(cl_y),
        'G1 Z' + str(cl_z[wellplate] + z[1]),
        'G1 E' + str(0),
        'M400',
        'M42 P4 S' + str(cl_intensity) + ' ; CROSSLINK HERE',
        'G4 P' + str(cl_duration),
        'M42 P4 S0',
        'G1 Z50 F1000',
        'G1 E' + str(mid),
        'G1 X' + str(target_x) + ' Y' + str(target_y),
        'G1 Z' + str(z[1])
    ]

    return '\n'.join(commands)

def calculate_wellplate_positions(positions):
    petri = {
        "A": {
            0: {
                0: {
                    "X": float(positions["tool0"]["X"]),
                    "Y": float(positions["tool0"]["Y"]),
                    "Z": float(positions["tool0"]["Z"])
                },
                1: {
                    "X": float(positions["tool1"]["X"]),
                    "Y": float(positions["tool1"]["Y"]),
                    "Z": float(positions["tool1"]["Z"])
                }
            }
        }
    }
    row_6 = ["A", "B"]
    column_6 = 3
    out_6 = {}
    for i in xrange(len(row_6)):
        row_out = {}
        for j in xrange(column_6):
            row_out[j] = {
                0: {
                    "X": float(positions["tool0"]["X"]) + j * 39.12,
                    "Y": float(positions["tool0"]["Y"]) + i * 39.12,
                    "Z": float(positions["tool0"]["Z"])
                },
                1: {
                    "X": float(positions["tool1"]["X"]) + j * 39.12,
                    "Y": float(positions["tool1"]["Y"]) + i * 39.12,
                    "Z": float(positions["tool1"]["Z"])
                }
            }
        out_6[row_6[i]] = row_out
    row_12 = ["A", "B", "C"]
    column_12 = 4
    out_12 = {}
    for i in xrange(len(row_12)):
        row_out = {}
        for j in xrange(column_12):
            row_out[j] = {
                0: {
                    "X": float(positions["tool0"]["X"]) + j * 26.01,
                    "Y": float(positions["tool0"]["Y"]) + i * 26.01,
                    "Z": float(positions["tool0"]["Z"])
                },
                1: {
                    "X": float(positions["tool1"]["X"]) + j * 26.01,
                    "Y": float(positions["tool1"]["Y"]) + i * 26.01,
                    "Z": float(positions["tool1"]["Z"])
                }
            }
        out_12[row_12[i]] = row_out
    row_24 = ["A", "B", "C", "D"]
    column_24 = 6
    out_24 = {}
    for i in xrange(len(row_24)):
        row_out = {}
        for j in xrange(column_24):
            row_out[j] = {
                0: {
                    "X": float(positions["tool0"]["X"]) + j * 19.3,
                    "Y": float(positions["tool0"]["Y"]) + i * 19.3,
                    "Z": float(positions["tool0"]["Z"])
                },
                1: {
                    "X": float(positions["tool1"]["X"]) + j * 19.3,
                    "Y": float(positions["tool1"]["Y"]) + i * 19.3,
                    "Z": float(positions["tool1"]["Z"])
                }
            }
        out_24[row_24[i]] = row_out
    row_96 = ["A", "B", "C", "D", "E", "F"]
    column_96 = 12
    out_96 = {}
    for i in xrange(len(row_96)):
        row_out = {}
        for j in xrange(column_96):
            row_out[j] = {
                0: {
                    "X": float(positions["tool0"]["X"]) + j * 9,
                    "Y": float(positions["tool0"]["Y"]) + i * 9,
                    "Z": float(positions["tool0"]["Z"])
                },
                1: {
                    "X": float(positions["tool1"]["X"]) + j * 9,
                    "Y": float(positions["tool1"]["Y"]) + i * 9,
                    "Z": float(positions["tool1"]["Z"])
                }
            }
        out_96[row_96[i]] = row_out

    return {
        1: petri,
        6: out_6,
        12: out_12,
        24: out_24,
        96: out_96
    }

def end_print():
    x_end_pos = 0
    y_end_pos = 0
    e_end_pos = 0
    z_end_pos = 50
    commands = [
        'M42 P16 S0',
        'M42 P17 S0',
        'G1 Z' + str(z_end_pos) + ' F1000',
        'G1 E' + str(e_end_pos) + ' F1000',
        'G1 X' + str(x_end_pos) + ' Y' + str(y_end_pos) + ' F1000'
    ]
    return '\n'.join(commands)


def can_post_process_local(payload, positions, wellPlate, cl_params, tempData):
    processed = False

    with open(payload["file"], 'r') as f:
        for i, line in enumerate(f):
            if post_processed_check(line) == True:
                processed = True
                return payload

    filename = str(payload["file"])

    fName = '.'.join(str.split(filename, '.')[0:-1])
    fType = str.split(filename, '.')[-1]
    timeformat = '%Y-%m-%d-%H-%M-%S'
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(timeformat)
    inputFileName = '.'.join(str.split(str.split(filename, '/')[-1], '.')[0:-1]) + '.' + fType
    
    if processed == True:
        outputFileName = inputFileName + timestamp + '.' + fType
        outputFile = fName + timestamp + '.' + fType    
    elif processed == False:
        outputFileName = inputFileName + '_processed_' + timestamp + '.' + fType
        outputFile = fName + '_processed_' + timestamp + '.' + fType

    if processed == False:
        with open(outputFile, 'w') as o:
            o.write('; POST PROCESSED\n')
            active_e = 0
            last_e = 0
            extruding = False
            x_ctr, y_ctr = map(lambda x: positions[x]['X'], positions), map(lambda x: positions[x]['Y'], positions)
            x_pos, x_pos_old = map(lambda x: positions[x]['X'], positions), map(lambda x: positions[x]['X'], positions)
            y_pos, y_pos_old = map(lambda x: positions[x]['Y'], positions), map(lambda x: positions[x]['Y'], positions)

            layer_z = map(lambda x: positions[x]['Z'], positions)
            layer = 0

            with open(filename, 'r') as f:
                for i, line in enumerate(f):
                    if z_value(line) is not None:
                        o.write(stop_extrude(active_e) + '\n')
                        last_e = 0
                        extruding = False
                        layer_z = map(lambda x: positions[x]['Z'] + z_value(line), positions)
                        layer += 1
                        next
                    if m_value(line) == 190.0 or m_value(line) == 104.0 or m_value(line) == 109.0:
                        next
                    else:
                        if g_value(line) is not None:
                            if g_value(line) == 28.0:
                                next
                            elif g_value(line) == 1 or e_value(line) is not None:
                                if g_value(line) == 1:
                                    if x_value(line) is not None:
                                        x_pos_old[active_e] = x_pos[active_e]
                                        x_pos[active_e] = x_value(line) + x_ctr[active_e]
                                    if y_value(line) is not None:
                                        y_pos_old[active_e] = y_pos[active_e]
                                        y_pos[active_e] = y_value(line) + y_ctr[active_e]

                                if e_value(line) is not None:
                                    d_e = e_value(line) - last_e
                                    if d_e > 0:
                                        o.write('G1 X' + str(x_pos_old[active_e]) + ' Y' + str(y_pos_old[active_e]) + '\n')
                                        if not extruding:
                                            o.write(start_extrude(active_e, layer_z) + '\n')
                                            extruding = True
                                        o.write(g1_modify(line, active_e, x_ctr, y_ctr) + '\n')
                                        last_e = e_value(line)
                                        next
                                    elif d_e < 0:
                                        o.write(g1_modify(line, active_e, x_ctr, y_ctr))
                                        if extruding:
                                            o.write(stop_extrude(active_e) + '\n')
                                            extruding = False
                                        last_e = e_value(line)
                                        next
                                elif g_value(line) == 1:
                                    if e_value(line) is None and last_e > 0:
                                        if extruding:
                                            o.write(stop_extrude(active_e) + '\n')
                                            extruding = False
                                        last_e = 0
                                        o.write(g1_modify(line, active_e, x_ctr, y_ctr) + '\n')
                                        next
                                    else:
                                        o.write(g1_modify(line, active_e, x_ctr, y_ctr) + '\n')
                            else:
                                o.write(line)
                        elif line.startswith('T') and t_value(line) is not None:
                            active_e = int(t_value(line))
                            o.write(switch_extruder(active_e) + '\n')
                        elif m_value(line) == 106.0:
                            o.write(start_extrude(active_e, layer_z) + '\n')
                        elif m_value(line) == 107.0:
                            o.write(stop_extrude(active_e, layer_z) + '\n')
                        else:
                            o.write(line)
                f.close()
            o.write(end_print() + '\n')
        o.close

    if processed == True:
        return payload
    else:
        return {
            "file": outputFile,
            "filename": payload["filename"],
            "origin": payload["origin"]
        }

def can_post_process_api(apiPrint):
    return apiPrint

test_payload = {
    'origin': 'local', 
    'file': 'test_files/test_lattice.gcode',
    'filename': u'test_files/test_lattice.gcode'
}

test_positions = {
    "tool0": {
        "X": 11.20,
        "Y": 63,
        "Z": 16
    },
    "tool1": {
        "X": 59.53,
        "Y": 63,
        "Z": 13
    },
}

cl_params = {
    "cl_layers_enabled": True,
    "cl_layers": 1,
    "cl_duration": 2000,
    "cl_intensity": 25,
    "cl_end": True,
    "cl_end_duration": 2000,
    "cl_end_intensity": 100
}

payload_6 = {
    'origin': 'local',
    'file': 'test_files/bb2.gcode',
    'filename': u'test_files/bb2.gcode'
}

positions_6 = {
            "A": {
                "X": 107,
                "Y": 57,
                "Z": 0
                },
            "B": {
                "X": 107,
                "Y": 57,
                "Z": 0
                },
            "C": {
                "X": 107,
                "Y": 57,
                "Z": 0
                },
            "D": {
                "X": 107,
                "Y": 57,
                "Z": 0
                },
            "E": {
                "X": 107,
                "Y": 57,
                "Z": 0
                },
            "F": {
                "X": 107,
                "Y": 57,
                "Z": 0
                }
            }

# post_process(test_payload, test_positions, 1, cl_params, None)
#can_post_process_local(payload_6, positions_6, 1, cl_params, None)
# print calculate_wellplate_positions(test_positions, 24)


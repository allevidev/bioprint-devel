; POST PROCESSED
G1 Z50
G1 E22
G21
G1 X11.2 Y63.0 F1000
T0 ; ensure we keep T0 active to prevent changing pressure
M400 ; wait for commands to complete
G1 E22 F1000.0 ; move extruder to midpoint
M400 ; wait for commands to complete
G1 Z50
E0
M400 ; wait for commands to complete
M42 P16 S0 ; turn extruder 0 off
M400
G90
G1
G1 X-3.8 Y48.0
G1 X-3.8 Y48.0
G1 E46 ; Move extruder to E0 position of 46
G1 Z16.2
M400 ; wait for commands to complete
M42 P16 S255 ; turn extruder 0 on
M400 ; wait for commands to complete
G1 X1.2 Y53.0
G1 X1.2 Y53.0
G1 X6.2 Y48.0
G1 X6.2 Y48.0
G1 X11.2 Y53.0
G1 X11.2 Y53.0
G1 X16.2 Y48.0
G1 X16.2 Y48.0
G1 X21.2 Y53.0
G1 X21.2 Y53.0
G1 X26.2 Y48.0
E0
M400 ; wait for commands to complete
M42 P16 S0 ; turn extruder 0 off
M400
G90
G1 X26.2 Y53.0
G1 X26.2 Y53.0
G1 E46 ; Move extruder to E0 position of 46
G1 Z16.2
M400 ; wait for commands to complete
M42 P16 S255 ; turn extruder 0 on
M400 ; wait for commands to complete
G1 X21.2 Y58.0
G1 X21.2 Y58.0
G1 X16.2 Y53.0
G1 X16.2 Y53.0
G1 X11.2 Y58.0
G1 X11.2 Y58.0
G1 X6.2 Y53.0
G1 X6.2 Y53.0
G1 X1.2 Y58.0
G1 X1.2 Y58.0
G1 X-3.8 Y53.0
E0
E0
M400 ; wait for commands to complete
M42 P16 S0 ; turn extruder 0 off
M400
G90
G1 X-3.8 Y58.0 

G1 X-3.8 Y58.0
G1 E46 ; Move extruder to E0 position of 46
G1 Z16.2
M400 ; wait for commands to complete
M42 P16 S255 ; turn extruder 0 on
M400 ; wait for commands to complete
G1 X1.2 Y63.0
G1 X1.2 Y63.0
G1 X6.2 Y58.0
G1 X6.2 Y58.0
G1 X11.2 Y63.0
G1 X11.2 Y63.0
G1 X16.2 Y58.0
G1 X16.2 Y58.0
G1 X21.2 Y63.0
G1 X21.2 Y63.0
G1 X26.2 Y58.0
E0
E0 
M400 ; wait for commands to complete
M42 P16 S0 ; turn extruder 0 off
M400
G90
G1 X26.2 Y63.0 

G1 X26.2 Y63.0
G1 E46 ; Move extruder to E0 position of 46
G1 Z16.2
M400 ; wait for commands to complete
M42 P16 S255 ; turn extruder 0 on
M400 ; wait for commands to complete
G1 X21.2 Y68.0
G1 X21.2 Y68.0
G1 X16.2 Y63.0
G1 X16.2 Y63.0
G1 X11.2 Y68.0
G1 X11.2 Y68.0
G1 X6.2 Y63.0
G1 X6.2 Y63.0
G1 X1.2 Y68.0
G1 X1.2 Y68.0
G1 X-3.8 Y63.0
E0
E0
M400 ; wait for commands to complete
M42 P16 S0 ; turn extruder 0 off
M400
G90
G1 X-3.8 Y68.0 

G1 X-3.8 Y68.0
G1 E46 ; Move extruder to E0 position of 46
G1 Z16.2
M400 ; wait for commands to complete
M42 P16 S255 ; turn extruder 0 on
M400 ; wait for commands to complete
G1 X1.2 Y73.0
G1 X1.2 Y73.0
G1 X6.2 Y68.0
G1 X6.2 Y68.0
G1 X11.2 Y73.0
G1 X11.2 Y73.0
G1 X16.2 Y68.0
G1 X16.2 Y68.0
G1 X21.2 Y73.0
G1 X21.2 Y73.0
G1 X26.2 Y68.0
E0
M400 ; wait for commands to complete
M42 P16 S0 ; turn extruder 0 off
M400
G90
G1 X26.2 Y73.0
G1 X26.2 Y73.0
G1 E46 ; Move extruder to E0 position of 46
G1 Z16.2
M400 ; wait for commands to complete
M42 P16 S255 ; turn extruder 0 on
M400 ; wait for commands to complete
G1 X21.2 Y78.0
G1 X21.2 Y78.0
G1 X16.2 Y73.0
G1 X16.2 Y73.0
G1 X11.2 Y78.0
G1 X11.2 Y78.0
G1 X6.2 Y73.0
G1 X6.2 Y73.0
G1 X1.2 Y78.0
G1 X1.2 Y78.0
G1 X-3.8 Y73.0
E0

T0 ; ensure we keep T0 active to prevent changing pressure
M400 ; wait for commands to complete
G1 E22 F1000.0 ; move extruder to midpoint
M400 ; wait for commands to complete
G1 Z50
M400 ; wait for commands to complete
M42 P17 S0 ; turn extruder 1 off
M400
G90
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.2
G1 E0
M400
M42 P4 S25 ; CROSSLINK HERE
G4 P2000
M42 P4 S0
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.2
G1
G1 X44.53 Y48.0 

G1 X44.53 Y48.0
G1 E0 ; Move extruder to E1 position of 0
G1 Z13.4
M400 ; wait for commands to complete
M42 P17 S255 ; turn extruder 1 on
M400 ; wait for commands to complete
G1 X44.53 Y78.0
E0
E0
M400 ; wait for commands to complete
M42 P17 S0 ; turn extruder 1 off
M400
G90
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.4
G1 E0
M400
M42 P4 S25 ; CROSSLINK HERE
G4 P2000
M42 P4 S0
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.4
G1
G1 X49.53 Y48.0
G1 X49.53 Y48.0
G1 E0 ; Move extruder to E1 position of 0
G1 Z13.4
M400 ; wait for commands to complete
M42 P17 S255 ; turn extruder 1 on
M400 ; wait for commands to complete
G1 X49.53 Y78.0
E0
E0
M400 ; wait for commands to complete
M42 P17 S0 ; turn extruder 1 off
M400
G90
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.4
G1 E0
M400
M42 P4 S25 ; CROSSLINK HERE
G4 P2000
M42 P4 S0
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.4
G1
G1 X54.53 Y48.0
G1 X54.53 Y48.0
G1 E0 ; Move extruder to E1 position of 0
G1 Z13.4
M400 ; wait for commands to complete
M42 P17 S255 ; turn extruder 1 on
M400 ; wait for commands to complete
G1 X54.53 Y78.0
E0
E0
M400 ; wait for commands to complete
M42 P17 S0 ; turn extruder 1 off
M400
G90
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.4
G1 E0
M400
M42 P4 S25 ; CROSSLINK HERE
G4 P2000
M42 P4 S0
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.4
G1
G1 X59.53 Y48.0
G1 X59.53 Y48.0
G1 E0 ; Move extruder to E1 position of 0
G1 Z13.4
M400 ; wait for commands to complete
M42 P17 S255 ; turn extruder 1 on
M400 ; wait for commands to complete
G1 X59.53 Y78.0
E0
E0
M400 ; wait for commands to complete
M42 P17 S0 ; turn extruder 1 off
M400
G90
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.4
G1 E0
M400
M42 P4 S25 ; CROSSLINK HERE
G4 P2000
M42 P4 S0
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.4
G1
G1 X64.53 Y48.0
G1 X64.53 Y48.0
G1 E0 ; Move extruder to E1 position of 0
G1 Z13.4
M400 ; wait for commands to complete
M42 P17 S255 ; turn extruder 1 on
M400 ; wait for commands to complete
G1 X64.53 Y78.0
E0
E0
M400 ; wait for commands to complete
M42 P17 S0 ; turn extruder 1 off
M400
G90
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.4
G1 E0
M400
M42 P4 S25 ; CROSSLINK HERE
G4 P2000
M42 P4 S0
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.4
G1
G1 X69.53 Y48.0
G1 X69.53 Y48.0
G1 E0 ; Move extruder to E1 position of 0
G1 Z13.4
M400 ; wait for commands to complete
M42 P17 S255 ; turn extruder 1 on
M400 ; wait for commands to complete
G1 X69.53 Y78.0
E0
E0
M400 ; wait for commands to complete
M42 P17 S0 ; turn extruder 1 off
M400
G90
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.4
G1 E0
M400
M42 P4 S25 ; CROSSLINK HERE
G4 P2000
M42 P4 S0
G1 Z50 F1000
G1 E22
G1 X59.53 Y63.0
G1 Z13.4
G1
G1 X74.53 Y48.0
G1 X74.53 Y48.0
G1 E0 ; Move extruder to E1 position of 0
G1 Z13.4
M400 ; wait for commands to complete
M42 P17 S255 ; turn extruder 1 on
M400 ; wait for commands to complete
G1 X74.53 Y78.0
E0




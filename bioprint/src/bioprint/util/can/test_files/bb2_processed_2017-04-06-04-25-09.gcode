; POST PROCESSED
C1 S0 ; uncap the extruder
G1 Z10 ; make sure we don't destroy the tip
T0 ; switch the extruder
C1 S255 ; cap the extruder
G1 Z0 ; go back
E0
M42 P16 S0 ; turn extruder 0 off
G1 ; here5
G1 X92.0 Y42.0 ; here5
G1 X92.0 Y42.0 ; here1
G1 Z0.2
M42 P16 S255 ; turn extruder 0 on
G1 X97.0 Y47.0 ; here2
G1 X102.0 Y42.0 ; here2
G1 X107.0 Y47.0 ; here2
G1 X112.0 Y42.0 ; here2
G1 X117.0 Y47.0 ; here2
G1 X122.0 Y42.0 ; here2
E0
M42 P16 S0 ; turn extruder 0 off
G1 X122.0 Y47.0 ; here4
G1 X122.0 Y47.0 ; here1
G1 Z0.2
M42 P16 S255 ; turn extruder 0 on
G1 X117.0 Y52.0 ; here2
G1 X112.0 Y47.0 ; here2
G1 X107.0 Y52.0 ; here2
G1 X102.0 Y47.0 ; here2
G1 X97.0 Y52.0 ; here2
G1 X92.0 Y47.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 0 off
G1 X92.0 Y52.0 
 ; here4
G1 X92.0 Y52.0 ; here1
G1 Z0.2
M42 P16 S255 ; turn extruder 0 on
G1 X97.0 Y57.0 ; here2
G1 X102.0 Y52.0 ; here2
G1 X107.0 Y57.0 ; here2
G1 X112.0 Y52.0 ; here2
G1 X117.0 Y57.0 ; here2
G1 X122.0 Y52.0 ; here2
E0
E0 
M42 P16 S0 ; turn extruder 0 off
G1 X122.0 Y57.0 
 ; here4
G1 X122.0 Y57.0 ; here1
G1 Z0.2
M42 P16 S255 ; turn extruder 0 on
G1 X117.0 Y62.0 ; here2
G1 X112.0 Y57.0 ; here2
G1 X107.0 Y62.0 ; here2
G1 X102.0 Y57.0 ; here2
G1 X97.0 Y62.0 ; here2
G1 X92.0 Y57.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 0 off
G1 X92.0 Y62.0 
 ; here4
G1 X92.0 Y62.0 ; here1
G1 Z0.2
M42 P16 S255 ; turn extruder 0 on
G1 X97.0 Y67.0 ; here2
G1 X102.0 Y62.0 ; here2
G1 X107.0 Y67.0 ; here2
G1 X112.0 Y62.0 ; here2
G1 X117.0 Y67.0 ; here2
G1 X122.0 Y62.0 ; here2
E0
M42 P16 S0 ; turn extruder 0 off
G1 X122.0 Y67.0 ; here4
G1 X122.0 Y67.0 ; here1
G1 Z0.2
M42 P16 S255 ; turn extruder 0 on
G1 X117.0 Y72.0 ; here2
G1 X112.0 Y67.0 ; here2
G1 X107.0 Y72.0 ; here2
G1 X102.0 Y67.0 ; here2
G1 X97.0 Y72.0 ; here2
G1 X92.0 Y67.0 ; here2
E0

C1 S0 ; uncap the extruder
G1 Z10.2 ; make sure we don't destroy the tip
T1 ; switch the extruder
C1 S255 ; cap the extruder
G1 Z0.2 ; go back
M42 P16 S0 ; turn extruder 1 off
G1 ; here5
G1 X92.0 Y42.0 
 ; here5
G1 X92.0 Y42.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 1 on
G1 X92.0 Y72.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 1 off
G1 ; here5
G1 X97.0 Y42.0 ; here5
G1 X97.0 Y42.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 1 on
G1 X97.0 Y72.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 1 off
G1 ; here5
G1 X102.0 Y42.0 ; here5
G1 X102.0 Y42.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 1 on
G1 X102.0 Y72.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 1 off
G1 ; here5
G1 X107.0 Y42.0 ; here5
G1 X107.0 Y42.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 1 on
G1 X107.0 Y72.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 1 off
G1 ; here5
G1 X112.0 Y42.0 ; here5
G1 X112.0 Y42.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 1 on
G1 X112.0 Y72.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 1 off
G1 ; here5
G1 X117.0 Y42.0 ; here5
G1 X117.0 Y42.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 1 on
G1 X117.0 Y72.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 1 off
G1 ; here5
G1 X122.0 Y42.0 ; here5
G1 X122.0 Y42.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 1 on
G1 X122.0 Y72.0 ; here2
E0



C1 S0 ; uncap the extruder
G1 Z10.4 ; make sure we don't destroy the tip
T2 ; switch the extruder
C1 S255 ; cap the extruder
G1 Z0.4 ; go back
E0
M42 P16 S0 ; turn extruder 2 off
G1 ; here5
G1 X92.0 Y42.0 
 ; here5
G1 X92.0 Y42.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 2 on
G1 X122.0 Y42.0 ; here2
E0
M42 P16 S0 ; turn extruder 2 off
G1 ; here5
G1 X92.0 Y47.0 
 ; here5
G1 X92.0 Y47.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 2 on
G1 X122.0 Y47.0 ; here2
E0
M42 P16 S0 ; turn extruder 2 off
G1 ; here5
G1 X92.0 Y52.0 
 ; here5
G1 X92.0 Y52.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 2 on
G1 X122.0 Y52.0 ; here2
E0
M42 P16 S0 ; turn extruder 2 off
G1 ; here5
G1 X92.0 Y57.0 
 ; here5
G1 X92.0 Y57.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 2 on
G1 X122.0 Y57.0 ; here2
E0
M42 P16 S0 ; turn extruder 2 off
G1 ; here5
G1 X92.0 Y62.0 
 ; here5
G1 X92.0 Y62.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 2 on
G1 X122.0 Y62.0 ; here2
E0
M42 P16 S0 ; turn extruder 2 off
G1 ; here5
G1 X92.0 Y67.0 
 ; here5
G1 X92.0 Y67.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 2 on
G1 X122.0 Y67.0 ; here2
E0
M42 P16 S0 ; turn extruder 2 off
G1 ; here5
G1 X92.0 Y72.0 
 ; here5
G1 X92.0 Y72.0 ; here1
G1 Z0.4
M42 P16 S255 ; turn extruder 2 on
G1 X122.0 Y72.0 ; here2
E0

C1 S0 ; uncap the extruder
G1 Z10.4 ; make sure we don't destroy the tip
T3 ; switch the extruder
C1 S255 ; cap the extruder
G1 Z0.4 ; go back
E0
M42 P16 S0 ; turn extruder 3 off
G1 ; here5
G1 X92.0 Y42.0 ; here5
G1 X92.0 Y42.0 ; here1
G1 Z0.6
M42 P16 S255 ; turn extruder 3 on
G1 X97.0 Y47.0 ; here2
G1 X92.0 Y52.0 ; here2
G1 X97.0 Y57.0 ; here2
G1 X92.0 Y62.0 ; here2
G1 X97.0 Y67.0 ; here2
G1 X92.0 Y72.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 3 off
G1 ; here5
G1 X97.0 Y42.0 ; here5
G1 X97.0 Y42.0 ; here1
G1 Z0.6
M42 P16 S255 ; turn extruder 3 on
G1 X102.0 Y47.0 ; here2
G1 X97.0 Y52.0 ; here2
G1 X102.0 Y57.0 ; here2
G1 X97.0 Y62.0 ; here2
G1 X102.0 Y67.0 ; here2
G1 X97.0 Y72.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 3 off
G1 ; here5
G1 X102.0 Y42.0 ; here5
G1 X102.0 Y42.0 ; here1
G1 Z0.6
M42 P16 S255 ; turn extruder 3 on
G1 X107.0 Y47.0 ; here2
G1 X102.0 Y52.0 ; here2
G1 X107.0 Y57.0 ; here2
G1 X102.0 Y62.0 ; here2
G1 X107.0 Y67.0 ; here3
M42 P16 S0 ; turn extruder 3 off
G1 X107.0 Y67.0 ; here1
G1 Z0.6
M42 P16 S255 ; turn extruder 3 on
G1 X102.0 Y72.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 3 off
G1 ; here5
G1 X107.0 Y42.0 ; here5
G1 X107.0 Y42.0 ; here1
G1 Z0.6
M42 P16 S255 ; turn extruder 3 on
G1 X112.0 Y47.0 ; here2
G1 X107.0 Y52.0 ; here2
G1 X112.0 Y57.0 ; here2
G1 X107.0 Y62.0 ; here2
G1 X112.0 Y67.0 ; here2
G1 X107.0 Y72.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 3 off
G1 ; here5
G1 X112.0 Y42.0 ; here5
G1 X112.0 Y42.0 ; here1
G1 Z0.6
M42 P16 S255 ; turn extruder 3 on
G1 X117.0 Y47.0 ; here2
G1 X112.0 Y52.0 ; here2
G1 X117.0 Y57.0 ; here2
G1 X112.0 Y62.0 ; here2
G1 X117.0 Y67.0 ; here2
G1 X112.0 Y72.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 3 off
G1 ; here5
G1 X102.0 Y42.0 ; here5
G1 X102.0 Y42.0 ; here1
G1 Z0.6
M42 P16 S255 ; turn extruder 3 on
G1 X107.0 Y47.0 ; here2
G1 X102.0 Y52.0 ; here2
G1 X107.0 Y57.0 ; here2
G1 X102.0 Y62.0 ; here2
G1 X107.0 Y67.0 ; here2
G1 X102.0 Y72.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 3 off
G1 ; here5
G1 X117.0 Y42.0 ; here5
G1 X117.0 Y42.0 ; here1
G1 Z0.6
M42 P16 S255 ; turn extruder 3 on
G1 X122.0 Y47.0 ; here2
G1 X117.0 Y52.0 ; here2
G1 X122.0 Y57.0 ; here2
G1 X117.0 Y62.0 ; here2
G1 X122.0 Y67.0 ; here2
G1 X117.0 Y72.0 ; here2
E0

C1 S0 ; uncap the extruder
G1 Z10.6 ; make sure we don't destroy the tip
T4 ; switch the extruder
C1 S255 ; cap the extruder
G1 Z0.6 ; go back
E0
M42 P16 S0 ; turn extruder 4 off
G1 ; here5
G1 X92.0 Y42.0 ; here5
G1 X92.0 Y42.0 ; here1
G1 Z0.8
M42 P16 S255 ; turn extruder 4 on
G1 X97.0 Y47.0 ; here2
G1 X102.0 Y42.0 ; here2
G1 X107.0 Y47.0 ; here2
G1 X112.0 Y42.0 ; here2
G1 X117.0 Y47.0 ; here2
G1 X122.0 Y42.0 ; here2
E0
M42 P16 S0 ; turn extruder 4 off
G1 X122.0 Y47.0 ; here4
G1 X122.0 Y47.0 ; here1
G1 Z0.8
M42 P16 S255 ; turn extruder 4 on
G1 X117.0 Y52.0 ; here2
G1 X112.0 Y47.0 ; here2
G1 X107.0 Y52.0 ; here2
G1 X102.0 Y47.0 ; here2
G1 X97.0 Y52.0 ; here2
G1 X92.0 Y47.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 4 off
G1 X92.0 Y52.0 
 ; here4
G1 X92.0 Y52.0 ; here1
G1 Z0.8
M42 P16 S255 ; turn extruder 4 on
G1 X97.0 Y57.0 ; here2
G1 X102.0 Y52.0 ; here2
G1 X107.0 Y57.0 ; here2
G1 X112.0 Y52.0 ; here2
G1 X117.0 Y57.0 ; here2
G1 X122.0 Y52.0 ; here2
E0
E0 
M42 P16 S0 ; turn extruder 4 off
G1 X122.0 Y57.0 
 ; here4
G1 X122.0 Y57.0 ; here1
G1 Z0.8
M42 P16 S255 ; turn extruder 4 on
G1 X117.0 Y62.0 ; here2
G1 X112.0 Y57.0 ; here2
G1 X107.0 Y62.0 ; here2
G1 X102.0 Y57.0 ; here2
G1 X97.0 Y62.0 ; here2
G1 X92.0 Y57.0 ; here2
E0
E0
M42 P16 S0 ; turn extruder 4 off
G1 X92.0 Y62.0 
 ; here4
G1 X92.0 Y62.0 ; here1
G1 Z0.8
M42 P16 S255 ; turn extruder 4 on
G1 X97.0 Y67.0 ; here2
G1 X102.0 Y62.0 ; here2
G1 X107.0 Y67.0 ; here2
G1 X112.0 Y62.0 ; here2
G1 X117.0 Y67.0 ; here2
G1 X122.0 Y62.0 ; here2
E0
M42 P16 S0 ; turn extruder 4 off
G1 X122.0 Y67.0 ; here4
G1 X122.0 Y67.0 ; here1
G1 Z0.8
M42 P16 S255 ; turn extruder 4 on
G1 X117.0 Y72.0 ; here2
G1 X112.0 Y67.0 ; here2
G1 X107.0 Y72.0 ; here2
G1 X102.0 Y67.0 ; here2
G1 X97.0 Y72.0 ; here2
G1 X92.0 Y67.0 ; here2
E0


C1 S0 ; uncap the extruder
G1 Z10.8 ; make sure we don't destroy the tip
T5 ; switch the extruder
C1 S255 ; cap the extruder
G1 Z0.8 ; go back
E0
M42 P16 S0 ; turn extruder 5 off
G1 ; here5
G1 X92.0 Y42.0 
 ; here5
G1 X92.0 Y42.0 ; here1
G1 Z1.0
M42 P16 S255 ; turn extruder 5 on
G1 X122.0 Y42.0 ; here2
E0
M42 P16 S0 ; turn extruder 5 off
G1 X92.0 Y47.0 
 ; here4
G1 X92.0 Y47.0 ; here1
G1 Z1.0
M42 P16 S255 ; turn extruder 5 on
G1 X122.0 Y47.0 ; here2
E0
M42 P16 S0 ; turn extruder 5 off
G1 X92.0 Y52.0 
 ; here4
G1 X92.0 Y52.0 ; here1
G1 Z1.0
M42 P16 S255 ; turn extruder 5 on
G1 X122.0 Y52.0 ; here2
E0
M42 P16 S0 ; turn extruder 5 off
G1 X92.0 Y57.0 
 ; here4
G1 X92.0 Y57.0 ; here1
G1 Z1.0
M42 P16 S255 ; turn extruder 5 on
G1 X122.0 Y57.0 ; here2
E0
M42 P16 S0 ; turn extruder 5 off
G1 X92.0 Y62.0 
 ; here4
G1 X92.0 Y62.0 ; here1
G1 Z1.0
M42 P16 S255 ; turn extruder 5 on
G1 X122.0 Y62.0 ; here2
E0
M42 P16 S0 ; turn extruder 5 off
G1 X92.0 Y67.0 
 ; here4
G1 X92.0 Y67.0 ; here1
G1 Z1.0
M42 P16 S255 ; turn extruder 5 on
G1 X122.0 Y67.0 ; here2
E0
M42 P16 S0 ; turn extruder 5 off
G1 X92.0 Y72.0 
 ; here4
G1 X92.0 Y72.0 ; here1
G1 Z1.0
M42 P16 S255 ; turn extruder 5 on
G1 X122.0 Y72.0 ; here2
E0
M42 P16 S0
M42 P17 S0
G1 Z50 F1000
G1 E0 F1000
G1 X0 Y0 F1000

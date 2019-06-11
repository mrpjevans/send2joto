G21 ; Set units to Metric
G90 ; Absolute coordinates

M106 S40 ; Move Joto's pen to position 40 which lifts the nib out of the dock
G4 P500 ; Short pause to allow the pen to move
M106 S0 ; Turn the motor off that moves the pen

; This block of commands allows Joto to reliably set the home (0,0) position 
G91
G1 F16000
M202 X450 Y450
G1 X5
G28 X0
G1 Y5
G28 Y0
G90
G4 P1000

M202 X250 Y250 ; Set the acceleration for your jot
G1 F8000 ; Set the speed

; Drawing
; Repeat the commands below with your own X,Y, coordinates to draw multiple lines

G1 X120 Y120 ; G1 is a move command which will move the pen to a specific X,Y, coordinate
M106 S110.0 ; Move Joto's pen to position 110 which presses the nib onto the surface
G4 P60.0

; After the pen is in the down position add your X,Y, coordinates to draw a line 
G1 X152.58 Y282.55 
G1 X151.99 Y281.51 
G1 X151.36 Y280.56 
G1 X150.71 Y279.69 
G1 X150.03 Y278.91 

M106 S70.0 ; Move Joto's pen to position 70 which lifts the nib off the surface
G4 P60.0

; Finish code
M106 S40 ; lifts the nib all the way up, ready to enter the dock
G4 P100
M106 S0

; This block of commands allows Joto to reliably get back to the home (0,0) position 
G91
G1 F16000
M202 X450 Y450
G1 X5
G28 X0
G1 Y5
G28 Y0
G90
G4 P1000
M106 S140 ; Moves Joto's pen to position 140 to place the nib back into the dock
G4 P1000
M106 S0
M84 ; Turns Joto's motors off. 
G21 ; Set units to Metric
G90 ; Absolute coordinates

M106 S30 ; Move Joto's pen to position 40 which lifts the nib out of the dock
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
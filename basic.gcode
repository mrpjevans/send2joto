G21 ; Set units to Metric
G90 ; Absolute coordinates

M106 S40 ; Move Joto's pen to position 40 which lifts the nib out of the dock
G4 P500 ; Short pause to allow the pen to move
M106 S235;
G4 P1000
M106 S0
M84 ; Turns Joto's motors off. 

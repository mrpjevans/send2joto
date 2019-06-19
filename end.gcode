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
M106 S{{pen_dock}} ; Moves Joto's pen to position 140 to place the nib back into the dock
G4 P1000
M84 ; Turns Joto's motors off. 

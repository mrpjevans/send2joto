#
# text2joto.py
# A script to convert a line of text to Joto gcode
# (c) 2019 PJ Evans <pj@mkcodesmiths.com>
# MIT License
#
# Absolutely no warranty. Use at your own risk. Bad gcode can
# break a Joto.
#
# Usage: See README
#
import argparse
import json
import sys
import os

my_dir = os.path.dirname(os.path.realpath(__file__))

# Command line
parser = argparse.ArgumentParser(description='Generate Joto gcode from text')
parser.add_argument('-t', '--text', type=str, default="",
                    help='Text string to convert')
parser.add_argument('-s', '--size', type=float, default=0.5,
                    help='Size of type (1 is big, try 0.2!)')
parser.add_argument('-u', '--pen-up', type=int, default=70,
                    help='Pen up position (try 70)')
parser.add_argument('-d', '--pen-down', type=int, default=175,
                    help='Pen down position (try 140 upwards)')
parser.add_argument('-o', '--pen-dock', type=int, default=235,
                    help='Pen dock position (try 190 upwards)')
parser.add_argument('-y', '--y-padding', type=float, default=4,
                    help='Padding between lines')
parser.add_argument('-g', '--gcode', action="store_true", default=False,
                    help='Include gcode start and end')
parser.add_argument('-b', '--start-gcode', type=str,
                    default=(my_dir + '/start.gcode'),
                    help='Path to start gcode')
parser.add_argument('-e', '--end-gcode', type=str,
                    default=(my_dir + '/end.gcode'),
                    help='Path to end gcode')
parser.add_argument('-f', '--font', type=str,
                    default=(my_dir + '/default_font.json'),
                    help='Font description file')

args = parser.parse_args()
text = args.text
font_size = args.size
pen_up = args.pen_up
pen_down = args.pen_down
pen_dock = args.pen_dock
y_padding = args.y_padding


# Read a file in line-by-line
def read_to_array(file_name):

    out = []
    f = open(file_name, "r")
    for line in f:
        line = line.replace("{{pen_up}}", pen_up)
        line = line.replace("{{pen_down}}", pen_down)
        line = line.replace("{{pen_dock}}", pen_dock)
        out.append(line.rstrip())

    return out


# No text? Attempt to read from stdin
if text == "":
    for line in sys.stdin:
        text += line.strip()
    if text == "":
        print("Nothing to do!")
        sys.exit(0)

# Do not permit any drawing over these co-ords
x_boundary = 280
y_boundary = 300

# Character patterns
f = open("default_font.json", "r")
font = json.load(f)

# Header and footer
if args.gcode:
    start_code = read_to_array("start.gcode")
    end_code = read_to_array("end.gcode")

# Header
if args.gcode:
    for line in start_gcode:
        print(line)

# Calculate and move to start position
x_offset = 0
y_offset = y_boundary - (100 * font_size)
print('G1 X%.2f Y%.2f' % (x_offset, y_offset))

# For each character
for character in text:

    if character not in font:
        print("Unknown character: " + character)
        sys.exit(1)

    # Repeat until successfully processed
    while True:

        x_right = 0
        repeat = False
        gcode = []

        # For each gcode command
        for cmd in font[character]:

            if cmd[0] == 'u':  # Pen up
                gcode.append('M106 S%i' % (pen_up))
                gcode.append('G4 P60.0')
            elif cmd[0] == 'd':  # Pen down
                gcode.append('M106 S%i' % (pen_down))
                gcode.append('G4 P60.0')
            elif cmd[0] == 'm':  # Move

                # Calc actual position to move to
                x = x_offset + (cmd[1] * font_size)
                y = y_offset + (cmd[2] * font_size)

                # Keep track of the rightmost point
                if x_right == 0 or x > x_right:
                    x_right = x

                # Would we draw over the boundary?
                if x_right > x_boundary:
                    repeat = True
                    break

                # Add instruction
                gcode.append('G1 X%.2f Y%5.2f' % (x, y))

        # If the last loop failed as we went too far right
        # move to the next line and repeat the character
        if repeat:
            x_offset = 0
            x_right = 0
            y_offset -= ((100 * font_size) + y_padding)
            # Too far down the page?
            if y_offset < 50:
                print("Dosen't fit :(")
                sys.exit(1)
        else:

            # Output the generated gcode for the letter
            for line in gcode:
                print(line)

            # Move offset along 1 character
            x_offset = x_right

            # Leave the infinite loop
            break

# Footer
if args.gcode:
    for line in end_gcode:
        print(line)

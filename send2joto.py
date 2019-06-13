#
# send2joto.py
# A script to send gcode to the Joto whiteboard plotter
# (c) 2019 PJ Evans <pj@mkcodesmiths.com>
# MIT License
#
# Absolutely no warranty. Use at your own risk. Bad gcode can
# break a Joto.
#
# Credit to Magus Bower for insipiration and Gcode
# https://gist.github.com/almostscheidplatz/915d9dd9ed6326599088a5d4750d5076
#
# Usage: See README
#

import time
import serial
import json
import sys
import os
import argparse

# Command line
parser = argparse.ArgumentParser(description='Send Gcode to a Joto')
parser.add_argument('-p', '--port', type=str, required=True,
                    help='Path to the USB serial connection')
parser.add_argument('-f', '--file', type=str, default="",
                    help='Gcode file to process')
args = parser.parse_args()

# Configure serial
ser = serial.Serial(
    port=args.port,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)


def sendLine(line):

    while True:

        # Clean the line and don't bother if empty
        line = str.strip(line)
        if line == '' or line[0] == ';':
            return True

        # Send line
        print("<< " + line)
        ser.write(str.encode(line + '\r\n'))

        # Check response
        response = ""
        timeout = 50

        while response == "":
            time.sleep(0.2)
            while ser.inWaiting() > 0:
                response += ser.read(1).decode("utf-8")
            timeout -= 1
            if timeout == 0:
                print("Timeout waiting for Joto's response")
                return False
            if response.strip() == "busy:processing":
                print("Waiting")
                time.sleep(1)
                response = ""

        # Validate response
        gotOk = False
        responseByLine = response.splitlines(False)
        for responseLine in responseByLine:
            print(">> " + responseLine)
            if responseLine == 'ok 0':
                gotOk = True

        if gotOk:
            break

    return True


# Check the file to send
if args.file != and os.path.isfile(args.file) is False:
    print('File not found')
    sys.exit(1)

# Cycle the port
ser.close()
ser.open()


# Open the file or stdin and read each line
if args.file != "":
    f = open(args.file, "r")
    for line in f:
        if sendLine(line) is False:
            break
    f.close()
else:
    for line in sys.stdin:
        if sendLine(line) is False:
            break

# Tidy up
ser.close()
sys.exit()

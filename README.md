# send2joto
Simple Python script to send gcode to a Joto whiteboard

## What It Does

This is a script that sends your gcode file to Joto and handles responses, checking for errors. I am using it as a starting platform for writing my own Joto apps. If you wnat to get starting programming Joto directly, it may come in useful.

## Requirements

* Python 3


## Usage

Joto connects to your computer as a serial device. You need to work out which one is Joto.

**Linux**
Look in /dev for a device named ttyACM0 or similar.

**macOs**
Look in /dev for a device named tty.usbmodem14201 or similar.

**Windows**
Not a clue, sorry. If someone wants to submit a PR...

To send a file of gcode instructions to Joto:

```bash
python3 send2joto.py --port /dev/tty.usbmodem14201 --file /path/to/file.gcode
```

Progress will be displayed on-screen.

## Example Gcode

Included are some sample scripts that will enter/leave care mode, wipe the board (slowly!) and draw a test line.

## Disclaimer

This utility is provided 'as is' with no warranty. Gcode can harm your Joto. Use at your own risk.

## And Finally..

Thanks to Magus Bower for insipiration and Gcode [https://gist.github.com/almostscheidplatz/915d9dd9ed6326599088a5d4750d5076]()


Improvements, suggestions and PRs welcomed.
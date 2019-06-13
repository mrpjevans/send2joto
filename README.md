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

If you omit the `--file` argument, the script will attempt to read from stdin, so you can pipe gcode to it!

## Example Gcode

Included are some sample scripts that will enter/leave care mode, wipe the board (slowly!) and draw a test line.

## Disclaimer

This utility is provided 'as is' with no warranty. Gcode can harm your Joto. Use at your own risk.

## And Finally..

Thanks to Magus Bower for insipiration and Gcode [https://gist.github.com/almostscheidplatz/915d9dd9ed6326599088a5d4750d5076]()


Improvements, suggestions and PRs welcomed.


# text2joto

## What It Does
Convert a text string to Joto-friendly gcode.

## Requirements

* Python 3

## Usage Examples

```bash
python3 text2joto.py
```
In this case text will read from stdin. To specify text as an argument, see options.

```bash
python3 text2joto.py -t "Hello"
```

Generate the gcode to spell out 'Hello'

```bash
python3 text2joto.py -g -s 0.2 -t "Hello"
```

Generate a complete gcode script to spell out 'Hello' in font size 0.2.


## Options

All are optional

`-t, --text "Hello"` The text to convert (rather than reading stdin)

`-s, --size 0.2` Font size (float) - 1.0 is quite large. Defaults to 0.5.

`-u, --pen-up` The 'pen up' position. Defaults to 70.

`-d, --pen-down` The 'pen down' position. Defaults to 175.

`-y, --y-padding` How much space to leave between lines. Defaults to 4.

`-g, --gcode` Include gcode start and end scripts (see below). Defaults to False.

`-b, --start-gcode` Path to start gcode script. Defaults to `./start.gcode`.

`-e, --end-gcode` Path to end gcode script. Defaults to `./end.gcode`.

`-f, --font` Font definition file to use. Defaults to `./default_font.json`.

## Boundaries

The gcode generation routine checks for whether a movement will take the pen outside of a safe area. On the x-axis, this cause a new line. If you run out of line sof the y-axis, the script will stop with a warning.

## Start and End Gcode Scripts

Included with the package are `start.gcode` and `end.gcode`. These are based on
the scripts released by Those for the Joto. By default, only the gcode for the
text itself is generated. This is not enough for the Joto, so a start and finish script
are required to correctly undock and then dock the pen. You can edit these files to suit your needs or replace them using the b and e arguments.

## Generating Font Definition JSON

The default_font.json file included is a simple line font derived from StickFont by NCPlot.

You can create your own fonts. The definition file is a JSON file formatted as follows:

```json
{
	"a": [
		["action", x, y]
	]
}
```

Where "a" is the letter or number to render. Within the following array are arrays of one of three types:

`["u"]` Pen up

`["d"]` Pen down

`["m", x, y]` Move to position x, y

So each letter is a group of actions that are converted into gcode. See stickfont2joto below for more.

# stickfont2joto

StickFont by NCPlot is a useful Windows utility for converting TTF fonts to single-line gcode. Perfect for Joto. the default_font.json file was generated using output from this program.

Unfortunately, the gcode generated is not a flavour Joto understands. This script converts StickFont gcode to either Joto gcode or a section of a Font Definition JSON for text2joto to use.

## Usage
```bash
python stickfont2joto.py -f a.gcode
```

This will produce a JSON definition section for the gcode in a.gcode.

```bash
python stickfont2joto.py -g -f a.gcode
```

This will produce a block of gcode for the same.


## Options

`-s, --s` Scale. Should normally be left at 1 (default).

`-c, --c` When generating JSON, specifically state which character this is. If not specified, the filename (without extension) will be used.

`-g, --gcode` Instead of generating JSON, generate Joto gcode instead.

`-u, --pen-up` Preferred 'pen up' value (Default 70).

`-d, --pen-down` Preferred 'pen down' value (Default 175).

`-x, --x-offset` (Gcode only) Starting point on the x-axis.

`-y, --y-offset` (Gcode only) Starting point on the y-axis.

`-f, --file` (Required) Source StickFont gcode file.

## Warning

Be careful using `-x` and `-y`. There are no boundary checks. Movements outside
Joto's safe area could damage your Joto.

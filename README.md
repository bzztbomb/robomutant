ROBOMUTANT
==========
Machines playing machines. A step towards creating a anamatronic mutant savior to inspire the masses to rise up against the Robotrons.

Robomutant is made up of two pieces.  Mikey is an interface between external code and MAME.  Tensortron is an attempt at a tensorflow graph that can play robotron.

MIKEY
=====
This is a a MAME LUA plugin that allows for external programs to see the framebuffer of a game and deliver input to mame. There are two modes, blocking and non-blocking.  Blocking mode will wait for input before allow the game to advance to the next frame.  Non-blocking will just take input as it is fed.  Turn blocking mode on by setting
`
local block_until_processed = true
`
in mikey/init.lua

To use the plugin, copy the directory into plugs/mikey then run mame like so:
`
./mame64 -window -plugins -plugin mikey robotron
`

1. If current_frame.png doesn't exist, the plugin will save the current frame to snap/robotron/current_frame.png
2. If blocking it will wait for an external program to produce input_moves.csv
3. If input_moves.csv exists it will read the current moves and send them to mame.

Input moves is a csv file that contains port, fieldname, and value. Here's an example:

`
:IN0,Move Left,1
:IN0,Move Up,0
:IN0,Move Right,0
:IN0,Move Down,0
:IN0,Fire Down,1
:IN0,Fire Up,0
:IN0,1 Player Start,0
:IN1,Fire Left,0
:IN1,Fire Right,0
`

DADDY
=====

Daddy generates random moves every frame. It makes sure MIKEY is doing his job. Run with a pretty vanilla python.

TENSORTRON
==========
An attempt at DEEP LEARNING bot. Not working yet.

`
# Record input movesand video
./mame64 -record input -aviwrite movie.avi robotron
# Train
python train.py
# Play
python play.py
./mame64 -plugins -plugin mikey robotron
`

Useful code in tensortron is in utils.py, parse a MAME INP file

Based on
========
* TensorKart -- https://github.com/kevinhughes27/TensorKart
* Which is based on Autopilot-Tensorflow: https://github.com/SullyChen/Autopilot-TensorFlow

TODO
====
* Convert input structure to use directions instead of port values
* Maybe use a 2d cost function based on joystick position so we get better costs
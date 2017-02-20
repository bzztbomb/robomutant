import os
import random

threshold = 0.7
num_frames = 4

def axis_to_moves(portname, fieldnames, axisval):
  retvalues = [0, 0]
  if (axisval < -threshold):
    retvalues[0] = 1
  if (axisval > threshold):
    retvalues[1] = 1
  lines = []
  for i in range(2):
    lines.append(portname + "," + fieldnames[i] + "," + str(retvalues[i]))
  return lines

def roborand():
  return (random.random() * 2.0) - 1.0

snap_dir = "/Users/bzztbomb/projects/mame/snap/robotron"
screenshot = os.path.join(snap_dir, "current_frame.png")
moves = os.path.join(snap_dir, "moves.csv")

think_frame = 0
lines = []

while True:
  # Look
  while (os.path.isfile(screenshot) == False):
    pass
  # Think
  if (think_frame % num_frames == 0):
    print("think")
    moveupdown = roborand()
    moveleftright  = roborand()
    fireupdown  = roborand()
    fireleftright  = roborand()
    start = roborand()
    # Act
    lines = []
    # lines.extend(port_to_moves(":IN0", ["Move Up", "Move Down", "Move Left", "Move Right", "1 Player Start", "2 Players Start", "Fire Up", "Fire Down"], port0))
    # lines.extend(port_to_moves(":IN1", ["Fire Left", "Fire Right"], port1))
    lines.extend(axis_to_moves(":IN0", ["Move Down", "Move Up"], moveupdown))
    lines.extend(axis_to_moves(":IN0", ["Move Left", "Move Right"], moveleftright))
    lines.extend(axis_to_moves(":IN0", ["Fire Down", "Fire Up"], fireupdown))
    lines.extend(axis_to_moves(":IN1", ["Fire Left", "Fire Right"], fireleftright))
    lines.append(":IN0,1 Player Start," + ("1" if start > threshold else "0"))

  print((moveupdown, moveleftright, fireupdown, fireleftright, start))
  print("\n")
  print(lines)
  print("\n")
  f = open(moves + ".tmp", "w")
  for line in lines:
    f.write(line)
    f.write("\n")
  f.close()
  os.rename(moves + ".tmp", moves)
  os.remove(screenshot)
  think_frame = think_frame + 1

# PORT_START("IN0")
# PORT_BIT( 0x01, IP_ACTIVE_HIGH, IPT_JOYSTICKLEFT_UP ) PORT_NAME("Move Up")
# PORT_BIT( 0x02, IP_ACTIVE_HIGH, IPT_JOYSTICKLEFT_DOWN ) PORT_NAME("Move Down")
# PORT_BIT( 0x04, IP_ACTIVE_HIGH, IPT_JOYSTICKLEFT_LEFT ) PORT_NAME("Move Left")
# PORT_BIT( 0x08, IP_ACTIVE_HIGH, IPT_JOYSTICKLEFT_RIGHT ) PORT_NAME("Move Right")
# PORT_BIT( 0x10, IP_ACTIVE_HIGH, IPT_START1 )
# PORT_BIT( 0x20, IP_ACTIVE_HIGH, IPT_START2 )
# PORT_BIT( 0x40, IP_ACTIVE_HIGH, IPT_JOYSTICKRIGHT_UP ) PORT_NAME("Fire Up")
# PORT_BIT( 0x80, IP_ACTIVE_HIGH, IPT_JOYSTICKRIGHT_DOWN ) PORT_NAME("Fire Down")

# PORT_START("IN1")
# PORT_BIT( 0x01, IP_ACTIVE_HIGH, IPT_JOYSTICKRIGHT_LEFT ) PORT_NAME("Fire Left")
# PORT_BIT( 0x02, IP_ACTIVE_HIGH, IPT_JOYSTICKRIGHT_RIGHT ) PORT_NAME("Fire Right")
# PORT_BIT( 0xfc, IP_ACTIVE_HIGH, IPT_UNKNOWN )

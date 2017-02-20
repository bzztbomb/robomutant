import tensorflow as tf
import model
import os.path
import matplotlib.pyplot as plt

threshold = 0.7

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

snap_dir = "/Users/bzztbomb/projects/mame/snap/robotron"
screenshot = os.path.join(snap_dir, "current_frame.png")
moves = os.path.join(snap_dir, "moves.csv")

sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

# Load Model
saver = tf.train.Saver()
saver.restore(sess, "./model.ckpt")

while True:
  # Look
  while (os.path.isfile(screenshot) == False):
    pass
  image = None
  while (image == None):
    try:
      image = plt.imread(screenshot)
      print (image.shape)
    except:
      pass
  # Think
  output = model.y.eval(feed_dict={model.x: [image], model.keep_prob: 1.0})
  # Act
  (moveupdown, moveleftright, fireupdown, fireleftright, start) = output[0]
  lines = []
  # lines.extend(port_to_moves(":IN0", ["Move Up", "Move Down", "Move Left", "Move Right", "1 Player Start", "2 Players Start", "Fire Up", "Fire Down"], port0))
  # lines.extend(port_to_moves(":IN1", ["Fire Left", "Fire Right"], port1))
  lines.extend(axis_to_moves(":IN0", ["Move Down", "Move Up"], moveupdown))
  lines.extend(axis_to_moves(":IN0", ["Move Left", "Move Right"], moveleftright))
  lines.extend(axis_to_moves(":IN0", ["Fire Down", "Fire Up"], fireupdown))
  lines.extend(axis_to_moves(":IN1", ["Fire Left", "Fire Right"], fireleftright))
  # lines.append(":IN0,1 Player Start," + "1" if start > threshold else "0")

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
  # Delete old input


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

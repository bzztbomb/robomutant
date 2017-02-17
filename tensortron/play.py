import tensorflow as tf
import model
import os.path
import matplotlib.pyplot as plt

def port_to_moves(portname, fieldnames, portval):
  result = []
  bit_to_check = 1
  for field in fieldnames:
    output = portname + "," + field + "," + str(1 if (portval & bit_to_check) else 0) + "\n"
    result.append(output)
    bit_to_check = bit_to_check << 1
  return result

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
    except:
      pass
  # Think
  output = model.y.eval(feed_dict={model.x: [image], model.keep_prob: 1.0})
  # Act
  (port0, port1) = output[0]
  port0 = int(port0)
  port1 = int(port1)
  lines = []
  lines.extend(port_to_moves(":IN0", ["Move Up", "Move Down", "Move Left", "Move Right", "1 Player Start", "2 Players Start", "Fire Up", "Fire Down"], port0))
  lines.extend(port_to_moves(":IN1", ["Fire Left", "Fire Right"], port1))
  print(lines)
  print("\n")
  f = open(moves + ".tmp", "w")
  for line in lines:
    f.write(line)
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

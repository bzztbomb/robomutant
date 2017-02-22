import os
import random
import numpy as np
import cv2
import math

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

# Set up the detector with default parameters.
blobParams = cv2.SimpleBlobDetector_Params()
blobParams.filterByConvexity = False
blobParams.filterByInertia = False
blobParams.filterByArea = False
blobParams.minArea = 5
blobParams.filterByCircularity = False
blobParams.filterByColor = False
detector = cv2.SimpleBlobDetector_create(blobParams)

savior = []
num_savior_frames = 9
for i in range(num_savior_frames):
  savior.append(cv2.imread('reference/mutant' + str(i) + ".png"))

savior_loc = []
while True:
  # Look
  while (os.path.isfile(screenshot) == False):
    pass
  image = None
  while (image == None):
    try:
      image = cv2.imread(screenshot)
      image = image[16:-12,8:-12]
    except:
      pass

  # Find the savior
  last_loc = savior_loc
  savior_loc = []
  for template in savior:
    if savior_loc != []:
      break
    w, h = template.shape[:-1]
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc):
      savior_loc = (pt[1], pt[0])
      print("Savior found!")
      break
  # if savior_loc == []:
  #   savior_loc = last_loc

  # Detect blobs.
  img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  (thresh, im_bw) = cv2.threshold(img_gray, 16, 255, cv2.THRESH_BINARY)
  keypoints = detector.detect(im_bw)
  if (len(keypoints) > 0 and savior_loc != []):
    keypoints = sorted(keypoints, key=lambda kp: math.hypot(kp.pt[0] - savior_loc[0], kp.pt[1] - savior_loc[1]))
    kp = keypoints[1 if len(keypoints) > 1 else 0]
    print("kp: " + str(kp.pt))
    print("savior: " + str(savior_loc))
    x_index = 0
    y_index = 1
    movedownup = 1 if kp.pt[y_index] > savior_loc[y_index] else -1
    moveleftright = -1 if kp.pt[x_index] > savior_loc[x_index] else 1
    firethresh = 20
    if abs(kp.pt[y_index] - savior_loc[y_index]) > firethresh:
      fireupdown = -movedownup
    else:
      fireupdown = 0
    if abs(kp.pt[x_index] - savior_loc[x_index]) > firethresh:
      fireleftright = -moveleftright
    else:
      fireleftright = 0

    # Think
    # movedownup = roborand()
    # moveleftright  = roborand()
    # fireupdown  = roborand()
    # fireleftright  = roborand()
    start = roborand()
    # Act
    lines = []
    # lines.extend(port_to_moves(":IN0", ["Move Up", "Move Down", "Move Left", "Move Right", "1 Player Start", "2 Players Start", "Fire Up", "Fire Down"], port0))
    # lines.extend(port_to_moves(":IN1", ["Fire Left", "Fire Right"], port1))
    lines.extend(axis_to_moves(":IN0", ["Move Down", "Move Up"], movedownup))
    lines.extend(axis_to_moves(":IN0", ["Move Left", "Move Right"], moveleftright))
    lines.extend(axis_to_moves(":IN0", ["Fire Down", "Fire Up"], fireupdown))
    lines.extend(axis_to_moves(":IN1", ["Fire Left", "Fire Right"], fireleftright))
    lines.append(":IN0,1 Player Start," + ("1" if start > threshold else "0"))
  else:
    lines = []
    # lines.extend(port_to_moves(":IN0", ["Move Up", "Move Down", "Move Left", "Move Right", "1 Player Start", "2 Players Start", "Fire Up", "Fire Down"], port0))
    # lines.extend(port_to_moves(":IN1", ["Fire Left", "Fire Right"], port1))
    lines.extend(axis_to_moves(":IN0", ["Move Down", "Move Up"], 0))
    lines.extend(axis_to_moves(":IN0", ["Move Left", "Move Right"], 0))
    lines.extend(axis_to_moves(":IN0", ["Fire Down", "Fire Up"], 0))
    lines.extend(axis_to_moves(":IN1", ["Fire Left", "Fire Right"], 0))
    start = roborand()
    lines.append(":IN0,1 Player Start," + ("1" if start > threshold else "0"))


  # print((moveupdown, moveleftright, fireupdown, fireleftright, start))
  # print("\n")
  # print(lines)
  # print("\n")
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

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

video = None
save_debug = False

savior_loc = []
while True:
  # Look
  while (os.path.isfile(screenshot) == False):
    pass
  image = None
  while (image == None):
    try:
      image = cv2.imread(screenshot)
      image = image[17:-12,8:-12]
    except:
      pass

  if (video == None) and (save_debug == True):
    height, width, channels = image.shape
    if (os.path.isfile('output.mp4')):
      os.remove('output.mp4')
    video = cv2.VideoWriter('output.mp4', -1, 10.0, (width,height))

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
    im_with_keypoints = cv2.drawKeypoints(im_bw, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    if (video != None):
      video.write(im_with_keypoints)

    # Convert keypoints to tuples
    pts = []
    for kp in keypoints:
      pts.append((kp.pt[0], kp.pt[1]))
    height, width, channels = image.shape
    # Treat corners as enemies
    pts.append((0,0))
    pts.append((0,height))
    pts.append((width,height))
    pts.append((width,0))
    pts = sorted(pts, key=lambda kp: math.hypot(kp[0] - savior_loc[0], kp[1] - savior_loc[1]))
    kp = pts[1 if len(pt) > 1 else 0]
    print("kp: " + str(kp))
    print("savior: " + str(savior_loc))
    x_index = 0
    y_index = 1
    movedownup = 1 if kp[y_index] > savior_loc[y_index] else -1
    moveleftright = -1 if kp[x_index] > savior_loc[x_index] else 1
    firethresh = 15
    if abs(kp[y_index] - savior_loc[y_index]) > firethresh:
      fireupdown = -movedownup
    else:
      fireupdown = 0
    if (abs(kp[x_index] - savior_loc[x_index]) > firethresh) or (fireupdown == 0):
      fireleftright = -moveleftright
    else:
      fireleftright = 0

    # Act
    lines = []
    lines.extend(axis_to_moves(":IN0", ["Move Down", "Move Up"], movedownup))
    lines.extend(axis_to_moves(":IN0", ["Move Left", "Move Right"], moveleftright))
    lines.extend(axis_to_moves(":IN0", ["Fire Down", "Fire Up"], fireupdown))
    lines.extend(axis_to_moves(":IN1", ["Fire Left", "Fire Right"], fireleftright))
    start = roborand()
    lines.append(":IN0,1 Player Start," + ("1" if start > threshold else "0"))
  else:
    lines = []
    lines.extend(axis_to_moves(":IN0", ["Move Down", "Move Up"], 0))
    lines.extend(axis_to_moves(":IN0", ["Move Left", "Move Right"], 0))
    lines.extend(axis_to_moves(":IN0", ["Fire Down", "Fire Up"], 0))
    lines.extend(axis_to_moves(":IN1", ["Fire Left", "Fire Right"], 0))
    start = roborand()
    lines.append(":IN0,1 Player Start," + ("1" if start > threshold else "0"))

  f = open(moves + ".tmp", "w")
  for line in lines:
    f.write(line)
    f.write("\n")
  f.close()
  os.rename(moves + ".tmp", moves)
  os.remove(screenshot)

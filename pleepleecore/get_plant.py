from collections import deque
import numpy as np
import cv2
import sys
import imutils
import time

colors = [[(20, 131, 84), (50, 255, 132), (0, 0, 0)]]

def get_plant(filename):
    """Get whether a plant is detected or not in a previously
    stored image.

    Return:
        True if a plant is detected, False overwise

    Args:
        filename: The path to the file to analyze.
    """
    points = deque(maxlen=50000)
    frame = cv2.imread(filename)
    frame = imutils.resize(frame, width=500)
    # HSV is betted for our filtering
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    data = []
    for color in colors:
        mask = cv2.inRange(hsv, color[0], color[1])
        # Eliminate noise then expand what remains
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        x, y, radius = 0, 0, 0
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        points.appendleft(center)
        for i in range(1, len(points)):
            if points[i - 1] is None or points[i] is None:
                continue
        data.append((x, y, color, radius, 0, center))
    print(data)
    for d in data:
        ok = True
        # Skip "no detections"
        if d[4] == -1 and d[0] == 0 and d[1] == 0:
            continue
        for d2 in data:
            if d == d2:
                continue
            minr = min(d[3], d2[3])
            maxr = max(d[3], d2[3])
            dx = abs(d[0]-d2[0])
            dy = abs(d[1]-d2[1])
            if maxr * maxr * 1.2 > dx * dx + dy * dy and d[3] < d2[3]:
            # If we intersect a bigger circle, it is not a valid circle.
                ok = False
                continue
            # Size and validity filtering.
        if d[3] > 50 and ok:
            cv2.circle(frame, (int(d[0]), int(d[1])), int(d[3]), d[2][2], 5)
            cv2.circle(frame, d[5], 5, d[2][2], -1)
            return True
    return False

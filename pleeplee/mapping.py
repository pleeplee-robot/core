#! /usr/bin/env python3

import sys

import primitives

from pleeplee import Location


filename='inputs.txt'

if len(sys.argv) > 1:
    filename = sys.argv[1]

perimeter = readPerimeterFromFile(filename)
angleNorth = readAngleNorth()
dirInit = (-10.0, -10.0)
angleToDirection = -90.0
height = 0.0
odometry = Odometry(Point(6.5, 6.7), 0.6)

data0 = Data(Color.RED, 134.0, *args)
data1 = Data(Color.YELLOW, 19.0, *args)
data2 = Data(Color.BLUE, -25.0, *args)
datas = [data0, data1, data2]

# Init & use of location
loc = Location(angleNorth, dirInit, height, *perimeter)
loc.computePos(angleToDirection, odometry, *datas)

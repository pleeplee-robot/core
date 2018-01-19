#! /usr/bin/env python3

from enum import Enum

from pleepleeloc.geometry import Point
from pleepleeloc.utils import LED, Color, Data

# Primitives of the application that for now just print

# Primitive function to go forward (in cm)
def goForward(length):
    print('Go forward {} cm'.format(length))

# Primitive function to turn from x radian.
# For now the robots can only turn right
def turn(radians):
    print('Turn {} radians'.format(radians))

class ServoState(Enum):
    ServoRight = 0
    ServoRightFront = 1
    ServoFront = 2
    ServoLeftFront = 3
    ServoLeft = 4

def trunServomotor(state):
    print('Turn servomotor axis into choosen state:')

# Primitive function
def takeAPicture():
    print('Take a picture')
    path = '~'
    return path

def analysePicture(path):
    print('Analyse picture')


def readPerimeterFromFile(path):
    print('Read input file for perimeter')

    # Fake datas for now

    corner1 = LED(Color.RED, Point(3.0, 3.0))
    corner2 = LED(Color.YELLOW, Point(13.0, 5.0))
    corner3 = LED(Color.BLUE, Point(11.0, 9.0))
    corner4 = LED(Color.GREEN, Point(1.0, 10.0))
    perimeter = [corner1, corner2, corner3, corner4]
    return perimeter

def readAngleNorth():
    print('Read the angle between the North and the axis of the robot')

    return -45.0


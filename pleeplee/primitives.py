#! /usr/bin/env python3

from enum import Enum

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
    print('Turn servomotor axis into coosen state:')

# Primitive function
def takeAPicture():
    print('Take a picture')
    path = '~'
    return path

def analysePicture(path):
    print('Analyse picture')

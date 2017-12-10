#! /usr/bin/env python3

# Primitives of the application that for now just print

def goForward(length):
    print('Go forward {} cm'.format(length))


def turn(radians):
    print('Turn {} radians'.format(radians))


def takeAPicture():
    print('Take a picture')
    path = '~'
    return path

def analysePicture(path):
    print('Analyse picture')

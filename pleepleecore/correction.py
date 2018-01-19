#! /usr/bin/env python3

import math

PRECISION = 0.1

def getCorrection(start, end, pos):
    """Correct the angle for the trajectory adjustment

    Function to get the correct angle correction when the robot deviates from
    it's estimated trajectory.

    Args:
       start: The starting position of the robot.
       end: The position the robot is supposed to arrive.
       pos: The current position of the robot.

    Returns:
        An angle in radians between -pi and pi to correct the robot trajectory
        and arrive succesfully at end position.
    """
    (xs, ys) = start
    (xe, ye) = end
    (xp, yp) = pos

    # Discard edge cases with no sense
    assert(xs != xe or ys != ye)
    assert(xp != xe or yp != ye)
    assert(xs != xp or ys != yp)

    # First get the line equation from start to end points.
    # line equation follows the following pattern: y = m * x + b
    m = 0.0
    b = 0.0
    if abs(xe - xs) > PRECISION:
        m = (ye - ys) / (xe - xs)
        b = ys - m * xs
    else:
        m = 1
        b = - xs

    # Get the perpendicular line equation to the first line
    mp = 0.0
    bp = 0.0
    if abs(xe - xs) < PRECISION:
        bp = yp
    elif abs(m) < PRECISION:
        mp = 1
        bp = - xp
    else:
        mp = - 1 / m
        bp = yp - mp * xp

    # Get the point at the intersection of the two lines
    xi = 0.0
    yi = 0.0
    if abs(xe - xs) < PRECISION:
        xi = b
        yi = bp
    elif abs(m) < PRECISION:
        xi = bp
        yi = b
    else:
        xi = - (bp - b) / (mp - m)
        yi = m * xi + b

    # Get the distance between the tree points
    dist_pi = math.sqrt((xp - xi) * (xp - xi) + (yp - yi) * (yp - yi))
    dist_pe = math.sqrt((xp - xe) * (xp - xe) + (yp - ye) * (yp - ye))
    dist_sp = math.sqrt((xs - xp) * (xs - xp) + (ys - yp) * (ys - yp))

    # Get the offset angles alpha and beta
    alpha = math.asin(dist_pi / dist_pe)
    beta = math.asin(dist_pi / dist_sp)

    return - (alpha + beta)

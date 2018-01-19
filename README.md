[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# PleePlee Robot

![logo](https://github.com/pleeplee-robot/location/blob/master/resources/logo-pleeplee.png)

PleePlee is a proof of concept of a mobile gardener robot.
This repository is about the code for miscellaneous components of the robot.
It contains the code and documentation for:
- the camera
- the LEDs
- the motor driver
- the odometric captors

## Features

The PleePlee robot is able to:
- :seedling: :shower: Water plants.
- :car: Move in a straight line and turn in place.
- :bulb: :satellite: Localize itself in a small area delimited by luminous landmarks.
- :curly_loop: Avoid obstacles.
- :eyes: Log any changes to the garden. (Foreign object or person crossing).


## Core

This repository holds the core code of the robot, that will send orders
to components, recieve the result of these orders, use the location API
and contains the core logic of the robot behavior.

This repository is the only one that is not complete yet. The integration of
the mapping and the algorithm to avoid obstacle are still missing.



#pragma once

/**
 *  Debug information on the laser used.
 */
void print_laser_information(ArRobot& robot);

/**
 *  Retrieve at which angle the closest object is.
 */
double get_min_dist_angle(ArRobot& robot, double angle_scan);

/**
 *  Retrieve the distance with the first obstacle in the @angle_scan direction
 */
double peek_dist_angle(ArRobot& robot, double angle_scan);

/*
 * Debug information on what is the minimum distance between the robot and
 * any obstacle.
 */
void print_min_dist_angle(ArRobot& robot, double angle_scan);

#pragma once

#include "Aria.h"

/**
 *  Simple structure to define a point in 2D space.
 */
struct Point
{
    double x;
    double y;
};

using Point = struct Point;


/**
 *  State the result of the wallfollowing of the robot.
 */
enum class result_state : char
{
    ERROR,
    SUCCESS,
    FREE,
    UNKNOWN
};

/**
 *  Return true if the robot is on the almost on the destination 8cm accuracy.
 */
bool on_point(ArRobot& robot, Point destination);

/**
 *  Return true if the robot can reach the destination when wall following the
 *  obstacle.
 */
bool free_space(ArRobot& robot, Point destination);

/**
 *  This function makes the robot wall follow the obstacle obstacle and return
 *  a result state. If during the wall following we reach the destination the
 *  the state is SUCCESS, is there is a free space between the robot and the
 *  destintaiton the state FREE. Otherwise, ERROR.
 */
result_state wall_follow(Point old_point, ArRobot& robot, Point destination);

/**
 *  Return true if the robot meet an obstacle the distance. Any object which is
 *  at less than 2 Robot radius + 50cm is considered as an obstacle.
 */
bool has_encounter_obstacle(ArRobot& robot);

/**
 *  Make the robot to turn toward the point destination and move in the right
 *  direction until the robot is on the destination or if an obstacle has been
 *  encountered.
 */
void move_toward(ArRobot& robot, Point destination);

/**
 *  High level algorithm that call the other functions. Basically, implements
 *  a distbug algorithm.
 */
int reach_destination(ArRobot& robot, Point destination);

#include "robot.hh"
#include "utils.hh"

void turn_toward(ArRobot& robot, Point destination)
{
    auto curr_pos = Point{robot.getX(), robot.getY()};
    double xi = destination.x - curr_pos.x;
    double yi = destination.y - curr_pos.y;
    double angle1 = atan2(yi, xi);
    robot.enableMotors();
    int rotVel = 10;
    double angle = (angle1 - (robot.getTh() * M_PI / 180)) * 180 / M_PI;

    if (!angle)
	rotVel *= -1;

    while (angle > 2 || angle < -2)
    {
    	robot.lock();
    	robot.setVel(0);
    	robot.setRotVel(10);
    	robot.unlock();
    	angle = (angle1 - (robot.getTh() * M_PI / 180)) * 180 / M_PI;
    }
}

bool on_point(ArRobot& robot, Point destination)
{
    return (((robot.getX() - destination.x) < 80) &&
	    ((robot.getX() - destination.x) > -80) &&
	    ((robot.getY() - destination.y) < 80) &&
	    ((robot.getY() - destination.y) > -80));
}

bool free_space(ArRobot& robot, Point destination)
{
    auto curr_pos = Point{robot.getX(), robot.getY()};
    double xi = destination.x - curr_pos.x;
    double yi = destination.y - curr_pos.y;
    double angle1 = atan2(yi, xi);
    double angle = (angle1 - (robot.getTh() * M_PI / 180)) * 180 / M_PI;
    return angle > 0; // The Goal is on the left or in front of the robot.
}

bool has_encounter_obstacle(ArRobot& robot)
{
    // If min dist is less than 2 * robot size + 5cm then there is an obstacle
    return (get_min_dist_angle(robot, 10) <= 2 * robot.getRobotRadius() + 50);
}

static void recadre_robot(ArRobot& robot, double distance_to_wall)
{
    if (distance_to_wall > 480)
    {
	std::cout << "RECADRING RIGHT" << std::endl;
	robot.lock();
	robot.setVel(20);
	robot.setRotVel(-2);
	robot.unlock();
	ArUtil::sleep(250);
    }
    else if (distance_to_wall < 410)
    {
	std::cout << "RECADRING LEFT" << std::endl;
	robot.lock();
	robot.setVel(20);
	robot.setRotVel(2);
	robot.unlock();
	ArUtil::sleep(250);
    }
}

result_state wall_follow(Point old_point, ArRobot& robot, Point destination)
{
    // First always follow by going on the left side
    ArLog::log(ArLog::Normal, "my_robot: Rotating at 20 deg/s for 4.5 sec...");
    robot.lock();
    robot.setVel(0);
    robot.setRotVel(20);
    robot.unlock();
    ArUtil::sleep(4500);

    while (!on_point(robot, destination) &&
	   !free_space(robot, destination))
    {
	double md = peek_dist_angle(robot, -90);
	double md_l = peek_dist_angle(robot, -80);
	double md_r = peek_dist_angle(robot, -100);

	double rotVel = 0;
	double vel = 200;
	double sleep = 500;
	if ((md_l > md_r + 10)) // Turn right
	{
	    if (md_l - md - md_r > 100) // Stop and Turn
	    {
		std::cout << "HIGH RIGHT" << std::endl;
		rotVel = -20;
		vel = 80;
	    }
	    else
	    {
		std::cout << "RIGHT" << std::endl;
		rotVel = -7;
		vel = 25;
	    }
	}
	else if ((md_r > md_l + 10)) // Turn left
	     {
		 if (md_r - md - md_l > 100) // Stop and Turn
		 {
		     std::cout << "HIGH LEFT" << std::endl;
		     rotVel = 20;
		     vel = 80;
		 }
		 else
		 {
		     std::cout << "LEFT" << std::endl;
		     rotVel = 7;
		     vel = 25;
		 }
	     }
	else // IF LOST SHOULD MOVE_TOWARD
	    std::cout << "STRAIGHT" << std::endl;

	if (md < 420 || md > 480)
	    std::cerr << "MD: " <<  md << std::endl;

	robot.lock();
	robot.setVel(vel);
	robot.setRotVel(rotVel);
	robot.unlock();
	ArUtil::sleep(sleep);
	recadre_robot(robot, md);

    }
    if (!on_point(robot, destination))
	return result_state::FREE;

    return result_state::SUCCESS;
}

void move_toward(ArRobot& robot, Point destination)
{
    turn_toward(robot, destination);
    while (!on_point(robot, destination) && !has_encounter_obstacle(robot))
    {
    	robot.lock();
    	robot.setRotVel(0);
    	robot.setVel(200);
    	robot.unlock();
    }
    robot.stop();
}

int reach_destination(ArRobot& robot, Point destination)
{
    auto curr_pos = Point{robot.getX(), robot.getY()};
    auto old_leave_point = curr_pos;

    while (true)
    {
	move_toward(robot, destination);
	curr_pos = Point{robot.getX(), robot.getY()};

	if (on_point(robot, destination))
	    break;

	auto result = wall_follow(curr_pos, robot, destination);

	switch (result)
	{
	case result_state::ERROR:
	    return 1;
	case result_state::SUCCESS:
	    return 0;
	case result_state::FREE:
	    old_leave_point = Point{robot.getX(), robot.getY()};
	    break;
	case result_state::UNKNOWN:
	    old_leave_point = Point{robot.getX(), robot.getY()};
	    break;
	default:
	    return -1;
	}
    }

    return 0;
}

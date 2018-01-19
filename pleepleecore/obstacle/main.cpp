#include "robot.hh"
#include "utils.hh"

int main(int argc, char **argv)
{
    Aria::init();

    ArRobot robot;
    ArArgumentParser parser(&argc, argv);

    parser.loadDefaultArguments();

    ArRobotConnector robotConnector(&parser, &robot);
    ArLaserConnector laserConnector(&parser, &robot, &robotConnector);

    if (!robotConnector.connectRobot())
    {
	ArLog::log(ArLog::Terse, "my_robot: Could not connect to the robot.");
	if (parser.checkHelpAndWarnUnparsed())
	{
	    Aria::logOptions();
	    Aria::exit(1);
	}
    }
    if (!Aria::parseArgs())
    {
	Aria::logOptions();
	Aria::shutdown();
	return 1;
    }

    ArLog::log(ArLog::Normal, "my_robot: Connected.");

    robot.runAsync(true);

    if (!laserConnector.connectLasers())
    {
	std::cout << "Can’t connect to laser\n"; //Exit if error
	Aria::exit(0);
	exit(1);
    }

    robot.lock();
    ArLog::log(ArLog::Normal, "my_robot: Pose=(%.2f,%.2f,%.2f), Trans. Vel=%.2f,"
	       "Rot. Vel=%.2f, Battery=%.2fV", robot.getX(), robot.getY(),
	       robot.getTh(), robot.getVel(), robot.getRotVel(),
	       robot.getBatteryVoltage());
    robot.unlock();

    Point destination = Point{0, 8262};
    char *endptr;

    if (argc == 3)
	destination = Point{(double)strtol(argv[1], &endptr, 10),
			    (double)strtol(argv[2], &endptr, 10)};

    // MAP2 / MAP3 Point{7651, 8180};
    reach_destination(robot, destination);

    robot.lock();
    ArLog::log(ArLog::Normal, "my_robot: Pose=(%.2f,%.2f,%.2f), Trans. Vel=%.2f,"
	       "Rot. Vel=%.2f, Battery=%.2fV", robot.getX(), robot.getY(),
	       robot.getTh(), robot.getVel(), robot.getRotVel(),
	       robot.getBatteryVoltage());
    robot.unlock();

    ArLog::log(ArLog::Normal, "my_robot: Ending robot thread...");
    robot.stopRunning();
    robot.waitForRunExit();
    ArLog::log(ArLog::Normal, "my_robot: Exiting.");
    return 0;
}

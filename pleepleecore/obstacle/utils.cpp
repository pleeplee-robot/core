#include "robot.hh"

void print_laser_information(ArRobot& robot)
{
    const ArRobotParams *params = robot.getRobotParams();
    for(size_t i = 1; i <= robot.getNumLasers(); ++i)
    {
	if(!robot.findLaser(i))
	    continue;

	ArLog::log(ArLog::Normal,
		   "\tlaser #%d: pose=(x:%d, y:%d, z:%d, th:%0.2f), powerOutput=%s\n",
		   i,
		   params->getLaserX(i), params->getLaserY(i),
		   params->getLaserZ(i), params->getLaserTh(i),
		   params->getLaserPowerOutput(i)
	    );
    }
}

double get_min_dist_angle(ArRobot& robot, double angle_scan)
{
    double dist;

    std::map<int, ArLaser*> *lasers = robot.getLaserMap();
    for(std::map<int, ArLaser*>::const_iterator i = lasers->begin(); i != lasers->end(); ++i)
    {
        //int laserIndex = i->first;
	ArLaser* laser = i->second;
	if(!laser)
	    continue;
	laser->lockDevice();

	double angle = 0;
	dist = laser->currentReadingPolar(-angle_scan, angle_scan, &angle);

	laser->unlockDevice();
    }
    return dist;
}

double peek_dist_angle(ArRobot& robot, double angle_scan)
{
    double dist;

    std::map<int, ArLaser*> *lasers = robot.getLaserMap();
    for(std::map<int, ArLaser*>::const_iterator i = lasers->begin(); i != lasers->end(); ++i)
    {
	int laserIndex = i->first;
	ArLaser* laser = i->second;
	if(!laser)
	    continue;
	laser->lockDevice();

	double angle = 0;
	dist = laser->currentReadingPolar(angle_scan - 1, angle_scan + 1, &angle);

	ArLog::log(ArLog::Normal, "angle_scan %lf, Laser #%d (%s): %s. "
		   "Closest reading is at %3.0f degrees and is %2.4f at meters",
		   angle_scan, laserIndex, laser->getName(),
		   (laser->isConnected() ? "connected" : "NOT CONNECTED"),
		   angle, dist/1000.0);

	laser->unlockDevice();
    }
    return dist;
}


void print_min_dist_angle(ArRobot& robot, double angle_scan)
{
    robot.lock();
    std::map<int, ArLaser*> *lasers = robot.getLaserMap();
    for(std::map<int, ArLaser*>::const_iterator i = lasers->begin(); i != lasers->end(); ++i)
    {
	int laserIndex = i->first;
	ArLaser* laser = i->second;
	if(!laser)
	    continue;
	laser->lockDevice();

	double angle = 0;
	double dist = laser->currentReadingPolar(-angle_scan, angle_scan, &angle);

	ArLog::log(ArLog::Normal, "Laser #%d (%s): %s. "
		   "Closest reading is at %3.0f degrees and is %2.4f at meters",
		   laserIndex, laser->getName(),
		   (laser->isConnected() ? "connected" : "NOT CONNECTED"),
		   angle, dist/1000.0);
	laser->unlockDevice();
    }
    robot.unlock();
}

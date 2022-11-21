import sys
from os import getlogin
sys.path.append(f"/home/flw/IT_IS_WORKING/crazyswarm/ros_ws/src/crazyswarm/scripts/")

import numpy as np
from pycrazyswarm import *
import sys
import math
import time
import rospy
from time import sleep

class CrazyflieWrapper(object):
    def __init__(self, start_time, land_time, movement_time, movement_amount, height):
        cf_yaml = '/home/flw/IT_IS_WORKING/crazyswarm/ros_ws/src/crazyswarm/launch/crazyflies.yaml'
        self.swarm = Crazyswarm(crazyflies_yaml=cf_yaml)
        self.allcfs = self.swarm.allcfs
        self.start_time = start_time
        self.land_time = land_time
        self.movement_time = movement_time
        self.movement_amount = movement_amount
        self.height = height
        self.time_for_next_command = time.time()
        self.relative_position = Vector3D()

    def check_and_set_time_for_command(self, commands_seconds):
        if self.time_for_next_command <= time.time():
            self.time_for_next_command = time.time() + commands_seconds
            return True
        return False

    def print_debug(self):
        print("time for starting:", self.start_time)
        print("time for landing:", self.land_time)
        print("time for moving:", self.movement_time)
        print("amount of moving:", self.movement_amount)
        print("height:", self.height)

    def move(self, vector):
        if self.check_and_set_time_for_command(self.movement_time):
            vector.scale(self.movement_amount)
            self.relative_position.addX(vector.getX())
            self.relative_position.addY(vector.getY())
            self.relative_position.addZ(vector.getZ())
            print(vector.getX(), vector.getY(), vector.getZ())
            for cf in self.allcfs.crazyflies:
                pos = np.array(cf.initialPosition) + np.array([self.relative_position.getX(), self.relative_position.getY(), self.relative_position.getZ()])
                cf.goTo(pos, 0, self.movement_time)
            sleep(self.movement_time)

    def start(self):
        if self.check_and_set_time_for_command(self.start_time):
            self.allcfs.takeoff(targetHeight=self.height, duration=self.start_time)
            print("start")

    def land(self):
        if self.check_and_set_time_for_command(self.land_time):
            self.allcfs.land(targetHeight=0.00, duration=self.land_time)
            print("land")

class Vector3D(object):
    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        self.x = x
        self.y = y
        self.z = z
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getZ(self):
        return self.z
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def setZ(self, z):
        self.z = z
    def addX(self, amount):
        self.x += amount
    def addY(self, amount):
        self.y += amount
    def addZ(self, amount):
        self.z += amount
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    def scale(self, amount):
        own_length = self.length()
        self.x = amount * self.x / own_length
        self.y = amount * self.y / own_length
        self.z = amount * self.z / own_length

def format_decimal(number):
    return '{0:.2f}'.format(number)

class InterfaceDrone:
    def __init__(self, realMode=True) -> None:
        self.realMode = realMode
        self.start_time = 2.5
        self.land_time = 2.5
        self.movement_time = 2.5
        self.movement_amount = 0.5
        self.height = 0.3
        self.rate = 10  # [Hz] Rate of publishing waypoints
        self.circle_path = self.generate_circle_path(r=2, time=self.movement_time)
        if self.realMode:
            print(self.realMode)
            self.cfs = CrazyflieWrapper(self.start_time, self.land_time, self.movement_time, self.movement_amount, self.height)
        print("Connected to Drone successfully")

    def generate_circle_path(self,r:float,time:float):
        pi=math.pi
        n = time*self.rate # No. of points on circumference
        #waypoints = [(round((math.cos(2*pi/n*x)*r)-r, 2), round(math.sin(2*pi/n*x)*r, 2)) for x in range(0,n+1)]
        #return waypoints

    def takeoff(self):
        if self.realMode:
            self.cfs.start()

    def land(self):
        if self.realMode:
            self.cfs.land()

    def perform_gesture(self, command):
        current_direction = Vector3D()
        if command == "Left":
            current_direction.addX(-1.0)
        elif command == "Right":
            current_direction.addX(1.0)
        elif command == "Front":
            current_direction.addY(1.0)
        elif command == "Back":
            current_direction.addY(-1.0)
        elif command == "Up":
            current_direction.addZ(1.0)
        elif command == "Down":
            current_direction.addZ(-1.0)
        elif command == "CW_Circle":    #TODO: Check documentation for trajectory https://crazyswarm.readthedocs.io/en/latest/api.html#crazyflie-class
            waypoints = self.circle_path
            rate = rospy.Rate(self.rate)
            for waypoint in waypoints:
                for cf in self.cfs.allcfs.crazyflies:
                    pos = np.array(cf.initialPosition) + np.array([waypoint[0], waypoint[1], 0])
                    cf.cmdPosition(pos)
                rate.sleep()
            return
        elif command == "CCW_Circle":
            waypoints = self.circle_path.reverse()  # Reverse the list to get CCW
            rate = rospy.Rate(self.rate)
            for waypoint in waypoints:
                for cf in self.cfs.allcfs.crazyflies:
                    pos = np.array(cf.initialPosition) + np.array([waypoint[0], waypoint[1], 0])
                    cf.cmdPosition(pos)
                rate.sleep()
            return

        if self.realMode:
            if current_direction.length() > 0.01:
                self.cfs.move(current_direction)
        print(f"Drone successfully performed gesture: {command}")
#!/usr/bin/env bash

#Run  gets
rosrun data_manager getBattery.py &
rosrun data_manager getMotor.py &
rosrun data_manager getPositionAMCL.py &
rosrun data_manager getPositionOdom.py &

# Run buffer manager
rosrun data_manager bufferManager.py


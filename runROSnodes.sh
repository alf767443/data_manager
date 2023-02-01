#!/usr/bin/env bash

# init and sinc
python3 init.py &&

# Clean
# rosnode kill /getBattery
# rosnode kill /getMotors
# rosnode kill /getPosition
# rosnode kill /getPositionOdom
rosnode kill /listenNodes
rosnode kill /bufferManager




#Run  gets
# rosrun data_manager getBattery.py &
# rosrun data_manager getMotor.py &
# rosrun data_manager getPositionAMCL.py &
# rosrun data_manager getPositionOdom.py &

# Run buffer manager
rosrun data_manager listenNodes.py &
rosrun data_manager bufferManager.py



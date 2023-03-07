#!/usr/bin/env bash

bash ~/catkin_ws/src/data_manager/killROSnodes.sh

rosrun data_manager listenNode.py &
rosrun data_manager bufferManager.py &
rosrun data_manager getSignal.py &
# rosrun data_manager queueAction.py &
rosrun data_manager getNodes.py &
rosrun data_manager diagnostic.py &
rosrun data_manager getHTOP.py &


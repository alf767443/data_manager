#!/usr/bin/env bash
rosrun data_manager listenNode.py &
rosrun data_manager bufferManager.py &
rosrun data_manager getSignal.py &
# rosrun data_manager queueAction.py &
rosrun data_manager getNodes.py &
rosrun data_manager diagnostic.py &


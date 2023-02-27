#!/usr/bin/env bash

# init and sinc

# Clean
rosnode kill /listenNodes
rosnode kill /bufferManager
rosnode kill /getSignal
rosnode kill /queueActions
rosnode kill /getNodes
rosnode kill /platform_diagnostics

# Run buffer manager
rosrun data_manager listenNode.py &
rosrun data_manager getSignal.py &
# rosrun data_manager queueActions.py &
rosrun data_manager bufferManager.py

rosrun data_manager listenNode.py &
rosrun data_manager bufferManager.py &
rosrun data_manager getSignal.py &
# rosrun data_manager queueAction.py &
rosrun data_manager getNodes.py &
rosrun data_manager diagnostic.py &


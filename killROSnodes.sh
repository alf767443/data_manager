#!/usr/bin/env bash

# init and sinc

# Clean
rosnode kill /listenNodes
rosnode kill /bufferManager
rosnode kill /getSignal
rosnode kill /queueActions
rosnode kill /getNodes
rosnode kill /platform_diagnostics

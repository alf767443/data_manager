#!/usr/bin/env python3

import rospy
import subprocess

# Inicialize o nó do ROS
rospy.init_node('my_node')

# Obtenha a lista de nós em execução
nodes = subprocess.check_output(['rosnode', 'list']).decode().splitlines()

# Para cada nó em execução, obtenha as conexões
for node in nodes:
    connections = subprocess.check_output(['rosnode', 'info', node]).decode().splitlines()
    print('Node:', node)
    print('Connections:', connections)

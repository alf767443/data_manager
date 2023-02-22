#!/usr/bin/env python3
import rospy
import rosnode

if __name__ == '__main__':
    rospy.init_node('node_info')
    nodes = rosnode.get_node_names()
    for node in nodes:
        node_info = rosnode.get_node_info(node)
        connections = node_info.connections
        print("Node:", node)
        print("URI:", node_info.uri)
        print("PID:", node_info.pid)
        print("Connections:")
        for c in connections:
            print("  *", c)
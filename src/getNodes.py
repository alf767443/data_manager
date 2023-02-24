#!/usr/bin/env python3

import rospy
from rosnode import get_node_names

if __name__ == '__main__':
    rospy.init_node('node_list')
    node_names = get_node_names()
    print("Nodes currently running:\n{}".format("\n".join(node_names)))

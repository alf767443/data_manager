#!/usr/bin/env python3

import rosnode


if __name__ == '__main__':
    rospy.init_node('node_info')
    node_list = rosnode.get_node_names()
    print(node_list)
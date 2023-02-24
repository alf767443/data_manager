#!/usr/bin/env python3

import rospy

if __name__ == '__main__':
    rospy.init_node('node_info')
    node_names = rospy.get_published_topics()
    print("Nodes and Topics currently running:\n{}".format("\n".join([str(x) for x in node_names])))

#!/usr/bin/env python3
import rospy
import rosnode

if __name__ == '__main__':
    rospy.init_node('node_info')
    nodes = rosnode.get_node_names()
    for node in nodes:
        print("Node:", node)
        node_info = rosnode.get_node_info(node)
        print("  URI:", node_info.uri)
        print("  PID:", node_info.pid)
        published_topics = rospy.get_published_topics(node)
        print("  Published Topics:")
        for t in published_topics:
            print("    *", t[0], "\tType:", t[1])
            subscribers = rospy.get_subscriber_info(t[0])
            print("    Subscribers:")
            for s in subscribers:
                print("      *", s[1], "\tType:", s[3])
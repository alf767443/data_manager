#!/usr/bin/env python3
import rospy
import rosgraph

if __name__ == '__main__':
    rospy.init_node('node_info')
    nodes = rosgraph.Master('/rostopic').getSystemState()[0]
    for node in nodes:
        node_info = rosgraph.Master('/rostopic').lookupNode(node)
        node_uri = node_info.uri
        node_pid = node_info.pid
        print("Node:", node)
        print("URI:", node_uri)
        print("PID:", node_pid)
        published_topics = rospy.get_published_topics(node)
        print("Published Topics:")
        for t in published_topics:
            print("  *", t)
        for t in published_topics:
            subscribers = rospy.get_subscriber_info(t[0])
            print("Subscribers for", t[0], ":")
            for s in subscribers:
                print("  *", s[1], "connected to", s[0])
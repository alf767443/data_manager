#!/usr/bin/env python3
import rospy

if __name__ == '__main__':
    rospy.init_node('node_info')
    nodes = rospy.get_node_names()
    for node in nodes:
        print("Node:", node)
        published_topics = rospy.Publisher.get_num_connections(rospy.Publisher("test_topic", rospy.Empty, queue_size=1)._impl.tcpros_pub)
        print("  Published Topics:", published_topics)
        subscriptions = rospy.Subscriber.get_num_connections(rospy.Subscriber("test_topic", rospy.Empty)._impl.tcpros_sub)
        print("  Subscriptions:", subscriptions)
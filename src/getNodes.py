#!/usr/bin/env python3

import rospy
import rosgraph
import rosnode

if __name__ == '__main__':
    rospy.init_node('topic_info')
    
    # get list of topics and their types
    topics = rospy.get_published_topics()
    
    # print out the list of topics and their types
    print('Topics:')
    for topic in topics:
        print(topic)
        
        # get list of nodes publishing and subscribing to this topic
        publishers, subscribers = rosgraph.Master('/rostopic').getTopicTypes(topic)
        nodes = publishers + subscribers
        
        # print out the list of nodes publishing and subscribing to this topic
        for node in nodes:
            print('  Node: ' + node)
            
            # get list of topics that this node is publishing to
            pubs, _ = rospy.get_published_topics(node)
            print('    Publishes:')
            for pub in pubs:
                print('      ' + pub[0])
            
            # get list of topics that this node is subscribing to
            _, subs, _ = rospy.client.get_master().getSystemState()
            node_subs = [x[0] for x in subs if node in x[1]]
            print('    Subscribes:')
            for sub in node_subs:
                print('      ' + sub)
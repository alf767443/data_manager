#!/usr/bin/env python3

import rospy

#Obtem os nós e os seus publishers e subscribers
if __name__ == '__main__':
    rospy.init_node('node_info')
    topics = rospy.get_published_topics()
    node_dict = {}
    for topic in topics:
        node_name = topic[0].split('/')[1]
        if node_name not in node_dict:
            node_dict[node_name] = {'publishes': [], 'subscribes': []}
        if topic[0].startswith('/' + node_name + '/'):
            node_dict[node_name]['publishes'].append(topic[0])
        else:
            node_dict[node_name]['subscribes'].append(topic[0])

    for node_name, node_info in node_dict.items():
        print(f"Node: {node_name}")
        print(f"Publishes to: {node_info['publishes']}")
        print(f"Subscribes to: {node_info['subscribes']}")

#!/usr/bin/env python3

import rospy
import rostopic

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
        for topic in node_info['publishes'] + node_info['subscribes']:
            try:
                pubs, subs, _ = rostopic.get_topic_type(topic)
                pubs = [p.split('/')[1] for p in pubs if len(p.split('/')) > 1]
                subs = [s.split('/')[1] for s in subs if len(s.split('/')) > 1]
                if topic.startswith('/'):
                    source_node = topic.split('/')[1]
                else:
                    source_node = node_name
                for target_node in pubs + subs:
                    if target_node != source_node:
                        print(f"  {source_node} -> {target_node}")
            except rostopic.ROSTopicIOException:
                pass

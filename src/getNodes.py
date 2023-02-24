#!/usr/bin/env python3

import rospy
import rosnode
from rosnode import NodeInfoProxy

if __name__ == '__main__':
    rospy.init_node('node_info')
    node_names = rosnode.get_node_names()
    print("Nodes currently running:\n{}".format("\n".join(node_names)))

    for node_name in node_names:
        try:
            node_api = rosnode.get_api_uri(rospy.get_master(), node_name)
            node_info = NodeInfoProxy(node_name)
            pubs, subs, srvs = node_info.get_uri(), node_info.get_published_topics(), node_info.get_service_list()
            print("Node name: {}\nAPI URI: {}\nPublications: {}\nSubscriptions: {}\nServices: {}\n"
                  .format(node_name, node_api, pubs, subs, srvs))
            
        except Exception as e:
            print(e)
            pass

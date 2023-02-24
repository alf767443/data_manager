#!/usr/bin/env python3

import rospy
import rosnode

if __name__ == '__main__':
    rospy.init_node('node_info')
    node_names = rosnode.get_node_names()
    print("Nodes currently running:\n{}".format("\n".join(node_names)))

    for node_name in node_names:
        try:
            node_api = rosnode.get_api_uri(rospy.get_master(), node_name)
            node_info = rosnode.get_node_info(node_name)
            print("Node name: {}\nAPI URI: {}\nPublications: {}\nSubscriptions: {}\nServices: {}\n"
                  .format(node_name, node_api, node_info.get('publications'), node_info.get('subscriptions'),
                          node_info.get('services')))
        except Exception as e:
            print(e)
            pass

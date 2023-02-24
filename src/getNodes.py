#!/usr/bin/env python3

import rospy
import rosnode
from rosgraph import Master, Node

if __name__ == '__main__':
    rospy.init_node('node_info')
    master = Master('/rostopic')
    node_names = rosnode.get_node_names()
    print("Nodes currently running:\n{}".format("\n".join(node_names)))

    for node_name in node_names:
        try:
            node_info = Node(node_name, master)
            print("Node name: {}\nURI: {}\nXML-RPC URI: {}\nPublications: {}\nSubscriptions: {}\nServices: {}\n"
                  .format(node_name, node_info.uri, node_info.xmlrpc_uri, node_info.publications,
                          node_info.subscriptions, node_info.services))
        except:
            pass

#!/usr/bin/env python3
import rospy
import xmlrpc.client

def get_node_info(node_name):
    # Get the URI and PID of the node
    uri = xmlrpc.client.ServerProxy(rospy.get_master_uri()).lookupNode(node_name)
    pid = xmlrpc.client.ServerProxy(uri).getPid('/')

    return {'name': node_name, 'uri': uri, 'pid': pid}

if __name__ == '__main__':
    rospy.init_node('node_info')
    nodes = rospy.get_node_names()
    for node in nodes:
        info = get_node_info(node)
        print("Node: " + info['name'])
        print("  URI: " + info['uri'])
        print("  PID: " + str(info['pid']))

        # Get the topics that the node is publishing to
        pubs, _ = rospy.get_published_topics(node)
        print("  Published topics:")
        for topic, msg_type in pubs:
            print("    " + topic + " (" + msg_type + ")")

        # Get the topics that the node is subscribed to
        _, subs, _ = rospy.client.get_master().getSystemState()
        node_subs = [x[0] for x in subs if node in x[1]]
        print("  Subscribed topics:")
        for topic in node_subs:
            print("    " + topic)
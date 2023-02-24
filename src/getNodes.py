#!/usr/bin/env python3

import rospy
import rosnode
import re


def parsec(info):
# Extrai o nome do nó
    node_name = re.search(r"Node \[(.*)\]", info).group(1)

    # Extrai as publicações
    pubs = re.findall(r"\* (.*) \[(.*)\]", re.search(r"Publications:(.*)Subscriptions", info, re.DOTALL).group(1))
    publications = [{"topic": topic, "type": msg_type} for topic, msg_type in pubs]

    # Extrai as subscrições
    subs = re.findall(r"\* (.*) \[(.*)\]", re.search(r"Subscriptions:(.*)Services", info, re.DOTALL).group(1))
    subscriptions = [{"topic": topic, "type": msg_type} for topic, msg_type in subs]

    # Extrai os serviços
    services = re.findall(r"\* (.*)", re.search(r"Services:(.*)", info, re.DOTALL).group(1))

    return (node_name, publications, subscriptions, services)



if __name__ == '__main__':
    rospy.init_node('node_info')
    node_list = rosnode.get_node_names()
    # print(node_list)
    for node in node_list:
        print('-------------------------------------------------------')
        info = rosnode.get_node_info_description(node)
        print(parsec(info=info))
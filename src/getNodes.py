#!/usr/bin/env python3

from GlobalSets.Mongo import DataSource as Source, Clients, DataBases as db, Collections as col
from GlobalSets.localSave import createFile
from tcppinglib import tcpping

import rospy, bson, rosnode
import datetime
import re

dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase'  : db.dataLake,
    'collection': col.Nodes
}

class getNodes:
    def __init__(self) -> None:
        data = []
        _createFile = False
        rospy.init_node('getNodes', anonymous=False)
        while not rospy.is_shutdown():
            try:
                node_list = rosnode.get_node_names()
                for node in node_list:
                    info = rosnode.get_node_info_description(node)
                    
                    (node_name, publications, subscriptions, services) = self.parsec(info=info)
                    bnode = {
                        'node' : node_name,
                        'pubs' : publications,
                        'subs' : subscriptions,
                        'serv' : services
                    }
                    _node = list(filter(lambda x: x['node'] == node_name, data))
                    if _node == []:
                        data.append(bnode)
                        _createFile = True
                    elif _node[0] != bnode:
                        _node[0].update(bnode)
                        _createFile = True
                    else:
                        _createFile =False
                if _createFile: createFile(dataPath=dataPath, content=data) 
            except Exception as e:
                print(e)
    
    def parsec(self, info):
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
    try:
        getNodes()
    except rospy.ROSInterruptException:
        pass

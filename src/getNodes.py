#!/usr/bin/env python3

from GlobalSets.Mongo import DataSource as Source, Clients, DataBases as db, Collections as col
from GlobalSets.localSave import createFile
from tcppinglib import tcpping

import rospy, bson, rosnode, rosgraph
from datetime import datetime
import re

dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase'  : db.dataLake,
    'collection': col.Nodes
}

class getNodes:
    def __init__(self) -> None:
        data = []
        master = rosgraph.Master('/rosnode') 
        _createFile = False
        rospy.init_node('getNodes', anonymous=False)
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():  
            try:
                node_list = rosnode.get_node_names()
                for node in node_list:
                    node_api = rosnode.get_api_uri(master, node)
                    info = rosnode.get_node_connection_info_description(node_api, master)
                    # rosnode.rosnode_info(node)
                    (node_name, publications, subscriptions, services) = self.parsec(msg=info)
                    bnode = {
                        'node' : node_name,
                        'pubs' : publications,
                        'subs' : subscriptions,
                        'serv' : services
                    }
                    # print(bnode)
                    _node = list(filter(lambda x: x['node'] == node_name, data))
                    if _node == []:
                        data.append(bnode)
                        _createFile =True
                    elif _node[0] != bnode:
                        _node[0].update(bnode)
                        _createFile =True
                    else:
                        _createFile =False
                _data = {
                    'nodes': data, 
                    'dateTime': datetime.now()
                    }
                if _createFile: 
                    createFile(dataPath=dataPath, content=_data) 
                    print('create file')
            except Exception as e:
                print(e)
            
        rate.sleep()
    
    def parsec(self, msg):
        # Extrai o nome do nó
        node_name = re.search(r"Node \[(.*)\]", msg).group(1)
        print(msg)
        # Extrai as publicações
        pubs = re.findall(r"\* (.*) \[(.*)\]", re.search(r"Publications:(.*)Subscriptions", msg, re.DOTALL).group(1))
        publications = [{"topic": topic, "type": msg_type} for topic, msg_type in pubs]

        # Extrai as subscrições
        subs = re.findall(r"\* (.*) \[(.*)\]", re.search(r"Subscriptions:(.*)Services", msg, re.DOTALL).group(1))
        subscriptions = [{"topic": topic, "type": msg_type} for topic, msg_type in subs]

        # Extrai os serviços
        services = re.findall(r"\* (.*)", re.search(r"Services:(.*)", msg, re.DOTALL).group(1))

        return (node_name, publications, subscriptions, services)


if __name__ == '__main__':
    try:
        getNodes()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile
from GlobalSets.util import msg_to_document

# Import nodes.py
from nodes import NODES

# Import librarys
import rospy, bson
from datetime import datetime

class listenNodes:
    def __init__(self, NODES) -> None:
        rospy.init_node('listenNodes', anonymous=False)
        self.NODES = NODES
        for node in self.NODES:
            self.newSubscriber(node=node)
        rospy.spin()
               
    def newSubscriber(self, node):
        rospy.Subscriber(name='/' + node['node'], data_class=self['msg'], callback=self.callback, callback_args=(1))
        
    def callback(self, msg, args):
        print(args)
        try:
            data = msg_to_document(msg=msg)
            data.update({'dateTime': datetime.now()})
            ##
            print(data)
            ##
            createFile(dataPath=self.dataPath, content=data) 
        except Exception as e:
            print(e)
        self.rate.sleep()


if __name__ == '__main__':
    try:
        listenNodes(NODES=NODES)
    except rospy.ROSInterruptException:
        pass

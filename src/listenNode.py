#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile
from GlobalSets.util import msg_to_document

# Import nodes.py
from nodes import NODES

# Import librarys
import rospy, bson
from datetime import datetime

class listenNode:
    def __init__(self, Node_Name:str, Node_msg, dataPath:bson, rate:int = 1) -> None:
        self.Node_Name = Node_Name
        self.Node_msg = Node_msg
        self.dataPath = dataPath
        self.rate = rate
        try:
            self.init_node()
        except Exception as e:
            print(e)
               
    def init_node(self):
        rospy.init_node('get_' + self.Node_Name, anonymous=False)
        self.rate = rospy.Rate(self.rate)
        rospy.Subscriber('/' + self.Node_Name, self.Node_msg, self.callback)
        #rospy.spin()
        
    def callback(self, msg):
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
        activesNodes = []
        for node in NODES:
            try:
                listenNode(node['node'], node['msg'], node['dataPath'], node['rate'])
            except Exception as e:
                print(e)
    except rospy.ROSInterruptException:
        pass

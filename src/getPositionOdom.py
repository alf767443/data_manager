#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import DataSource as Source, Clients as MongoClient, DataBases as db, Collections as col
from GlobalSets.localSave import createFile, sendFile
from GlobalSets.util import msg_to_document

# Import librarys
import rospy, bson
from std_msgs.msg import String

# Import listner
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, PoseWithCovarianceStamped
from tf.transformations import euler_from_quaternion

## What is the database path
dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase': db.dbBuffer,
    'collection': col.PositionOdom
}

# To fake data
from random import random
from datetime import datetime

# rospy.init_node('getPositionOdom', anonymous=False)

# rospy.Subscriber('/odom', Odometry, self.callback)

# rospy.spin()

class listenNode:
    def __init__(self, Node_Name:str, Node_msg, dataPath:bson, rate:int = 1) -> None:
        self.Node_Name = Node_Name
        self.Node_msg = Node_msg
        self.dataPath = dataPath
        self.rate = rospy.Rate(rate)
        
        
    def init_node(self):
        rospy.init_node('get_' + self.Node_Name, anonymous=False)
        rospy.Subscriber('/' + self.Node_Name, self.Node_msg, self.callback)
        rospy.spin()

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
        listenNode('odom',Odometry,dataPath)
    except rospy.ROSInterruptException:
        pass


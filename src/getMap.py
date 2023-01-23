#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import DataSource as Source, Clients as MongoClient, DataBases as db, Collections as col
from GlobalSets.localSave import createFile, sendFile

# Import librarys
import rospy, bson, pymongo

# Import listner
from nav_msgs.msg import OccupancyGrid
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

class getPosition():
    lastRead = []

    def __init__(self) -> None:
        rospy.init_node('getPositionOdom', anonymous=False)

        rospy.Subscriber('/map', Map, self.callback)

        rospy.spin()

    def callback(self, msg):
        rate = rospy.Rate(1)

        
        print(self.lastRead)

        data = {
            'map': msg.data
        }

        ## Temporary debug
        print(data)
        try:
           ##createFile(dataPath=dataPath, content=data)
           rate.sleep()
        except Exception as e:
            createFile(dataPath=dataPath, content=data)
            print(e)


if __name__ == '__main__':
    try:
        getPosition()
    except rospy.ROSInterruptException:
        pass

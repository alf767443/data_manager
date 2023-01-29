#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import DataSource as Source, Clients as MongoClient, DataBases as db, Collections as col
from GlobalSets.localSave import createFile, sendFile
from GlobalSets.util import msg_to_document

# Import librarys
import rospy, bson, pymongo, json, yaml, datetime
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

def documentHandler(x):
    return None
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    else:
        raise TypeError(x)

class getPosition():
    
    def __init__(self) -> None:
        rospy.init_node('getPositionOdom', anonymous=False)

        rospy.Subscriber('/odom', Odometry, self.callback)

        rospy.spin()

    def callback(self, msg):
        m = msg
        print(m)
        print("-------------------------------------------------------------")
        m = msg_to_document(msg=msg)
        print(m)
        print("#############################################################")

        rate = rospy.Rate(1)
        rate.sleep()

    
    

if __name__ == '__main__':
    try:
        getPosition()
    except rospy.ROSInterruptException:
        pass


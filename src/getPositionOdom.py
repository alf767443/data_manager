#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import DataSource as Source, Clients as MongoClient, DataBases as db, Collections as col
from GlobalSets.localSave import createFile, sendFile

# Import librarys
import rospy, bson, pymongo
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

class getPosition():
    def __init__(self) -> None:
        rospy.init_node('getPositionOdom', anonymous=False)

        rospy.Subscriber('/odom', Odometry, self.callback)

        rate = rospy.Rate(1)
        rate.sleep()

        rospy.spin()

    def callback(self, msg):
        or_x = msg.pose.pose.orientation.x
        or_y = msg.pose.pose.orientation.y
        or_z = msg.pose.pose.orientation.z
        or_w = msg.pose.pose.orientation.w
        x    = msg.pose.pose.position.x
        y    = msg.pose.pose.position.y

        (raw, pitch, yaw) = euler_from_quaternion([or_x, or_y, or_z, or_w])
        data = {

                'x'     : x,
                'y'     : y,
                'orient': 
                {
                    'raw'   : raw,
                    'pitch' : pitch,
                    'yaw'   : yaw
                }
            }
        ## Temporary debug
        print(data)
        try:
            if not sendFile(Client=MongoClient.RemoteUnitClient, dataPath=dataPath, content=data):
                createFile(dataPath=dataPath, content=data)
            else:
                rate = rospy.Rate(1)
                rate.sleep()
        except Exception as e:
            createFile(dataPath=dataPath, content=data)
            print(e)


if __name__ == '__main__':
    try:
        getPosition()
    except rospy.ROSInterruptException:
        pass

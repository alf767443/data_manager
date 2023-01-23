#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import DataSource as Source, Clients as MongoClient, DataBases as db, Collections as col
from GlobalSets.localSave import createFile, sendFile

# Import librarys
import rospy, bson, pymongo
from std_msgs.msg import String

# Import listner
from sensor_msgs.msg import BatteryState

## What is the database path
dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase': db.dbBuffer, 
    'collection': col.Battery
}

# To fake data
from random import random
from datetime import datetime

class getBattery():
    def __init__(self) -> None:
        rospy.init_node('getBattery', anonymous=False)

        rospy.Subscriber('/battery_state', BatteryState, self.callback)

        rospy.spin()


    def callback(self, msg):
        rate = rospy.Rate(1)

        data = {
            'dateTime'      : datetime.now(),
            'voltage'       : msg.voltage,
            'current'       : msg.current,
            'percentage'    : msg.percentage
        }
        ## Temporary debug
        print(data)
        try:
            createFile(dataPath=dataPath, content=data)
            rate.sleep()
        except Exception as e:
            createFile(dataPath=dataPath, content=data)
            print(e)


if __name__ == '__main__':
    try:
        getBattery()
    except rospy.ROSInterruptException:
        pass

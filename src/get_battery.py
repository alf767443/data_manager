#!/usr/bin/env python3
# license removed for brevity

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col
from GlobalSets.SaveInLocal import localSave

import rospy, bson, pymongo
from std_msgs.msg import String

## What's the database?
database = MongoClient.LocalClient[db.dbBuffer][col.Battery]

# To fake data
from random import random

def get_battery():
    rospy.init_node('getBattery', anonymous=False)
    rate = rospy.Rate(10) # 10 Hz

    while not rospy.is_shutdown():
        
        ###############################
        # Fake data generator
        data = {
            "dateTime": rospy.get_rostime(),
            "Voltage": random()*15,
            "Current": random()*5,
            "Percent": random(),
            "Temperature": random()*100
        }
        ###############################

        localSave(database=database, data=data)

        
        


if __name__ == '__main__':
    try:
        get_battery()
    except rospy.ROSInterruptException:
        pass
#!/usr/bin/env python3
# license removed for brevity

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col
from GlobalSets.SaveInLocal import localSave

# Import librarys
import rospy, bson, pymongo
from std_msgs.msg import String

## What's the database?
database = MongoClient.LocalClient[db.dbBuffer][col.Position]

# To fake data
from random import random, randint
from datetime import datetime

def get_position():
    rospy.init_node('getPosition', anonymous=False)
    rate = rospy.Rate(1)



    while not rospy.is_shutdown():
        
        ###############################
        # Fake data generator
        data = {
            "dateTime"      : datetime.now(),
            "Global"        : {
                "X": randint(-5, 1000),
                "Y": randint(-5, 1000),
            },
            "Whell"      : {
                "Left"  : randint(),
                "Right" : randint()
            }
        }
        ###############################

        result = localSave(database=database, data=data)

        rospy.loginfo(str(result))
        rate.sleep()

        
if __name__ == '__main__':
    try:
        get_position()
    except rospy.ROSInterruptException:
        pass
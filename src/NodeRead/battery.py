#!/usr/bin/env python3
# license removed for brevity

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col

import rospy, bson
from std_msgs.msg import String


##
database = MongoClient.LocalClient[db.dbBuffer][col.Battery]

# To fake data
from random import random

def send2local():
    rospy.init_node('send2local', anonymous=False)
    rate = rospy.Rate(10)
    

    while not rospy.is_shutdown():
        database
        


def ReadBatteryData():
     ## Read data
        # By now just a fake data
    Voltage     = random()*15
    Current     = random()*2
    Temperature = random()*100
    # and others


    
    return data_bson

if __name__ == '__main__':
    try:
        up2cloud()
    except rospy.ROSInterruptException:
        pass
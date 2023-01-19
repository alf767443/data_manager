



#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col, log, delRandomItem, sizeOf
from GlobalSets.localSave import getFiles

import rospy
from std_msgs.msg import String


## What is the database path
dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase': db.dbBuffer, 
    'collection': col.Battery
}

# To fake data
from random import random
from datetime import datetime

class bufferManager():
    def __init__(self) -> None:
        rospy.init_node('bufferManager', anonymous=False)

        getFiles()

        rospy.spin()

if __name__ == '__main__':
    try:
        bufferManager()
    except rospy.ROSInterruptException:
        pass

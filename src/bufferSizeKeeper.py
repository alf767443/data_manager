#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col, log, delRandomItem, sizeOf
import GlobalSets.l2c_functions as l2c

import rospy
from std_msgs.msg import String

def bufferSizeKeeper():
    rospy.init_node('bufferSizeKeeper', anonymous=False)
    rate = rospy.Rate(1) # 10hz
    mongodb_databases = [MongoClient.LocalClient, MongoClient.CloudClient]
    while not rospy.is_shutdown():  
        for database in mongodb_databases:
            for collection in col.Collections:
                mongodb_collection = database[db.dbBuffer][collection['name']] 
                while sizeOf(mongodb_collection) > collection['maxBufferSize']:
                    try:
                        delRandomItem(mongodb_collection)
                    except:
                        pass            
        rate.sleep()

if __name__ == '__main__':
    try:
        bufferSizeKeeper()
    except rospy.ROSInterruptException:
        pass

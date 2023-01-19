#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col, log, delRandomItem, sizeOf
import GlobalSets.l2c_functions as l2c

import rospy
from std_msgs.msg import String

def bufferSizeManager_local():
    rospy.init_node('bufferSizeManager', anonymous=False)
    rate = rospy.Rate(1) 
    while not rospy.is_shutdown(): 
        try:
            mongodb_databases = [MongoClient.LocalClient]
        except Exception as e:
            eStr    = str(e)
            rospy.loginfo(eStr) 
            continue
        try: 
            for database in mongodb_databases:
                for collection in col.Collections:
                    mongodb_collection = database[db.dbBuffer][collection['name']] 
                    delTry = 0
                    while sizeOf(mongodb_collection) > collection['maxBufferSize'] and delTry < 50:
                        delTry += 1
                        try:
                            delRandomItem(mongodb_collection)
                        except Exception as e:
                            eStr    = str(e)
                            rospy.loginfo(eStr)
                            continue            
            rate.sleep()
        except Exception as e:
            eStr    = str(e)
            rospy.loginfo(eStr)
            continue

if __name__ == '__main__':
    try:
        bufferSizeManager_local()
    except rospy.ROSInterruptException:
        pass

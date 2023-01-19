# not used
#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col, log
import GlobalSets.l2c_functions as l2c

import rospy
from std_msgs.msg import String

# Import librarys
from pymongo import collection, errors
import bson

def local2cloud():
    rospy.init_node('local2cloud', anonymous=False)
    rate = rospy.Rate(1) 
    while not rospy.is_shutdown():   
        for collection in col.Collections:
            l2c.uploadBase(database=db.dbBuffer, collection=collection['name'])
        rate.sleep()

if __name__ == '__main__':
    try:
        local2cloud()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import DataSource as Source, Clients as MongoClient, DataBases as db, Collections as col
from GlobalSets.localSave import createFile

# Import librarys
import rospy, bson, pymongo
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

def get_battery():
    rospy.init_node('getBattery', anonymous=False)
    rate = rospy.Rate(1)



    while not rospy.is_shutdown():
        
        ###############################
        # Fake data generator
        data = {
            "dateTime"      : datetime.now(),
            "Voltage"       : random()*15,
            "Current"       : random()*5,
            "Percent"       : random(),
            "Temperature"   : random()*100
        }
        ###############################

        try:
            if not MongoClient.RemoteUnitClient[dataPath['dataBase']][dataPath['collection']].insert_one(data).acknowledged: 
                createFile(dataPath=dataPath, content=data)
        except Exception as e:
            createFile(dataPath=dataPath, content=data)
            print(e)
            
        rate.sleep()

        
if __name__ == '__main__':
    try:
        get_battery()
    except rospy.ROSInterruptException:
        pass
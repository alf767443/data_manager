#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import DataSource as Source, Clients as MongoClient, DataBases as db, Collections as col
from GlobalSets.localSave import createFile, sendFile

# Import librarys
import rospy, bson, pymongo
from std_msgs.msg import String

# Import listner
from ubiquity_motor.msg import MotorState

## What is the database path
dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase': db.dbBuffer, 
    'collection': col.Motor
}

# To fake data
from random import random
from datetime import datetime

class getBattery():
    def __init__(self) -> None:
        rospy.init_node('getMotors', anonymous=False)

        rospy.Subscriber('/motor_state', MotorState, self.callback)

        rospy.spin()


    def callback(self, msg):
        data = {
            'dateTime'      : datetime.now(),
            'left'          :
                {
                   'pos'    : msg.leftPosition,
                   'rrate'  : msg.leftRotateRate,
                   'current': msg.leftCurrent,
                   'PWM'    : msg.leftPwmDrive
                },
            'right'          :
                {
                   'pos'    : msg.rightPosition,
                   'rrate'  : msg.rightRotateRate,
                   'current': msg.rightCurrent,
                   'PWM'    : msg.rightPwmDrive
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
        getBattery()
    except rospy.ROSInterruptException:
        pass

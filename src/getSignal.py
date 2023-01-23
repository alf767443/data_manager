#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import DataSource as Source, Clients as MongoClient, DataBases as db, Collections as col
from GlobalSets.localSave import createFile, sendFile
from tcppinglib import tcpping
from datetime import datetime

# Import librarys
import rospy, bson, pymongo
from std_msgs.msg import String

# Import listner
from sensor_msgs.msg import BatteryState

## What is the database path
dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase': db.dbBuffer, 
    'collection': col.RUConection
}

class getSignal():
    def __init__(self) -> None:
        print('init')
        rospy.init_node('getSignal', anonymous=False)
        print('node')
        self.saveSignalRTT()
        rospy.spin()

    def getInfo(self, ip: str, port: int):
        try:
            ping = tcpping(address=ip, port=port, interval=1, timeout=2, count=5)
        except Exception as e:
            print(e)

        return(ping.is_alive, ping.avg_rtt)

    def saveSignalRTT(self):
        rate = rospy.Rate(1)
        try:
            (isAlive , RTT) = self.getInfo(ip=MongoClient.ip, port=MongoClient.port)
            data = {
                'dateTime': datetime.now(),
                'Connect': isAlive,
                'RTT': RTT
            }
            print(data)
            #MongoClient.LocalClient[db.dbBuffer][col.UGVconnec].insert_one(data)
        except Exception as e:
            print(e)
        rate.sleep()



if __name__ == '__main__':
    try:
        print(datetime.now(), 'Start get signal with UGV')
        getSignal()
        print(datetime.now(), 'Stop get signal with UGV')
    except Exception:
        print(datetime.now(), 'Stop get signal with UGV')
        pass


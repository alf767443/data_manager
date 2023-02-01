#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile
from GlobalSets.util import msg_to_document

import pymongo, bson, datetime, rospy
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col


pipeline = {
    'Status_0|1' : [
        {
            '$match': {
                'status': {
                    '$lte': 1
                }
            }
        }, {
            '$sort': {
                'dateTime': -1
            }
        }
    ]
}


class listenNodes:
    queue = []

    def __init__(self) -> None:
        rospy.init_node('queueActions', anonymous=False)
        self.getFromRemoteUnit()
        rospy.spin()
                       
    def getFromRemoteUnit(self):
        actionsQueue = list(MongoClient.RemoteUnitClient[db.dataLake]['Actions'].aggregate(pipeline=pipeline['Status_0|1']))
        for new in actionsQueue:
            print(new)
        print(actionsQueue)
        rate = rospy.Rate(1)
        rate.sleep()


if __name__ == '__main__':
    try:
        listenNodes()
    except rospy.ROSInterruptException:
        pass

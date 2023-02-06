#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile
from GlobalSets.util import msg_to_document

import pymongo, bson, datetime, rospy, os, json
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
        for action in self.queue:
            self.runAction(action[0])
        rate = rospy.Rate(1)
        rate.sleep()
        rospy.spin()
                       
    def getFromRemoteUnit(self):
        actionsQueue = list(MongoClient.RemoteUnitClient[db.dataLake]['Actions'].aggregate(pipeline=pipeline['Status_0|1']))
        # print(actionsQueue)
        for actual in self.queue:
            print(actionsQueue.pop(actual))
        self.queue.append(actionsQueue)
        # print(self.queue)
        
        

    def runAction(self, action):
        print(action)
        print('topic:   ', action['topic'])
        print('msg:     ', action['msg'])
        print('command: ', action['command'])
        # command = "rostopic pub {} {} {}".format(str(action['topic']), str(action['msg']), str(action['command']))
        command = json.dumps(action['command'], indent=1)
        command = command.replace('{','').replace('}','').replace('"', '')
        print(command)
        # command.replace('{','').replace('}','')
        command = "rostopic pub " + action['topic'] + ' '+ action['msg'] + ' "' + command + '"'
        print(command)
        # os.system(command)

        

if __name__ == '__main__':
    try:
        listenNodes()
    except rospy.ROSInterruptException:
        pass

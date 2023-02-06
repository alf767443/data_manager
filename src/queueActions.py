#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile, updateMany
from GlobalSets.util import msg_to_document

import pymongo, bson, datetime, rospy, os, json, subprocess
from GlobalSets.Mongo import Source, Clients as MongoClient, DataBases as db, Collections as col


pipeline = {
    'Status_0|1' : [
        {
            '$match': {
                'status': {
                    '$lt': 1
                }
            }
        }, {
            '$sort': {
                'dateTime': -1
            }
        }
    ]
}

dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase'  : db.dataLake,
    'collection': col.Actions
}

class listenNodes:
    queue = []

    def __init__(self) -> None:
        rospy.init_node('queueActions', anonymous=False)
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            self.getFromRemoteUnit()
            for action in self.queue:
                # Action run ok
                if self.runAction(action):
                    print(action)
                    action.update({'status': 1})
                # Action failed
                else:
                    print(action)
                    action.update({'status': 2})
                updateMany(Client = MongoClient.RemoteUnitClient, dataPath = dataPath, content = self.queue )
            print(self.queue)
            
            rate.sleep()
        rospy.spin()
                       
    def getFromRemoteUnit(self):
        actionsQueue = list(MongoClient.RemoteUnitClient[db.dataLake]['Actions'].aggregate(pipeline=pipeline['Status_0|1']))
        # print(actionsQueue)
        for actual in self.queue:
            print(actionsQueue.pop(actual))
        for actual in actionsQueue:
            self.queue.append(actual)
        # print(self.queue)
        

    def runAction(self, action):
        # print(action)
        # print('topic:   ', action['topic'])
        # print('msg:     ', action['msg'])
        # print('command: ', action['command'])
        # command = "rostopic pub {} {} {}".format(str(action['topic']), str(action['msg']), str(action['command']))
        command = json.dumps(action['command'], indent=1)
        command = command.replace('{','').replace('}','').replace('"', '').replace(',','\n')
        print(command)
        # command.replace('{','').replace('}','')
        command = "rostopic pub -1 " + action['topic'] + ' '+ action['msg'] + ' "' + command + '"'
        try:
            result = subprocess.call(command, shell=True)
            return True   
        except Exception as e:
            print(e)
            return False
        

        

if __name__ == '__main__':
    try:
        listenNodes()
    except rospy.ROSInterruptException:
        pass

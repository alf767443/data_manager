#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile, updateMany
from GlobalSets.util import msg_to_document

import pymongo, bson, datetime, rospy, os, json, subprocess
from GlobalSets.Mongo import DataSource as Source, Clients as MongoClient, DataBases as db, Collections as col


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
            for action in list(filter(lambda d: d['status'] in [0], self.queue)):
                # Action run ok
                if self.runAction(action):
                    # print(action)
                    action.update({'status': 0})
                # Action failed
                else:
                    # print(action)
                    action.update({'status': 0})
            # print(self.queue)
            updateMany(Client = MongoClient.RemoteUnitClient, dataPath = dataPath, content = self.queue)     
            rate.sleep()
        rospy.spin()
                       
    def getFromRemoteUnit(self):
        actionsQueue = list(MongoClient.RemoteUnitClient[db.dataLake]['Actions'].aggregate(pipeline=pipeline['Status_0|1']))
        self.queue = actionsQueue


        # _ID from local queue
        _id = [action['_id'] for action in self.queue]
        remoteIDs = list(MongoClient.RemoteUnitClient[db.dataLake]['Actions'].find({'_id': _id}))

        print(_id, remoteIDs)


        



        
        print(self.queue)
        #print(_id)

            

        
        
    def runAction(self, action):
        command = json.dumps(action['command'], indent=1)
        command = command.replace('{','').replace('}','').replace('"', '').replace(',','\n')
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

#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile, updateMany
from GlobalSets.util import msg_to_document

import pymongo, bson, datetime, rospy, os, json, subprocess
from GlobalSets.Mongo import DataSource as Source, Clients as MongoClient, DataBases as db, Collections as col
from std_msgs.msg import String

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

        rospy.Subscriber("queue", String, self.queueCallback)
        
        rate = rospy.Rate(1)
        self.initialQuery()
        while not rospy.is_shutdown():
            self.getFromRemoteUnit()
            for action in list(filter(lambda d: d['status'] in [0], self.queue)):
                # Action run ok
                if self.runAction(action):
                    # print(action)
                    action.update({'status': 1})
                # Action failed
                else:
                    # print(action)
                    action.update({'status': 0})

            rate.sleep()

    def queueCallback(self, msg):
        data = msg.data
        data = json.loads(data)
        try:
            data['command']
            data['msg']
            data['topic']
            data['priority']
            data.update({'dateTime': datetime.datetime.now()})
            self.queue.append(data)
            
        except Exception as e:
            print(e)
            pass
        
    def initialQuery(self):
        remoteQueue = list(MongoClient.RemoteUnitClient[db.dataLake]['Actions'].find())
        # remote = next(remote for remote in remoteQueue)
        for item in remoteQueue:
            # if item != []:
            while not MongoClient.RemoteUnitClient[db.dataLake]['Actions'].update_one({'_id': item['_id']}, {'$set': {'status': 3}}).acknowledged:
                rospy.sleep(1)
                       
    def getFromRemoteUnit(self):
        # _ID from local queue
        _id = [action['_id'] for action in self.queue]
        remoteQueue = list(MongoClient.RemoteUnitClient[db.dataLake]['Actions'].find({'_id': {'$in' : _id} }))

        print('=============================')
        print("Local  queue: ",self.queue)
        print("Remote queue: ",remoteQueue)

        # Run in all local queue
        for local in self.queue:
            remote = next(remote for remote in remoteQueue if remote['_id'] == local['_id'])
            if remote != []:
                if local['status'] == 1:
                    MongoClient.RemoteUnitClient[db.dataLake]['Actions'].update_one({'_id': remote['_id']}, {'$set': {'status': 1}})
                    self.queue.remove(remote) 
                else:
                    remoteQueue.remove(remote)
                    self.queue.remove(remote)        
            # Local not found in remote
            else:
                local.update({'_id': MongoClient.RemoteUnitClient[db.dataLake]['Actions'].insert_one(local).inserted_id})

        # Append remote in local
        actionsQueue = list(MongoClient.RemoteUnitClient[db.dataLake]['Actions'].aggregate(pipeline=pipeline['Status_0|1']))
        for new in actionsQueue:
            self.queue.append(new)    
        
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

    def sortQueue(self, key):
        temp = []
        #Sort
        self.queue = sorted(self.queue, key=lambda d: d[key])
        #Remove duplicates
        for i in range(len(self.queue)):
            if self.queue[i] not in self.queue[i + 1:]:
                temp.append(self.queue[i])
            else:
                MongoClient.RemoteUnitClient[db.dataLake]['Actions'].update_one({'_id': self.queue[i]['_id']}, {'$set': {'status': 3}})
        i = 1
        #Remove commands duplicates
        while i < len(temp):
            if temp[i]['command'] == temp[i-1]['command']:
                temp.pop(i)
                MongoClient.RemoteUnitClient[db.dataLake]['Actions'].update_one({'_id': temp['_id']}, {'$set': {'status': 3}})
            else:
                i = i + 1
        self.queue = temp

if __name__ == '__main__':
    try:
        listenNodes()
    except rospy.ROSInterruptException:
        pass

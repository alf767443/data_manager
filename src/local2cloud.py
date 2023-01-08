#!/usr/bin/env python3
# license removed for brevity

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col, log

import rospy
from std_msgs.msg import String

# Import librarys
from pymongo import collection, errors
import bson

def local2cloud():
    rospy.init_node('local2cloud', anonymous=True)
    rate = rospy.Rate(1) # 10hz

    while not rospy.is_shutdown():   
        for collection in col.Collections:
            uploadBase(database=db.dbBuffer, collection=collection)
        rate.sleep()

if __name__ == '__main__':
    try:
        local2cloud()
    except rospy.ROSInterruptException:
        pass

def uploadElement(document: dict, local: collection.Collection, cloud: collection.Collection):
    try:
        if local.insert_one(document).acknowledged:
            cloud.delete_one(document)
    except errors.DuplicateKeyError:
        cloud.delete_one(document)
    except Exception as e:
        eStr = str(e)
        log.insert_one(eStr)
        print(eStr)  

def uploadBase(database: str, collection: str):
    local = MongoClient.LocalClient[database][collection]
    cloud = MongoClient.CloudClient[database][collection]
    try:
        if MongoClient.CloudClient.is_primary and local.count_documents(filter={}):
                documents = local.aggregate([
                    {
                        '$sort': {
                            'dateTime': -1
                        }
                    },
                    {
                        '$limit': 100
                    }
                ])
                while documents._has_next():
                    uploadElement(document=documents.next(), local=local, cloud=cloud)
                       
    except Exception as e:
        eStr = str(e)
        log.insert_one(eStr)
        print(eStr)
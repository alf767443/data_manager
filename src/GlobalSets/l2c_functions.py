# not used
#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col, log

import rospy
from std_msgs.msg import String

# Import librarys
from pymongo import collection, errors
import bson

def uploadElement(document: dict, local: collection.Collection, cloud: collection.Collection):
    try:
        for upTry in range(0,5):
            if MongoClient.CloudClient.is_primary and cloud.insert_one(document).acknowledged:
                local.delete_one(document)
                break
    except errors.DuplicateKeyError:
        local.delete_one(document)
    except Exception as e:
        eStr = str(e)
        rospy.loginfo(eStr)  

def uploadBase(database: str, collection: str):
    try:
        local = MongoClient.LocalClient[database][collection]
    except Exception as e:
        eStr = str(e)
        rospy.loginfo(eStr)
        return
    try:
        cloud = MongoClient.CloudClient[database][collection]
    except Exception as e:
        return

    try:
        if MongoClient.CloudClient.is_primary and local.count_documents(filter={}) > 0:
            documents = local.aggregate([
                {
                    '$sort': {
                        'dateTime': -1
                    }
                },
                {
                    '$limit': 1000
                }
            ])
            while documents._has_next():
                uploadElement(document=documents.next(), local=local, cloud=cloud)
                       
    except Exception as e:
        eStr = str(e)
        rospy.loginfo(eStr)
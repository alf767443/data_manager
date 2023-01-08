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
        if local.insert_one(document).acknowledged:
            cloud.delete_one(document)
    except errors.DuplicateKeyError:
        cloud.delete_one(document)
    except Exception as e:
        eStr = str(e)
        log.insert_one(eStr)
        print(eStr)  

def uploadBase(database: str, collection: str):
    try:
        local = MongoClient.LocalClient[database][collection]
        cloud = MongoClient.CloudClient[database][collection]
    except:
        return
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
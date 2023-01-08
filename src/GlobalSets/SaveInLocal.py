#!/usr/bin/env python3
# license removed for brevity

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col, log

# Import librarys
from pymongo import collection
import bson

def localSave(database: collection.Collection, data: bson):
    try:
        result = database.insert_one(data)
    except Exception as e:
        eStr = str(e)
        result =  log.insert_one(eStr)
        print(eStr)
    return result


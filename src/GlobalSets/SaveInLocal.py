#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col, log, sizeOf

# Import librarys
from pymongo import collection
import bson

def localSave(database: collection.Collection, data: bson):
    try:
        sizeOf(database=database)
        result  = database.insert_one(data)
    except Exception as e:
        eStr    = str(e)
        result  =  log(eStr)
        print(eStr)
    return result


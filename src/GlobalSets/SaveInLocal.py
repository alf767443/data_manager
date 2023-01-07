#!/usr/bin/env python3
# license removed for brevity

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col

# Import librarys
import pymongo, json, bson

def localSave(database: pymongo, data: bson):
    print(database.InsertOne(data))

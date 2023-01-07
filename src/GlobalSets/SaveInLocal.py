#!/usr/bin/env python3
# license removed for brevity

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col

# Import librarys
from pymongo import collection
import bson

def localSave(database: collection.Collection, data: bson):
    result = database.insert_one(data)

    return result


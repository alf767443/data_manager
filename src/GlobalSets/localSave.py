#!/usr/bin/env python3

import json, datetime, bson, os, random, pymongo
import GlobalSets.Mongo as Mongo

## Create the path
path =  os.path.expanduser('~')+'/UGV_tempData/'

def createFile(dataPath: bson, content: bson):
    try:
        ## Check if dataPath is valid
        test = dataPath['dataSource']
        test = dataPath['dataBase']
        test = dataPath['collection']
        # Create data string
        data = bson.encode(document={'dataPath': dataPath, 'content': content})
        ## Create the file name
        fileName =  datetime.datetime.strftime(datetime.datetime.now(),"%Y%m%d%H%M%S_%f")
        ## Define the extension
        extencion = '.cjson'
        ## Create the extension
        fullPath = path+fileName+extencion
        # Create directory if it don't exist
        if not os.path.exists(path=path):
            os.chmod
            os.makedirs(name=path)
        # Create file
        file = open(file=fullPath, mode='a')
        file = open(file=fullPath, mode='wb')
        # Fill file
        file.write(data)
        file.close()
        return file
    except Exception as e:
        print(e)
        return(False)

def getFiles():
    ## Get files
    files = sorted(os.listdir(path=path), reverse=True)
    ## Read files
    try:
        while Mongo.Clients.RemoteUnitClient.is_primary and len(files) > 0:
            for file in files:
                ## Read file
                get = open(file=path+file, mode='rb')
                data = bson.BSON.decode(get.read())
                dataPath = data['dataPath']
                content = data['content']
                ## Send to Remote Unit
                if Mongo.Clients.RemoteUnitClient[dataPath['dataBase']][dataPath['collection']].insert_one(content).acknowledged:
                    get.close()
                    if os.path.exists(path=path+file):
                        os.remove(path+file)
            files = sorted(os.listdir(path=path), reverse=True)
    except Exception as e:
        print(e)
        return False
    return True

def sendFile(Client: pymongo.MongoClient, dataPath: bson, content: bson):
    try:
        ## Check if dataPath is valid
        dataSource = dataPath['dataSource']
        dataBase = dataPath['dataBase']
        collection = dataPath['collection']
        return Client[dataBase][collection].insert_one(content).acknowledged
    except Exception as e:
        return False
import pymongo
from pymongo import collection
from datetime import datetime

# ---------------------------------------------------
# CLIENTS
class Clients:
    # Local Client
    try:
        LocalClient = pymongo.MongoClient('mongodb://localhost:27017/')
    except:
        pass

    # Cloud Client
    try:
        CloudClient = pymongo.MongoClient("mongodb+srv://Admin:admin@cedri.hfunart.mongodb.net/?retryWrites=true&w=majority")
    except:
        pass

# ---------------------------------------------------
# DATABASES
class DataBases:
    # Cloud dashboard database
    dbDashboard = 'CeDRI_UGV_dashboard'

    # Cloud buffer
    dbBuffer    = 'CeDRI_UGV_buffer'

# ---------------------------------------------------
# COLLECTIONS
class Collections:
    # Collection battery
    Battery     = 'Battery_Data'

    # Collection position
    Position    = 'Position_Data'

    # Collection log
    Log         = 'Log'

    #
    Collections = [
        {
            'name'              : Battery,
            'maxBufferSize'     : 2e6,      #bytes
            'maxDashboardSize'  : 100       #Itens
        },
        {
            'name'              : Position,
            'maxBufferSize'     : 2e6,      #bytes
            'maxDashboardSize'  : 100       #Itens
        },
        {
            'name'              : Log,
            'maxBufferSize'     : 2e6,      #bytes
            'maxDashboardSize'  : 100       #Itens
        }
    ]

# ---------------------------------------------------
# FUNCTIONS
# Log
def log(logData:str):
    try:
        Clients.LocalClient[DataBases.dbDashboard][Collections.Log].insert_one({
            "dateTime": datetime.now(),
            "log": logData 
        })
    except:
        pass

# Size of a collection
def sizeOf(database: collection.Collection):
    aggreation =  [
        {
            '$collStats': {
                'storageStats': {}
            }
        }
    ]
    result = database.aggregate(aggreation)
    return list(result)[0]['storageStats']['storageSize']

# Delete a random item
def delRandomItem(database: collection.Collection):
    aggreation = [
        {
            '$sample': {
                'size': 1
            }
        }
    ]
    result =  database.aggregate(aggreation)
    while result._has_next():
            temp = result.next()
            try:
                database.delete_one(temp).deleted_count
            except Exception as e:
                eStr    = str(e)
                result  =  log(eStr)
                print(eStr)

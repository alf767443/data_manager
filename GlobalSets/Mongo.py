import pymongo, rospy
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

    # Cloud Client
    try:
        RemoteUnitClient = pymongo.MongoClient('mongodb://194.210.89.81:27017/')
    except:
        pass

# ---------------------------------------------------
# DATASOURCE
class DataSource:
    # CeDRI UGV datasource
    CeDRI_UGV = 'CeDRI_UGV'

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
    Battery         = 'Battery_Data'

    # Collection position odometry
    PositionOdom    = 'PositionOdom_Data'

    # Collection position amcl
    PositionAMCL    = 'PositionAMCL_Data'

    # Collection position
    Motor           = 'Motor_Data'

    # Collection log
    Log             = 'Log'

    #
    Collections = [
        {
            'name'              : Battery,
            'maxBufferSize'     : 2e5,      #bytes
            'maxBufferCloud'    : 1e5,      #bytes
            'maxDashboardSize'  : 100       #Itens
        },
        {
            'name'              : PositionOdom,
            'maxBufferSize'     : 2e5,      #bytes
            'maxBufferCloud'    : 1e5,      #bytes
            'maxDashboardSize'  : 100       #Itens
        },
        {
            'name'              : PositionAMCL,
            'maxBufferSize'     : 2e5,      #bytes
            'maxBufferCloud'    : 1e5,      #bytes
            'maxDashboardSize'  : 100       #Itens
        },
        {
            'name'              : Motor,
            'maxBufferSize'     : 2e5,      #bytes
            'maxBufferCloud'    : 1e5,      #bytes
            'maxDashboardSize'  : 100       #Itens
        },
        {
            'name'              : Log,
            'maxBufferSize'     : 1e2,      #bytes
            'maxBufferCloud'    : 1e2,      #bytes
            'maxDashboardSize'  : 100       #Itens
        }
    ]

# ---------------------------------------------------
# FUNCTIONS
# Log
def log(logData:str):
    try:
        Clients.LocalClient[DataBases.dbBuffer][Collections.Log].insert_one({
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
    try:
        result = database.aggregate(aggreation)
        result = list(result)[0]['storageStats']['size']
    except Exception as e:
                eStr    = str(e)
                rospy.loginfo(eStr)
    return result

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
                rospy.loginfo(eStr)

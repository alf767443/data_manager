import pymongo


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
    Collections = [Battery, Position, Log]

try:
    log = Clients.LocalClient[DataBases.dbDashboard][Collections.Log]
except:
    pass
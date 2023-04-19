import os, pymongo

#============ Storage ============#
PATH = os.path.expanduser('~')+'/UGV_tempData/'

#============ Mongo ============#
DATALAKE = "datalake_UGV_Magni_debug"
DATASOURCE = "CeDRI_robots"
CLIENT = pymongo.MongoClient('mongodb://192.168.217.183:27017/', 
                             connectTimeoutMS = 1000, 
                             serverSelectionTimeoutMS = 1000, 
                             socketTimeoutMS = 1000)
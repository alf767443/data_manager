import json, datetime, bson, os, random
import Mongo

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
    for file in files:
        get = open(file=path+file, mode='rb')
        data = bson.BSON.decode(get.read())
        print(data['dataPath'])
        print(data['content'])
        print(file)
        get.close()
        if os.path.exists(path=path+file):
            os.remove(path+file)
            #print(1)
    return True



data = {
            "dateTime"      : datetime.datetime.now(),
            "Voltage"       : random.random()*15,
            "Current"       : random.random()*5,
            "Percent"       : random.random(),
            "Temperature"   : random.random()*100
        }

createFile({'dataSource': 'CeDRI_UGV', 'dataBase': 'CeDRI_UGV_buffer', 'collection': 'Battery_Data'},content=data)
getFiles()
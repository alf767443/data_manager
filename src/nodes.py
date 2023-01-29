# Global imports
from GlobalSets.Mongo import DataSource as Source, DataBases as db, Collections as col

# Messages
from nav_msgs.msg import Odometry


NODES = [
    #############################################################
    # {
    #     'node'    : --The node address (odom),
    #     'msg'     : --The type of message
    #     'rate'    : --Listen rate
    #     'dataPath': {
    #         'dataSource': --Name of data source in MongoDB
    #         'dataBase'  : --Name of data base in MongoDB
    #         'collection': --Name of collection in MongoDB
    #     }
    # }
    #############################################################
    
    # Odometry
    {
        'node'    : 'odom',
        'msg'     : Odometry,
        'rate'    : 1,
        'dataPath': {
            'dataSource': Source.CeDRI_UGV, 
            'dataBase'  : db.dbBuffer,
            'collection': col.PositionOdom
        }
    }, {
        'node'    : 'odom',
        'msg'     : Odometry,
        'rate'    : 1,
        'dataPath': {
            'dataSource': Source.CeDRI_UGV, 
            'dataBase'  : db.dbBuffer,
            'collection': col.PositionOdom
        }
    }
]

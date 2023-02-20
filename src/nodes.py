# Global imports
from GlobalSets.Mongo import DataSource as Source, DataBases as db, Collections as col

# Messages
from nav_msgs.msg import Odometry
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import BatteryState
from geometry_msgs.msg import PoseWithCovarianceStamped
from ubiquity_motor.msg import MotorState

from diagnostic_msgs.msg import DiagnosticArray
from dynamic_reconfigure.msg import ConfigDescription



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
        'q2e'     : True,
        'dataPath': {
            'dataSource': Source.CeDRI_UGV, 
            'dataBase'  : db.dataLake,
            'collection': col.PositionOdom
        }
    }, 
    # LiDAR
    # {
    #     'node'    : 'scan',
    #     'msg'     : LaserScan,
    #     'rate'    : 1,
    #     'q2e'     : False,
    #     'dataPath': {
    #         'dataSource': Source.CeDRI_UGV, 
    #         'dataBase'  : db.dataLake,
    #         'collection': col.LiDAR
    #     }
    # }, 
    # AMCL_pos
    {
        'node'    : 'amcl_pose',
        'msg'     : PoseWithCovarianceStamped,
        'rate'    : 1,
        'q2e'     : True,
        'dataPath': {
            'dataSource': Source.CeDRI_UGV, 
            'dataBase'  : db.dataLake,
            'collection': col.PositionAMCL
        }
    }, 
    # Motor state
    {
        'node'    : 'motor_state',
        'msg'     : MotorState,
        'rate'    : 1,
        'q2e'     : False,
        'dataPath': {
            'dataSource': Source.CeDRI_UGV, 
            'dataBase'  : db.dataLake,
            'collection': col.Motor
        }
    }, 
    # # Occupancy map
    # {
    #     'node'    : 'map',
    #     'msg'     : OccupancyGrid,
    #     'rate'    : 1,
    #     'q2e'     : False,
    #     'dataPath': {
    #         'dataSource': Source.CeDRI_UGV, 
    #         'dataBase'  : db.dataLake,
    #         'collection': col.Occupancy
    #     }
    # },
    # Battery
    {
        'node'    : 'battery_state',
        'msg'     : BatteryState,
        'rate'    : 1,
        'q2e'     : False,
        'dataPath': {
            'dataSource': Source.CeDRI_UGV, 
            'dataBase'  : db.dataLake,
            'collection': col.Battery
        }
    }, 
    
]


DIAGNOSTICS_NODES = [
    # {
    #     'node'    : --The node address (diagnostics),
    #     'msg'     : --The type of message
    #     'rate'    : --Listen rate
    #     'dataPath': {
    #         'dataSource': --Name of data source in MongoDB
    #         'dataBase'  : --Name of data base in MongoDB
    #         'collection': --Name of collection in MongoDB
    #     }
    # }
    {
        'node'    : 'diagnostics',
        'msg'     : DiagnosticArray,
        'rate'    : 1,
        'dataPath': {
            'dataSource': Source.CeDRI_UGV, 
            'dataBase'  : db.dataLake,
            'collection': col.Diagnostics
        }
    }, 
    # {
    #     'node'    : 'diagnostics_agg',
    #     'msg'     : DiagnosticArray,
    #     'rate'    : 1,
    #     'dataPath': {
    #         'dataSource': Source.CeDRI_UGV, 
    #         'dataBase'  : db.dataLake,
    #         'collection': col.Diagnostics
    #     }
    # }, 
    # {
    #     'node'    : 'motor_node/parameter_descriptions',
    #     'msg'     : ConfigDescription,
    #     'rate'    : 1,
    #     'dataPath': {
    #         'dataSource': Source.CeDRI_UGV, 
    #         'dataBase'  : db.dataLake,
    #         'collection': col.Diagnostics
    #     }
    # }, 
    # {
    #     'node'    : 'ubiquity_velocity_controller/parameter_descriptions',
    #     'msg'     : ConfigDescription,
    #     'rate'    : 1,
    #     'dataPath': {
    #         'dataSource': Source.CeDRI_UGV, 
    #         'dataBase'  : db.dataLake,
    #         'collection': col.Diagnostics
    #     }
    # }, 
    # {
    #     'node'    : 'urg_node/parameter_descriptions',
    #     'msg'     : ConfigDescription,
    #     'rate'    : 1,
    #     'dataPath': {
    #         'dataSource': Source.CeDRI_UGV, 
    #         'dataBase'  : db.dataLake,
    #         'collection': col.Diagnostics
    #     }
    # }, 
]
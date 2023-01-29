#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import DataSource as Source, Clients as MongoClient, DataBases as db, Collections as col
from GlobalSets.localSave import createFile, sendFile

# Import librarys
import rospy, bson, pymongo, json, yaml, datetime
from std_msgs.msg import String

# Import listner
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, PoseWithCovarianceStamped
from tf.transformations import euler_from_quaternion

## What is the database path
dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase': db.dbBuffer,
    'collection': col.PositionOdom
}

# To fake data
from random import random
from datetime import datetime

def documentHandler(x):
    return None
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    else:
        raise TypeError(x)

class getPosition():
    def __init__(self) -> None:
        rospy.init_node('getPositionOdom', anonymous=False)

        rospy.Subscriber('/odom', Odometry, self.callback)

        rospy.spin()

    def callback(self, msg):
        m = msg
        print(m)
        print("-------------------------------------------------------------")
        m = msg_to_document(msg=msg)
        print(m)
        print("#############################################################")

        rate = rospy.Rate(1)
        rate.sleep()

    
    def msg_to_document(msg):
        """
        Given a ROS message, turn it into a (nested) dictionary suitable for the datacentre.
        >>> from geometry_msgs.msg import Pose
        >>> msg_to_document(Pose())
        {'orientation': {'w': 0.0, 'x': 0.0, 'y': 0.0, 'z': 0.0},
        'position': {'x': 0.0, 'y': 0.0, 'z': 0.0}}
        :Args:
            | msg (ROS Message): An instance of a ROS message to convert
        :Returns:
            | dict : A dictionary representation of the supplied message.
        """




        d = {}

        slot_types = []
        if hasattr(msg,'_slot_types'):
            slot_types = msg._slot_types
        else:
            slot_types = [None] * len(msg.__slots__)


        for (attr, type) in zip(msg.__slots__, slot_types):
            d[attr] = sanitize_value(attr, getattr(msg, attr), type)

        return d


    def sanitize_value(attr, v, type):
        """
        De-rosify a msg.
        Internal function used to convert ROS messages into dictionaries of pymongo insertable
        values.
        :Args:
            | attr(str): the ROS message slot name the value came from
            | v: the value from the message's slot to make into a MongoDB able type
            | type (str): The ROS type of the value passed, as given by the ressage slot_types member.
        :Returns:
            | A sanitized version of v.
        """

            # print '---'
            # print attr
            # print v.__class__
            # print type
            # print v

        if isinstance(v, str):
            if type == 'uint8[]':
                v = Binary(v)
            else:
                # ensure unicode
                try:
                    if _PY3:
                        v = str(v, "utf-8")
                    else:
                        v = unicode(v, "utf-8")
                except UnicodeDecodeError as e:
                    # at this point we can deal with the encoding, so treat it as binary
                    v = Binary(v)
            # no need to carry on with the other type checks below
            return v

        if isinstance(v, rospy.Message):
            return msg_to_document(v)
        elif isinstance(v, genpy.rostime.Time):
            return msg_to_document(v)
        elif isinstance(v, genpy.rostime.Duration):
            return msg_to_document(v)
        elif isinstance(v, list):
            result = []
            for t in v:
                if hasattr(t, '_type'):
                    result.append(sanitize_value(None, t, t._type))
                else:
                    result.append(sanitize_value(None, t, None))
            return result
        else:
            return v

if __name__ == '__main__':
    try:
        getPosition()
    except rospy.ROSInterruptException:
        pass


#!/usr/bin/env python3
# license removed for brevity

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col

import rospy, pymongo
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        teste = {
            "first": 1,
            "second": 'a'
        }
        result = MongoClient.LocalClient[db.dbBuffer][col.Battery].insert_one(teste)
        
        rospy.loginfo(str(result))
        pub.publish(str(result))
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
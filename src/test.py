#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

posQueue = []

def callback(msg):
    data = msg.data
    _temp = None
    print(data, _temp, posQueue)
    if posQueue != []:
        _temp = posQueue.copy().pop()
        print(_temp)
        return None
    if data != _temp:
        posQueue.append(data)
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", posQueue)
    
def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
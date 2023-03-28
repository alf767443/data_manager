#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile
from sensor_msgs.msg import BatteryState

# Import librarys
import rospy, bson, psutil
from datetime import datetime



class test:
    def __init__(self) -> None:
        rospy.init_node('testNode', anonymous=False)
        rospy.Subscriber(name='/battery_state', data_class=BatteryState, callback=self.callback, queue_size=1)
        
        rospy.spin()
            
    def callback(self, msg):
        rate = rospy.Rate(1)

        if msg.voltage < 0.3:
            print('hello')
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        test()
    except rospy.ROSInterruptException:
        pass

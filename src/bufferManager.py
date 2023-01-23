#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import getFiles

import rospy
class bufferManager():
    def __init__(self) -> None:
        rospy.init_node('bufferManager', anonymous=False)
        rate = rospy.Rate(1)
        
        while not rospy.is_shutdown():
            print(getFiles(), end='\r')
            rate.sleep() 

if __name__ == '__main__':
    try:
        print("Is sync?")
        bufferManager()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import getFiles

import rospy
class bufferManager():
    def __init__(self) -> None:
        rospy.init_node('bufferManager', anonymous=False)

        print(getFiles(), end='\r')

        rospy.spin()

if __name__ == '__main__':
    try:
        print("Is sync?")
        bufferManager()
    except rospy.ROSInterruptException:
        pass

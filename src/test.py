#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

class test:
    posQueue = []

    def __init__(self) -> None:
        rospy.init_node('listener', anonymous=True)

        rospy.Subscriber("chatter", String, self.callback)

        
            
    def callback(self, msg):
        data = msg.data
        _temp = None
        print(data, _temp, self.posQueue)
        if self.posQueue != []:
            _temp = self.posQueue.copy()
            print(_temp)
            _temp = _temp.pop()
            print(_temp)
            # return None
        if data !=  _temp:
            self.posQueue.append(data)
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", self.posQueue)

if __name__ == '__main__':
    try:
        test()
    except rospy.ROSInterruptException:
        pass

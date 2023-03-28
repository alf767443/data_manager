#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile
from sensor_msgs.msg import BatteryState

# Import librarys
import rospy, bson, psutil, json
from datetime import datetime
from std_msgs.msg import String
class DecisionMaking:


    def __init__(self) -> None:
        rospy.init_node('decisionMaking', anonymous=False)
        rospy.Subscriber(name='/battery_state', data_class=BatteryState, callback=self.callback, queue_size=1)
        
        self.pub = rospy.Publisher('decision', String, queue_size=1)

        rospy.spin()
            
    def callback(self, msg):
        if msg.voltage < 0.3:
            self.pub.publish(data=self.NavGo2('w1'))
        rospy.sleep(1)

    def NavGo2(self, point):
        command = {
            'status': 0,
            'source': 0,
            'command': point,
            'msg': 'std_msgs/String',
            'topic': '/navGo2',
            'priority': 3
        }
        return json.dumps(command)

        

if __name__ == '__main__':
    try:
        DecisionMaking()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile
from sensor_msgs.msg import BatteryState

# Import librarys
import rospy, bson, psutil
from datetime import datetime

dataPath = {
    'dataSource': 'CeDRI_UGV', 
    'dataBase'  : 'ImpactTests',
    'collection': 'FiveMinutes'
}


class test:
    def __init__(self) -> None:
        rospy.init_node('testNode', anonymous=False)
        rospy.Subscriber(name='/battery_state', data_class=BatteryState, callback_args=self.callback, queue_size=1)
        rospy.spin()
        
            
    def callback(self, msg):
        rate = rospy.Rate(1)
        try:
            data = {
                'datetime': datetime.now(),
                'battery_voltage': msg.voltage,
                'cpu_perc': psutil.cpu_percent(percpu=True),
                'memory': psutil.virtual_memory(),
            }
            createFile(dataPath=dataPath, content=data) 
        except Exception as e:
            print(e)
        for i in range(1, 300): rate.sleep()

if __name__ == '__main__':
    try:
        test()
    except rospy.ROSInterruptException:
        pass

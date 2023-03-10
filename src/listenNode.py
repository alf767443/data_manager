#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile
from GlobalSets.util import msg_to_document

# Import nodes.py
from nodes import NODES

# Import librarys
import rospy, bson
from datetime import datetime
from tf.transformations import euler_from_quaternion

class listenNodes:
    def __init__(self, NODES) -> None:
        rospy.init_node('listenNodes', anonymous=False)
        self.NODES = NODES
        for node in self.NODES:
            node['ROS_rate'] = rospy.Rate(node['rate'])
            self.newSubscriber(node=node)
        rospy.spin()
               
    def newSubscriber(self, node):
        rospy.Subscriber(name='/' + node['node'], data_class=node['msg'], callback=self.callback, callback_args=node, queue_size=1)
        
    def callback(self, msg, args):
        try:
            data = msg_to_document(msg=msg)
            data.update({'dateTime': datetime.now()})
            if(args['q2e']):
                orientation = data['pose']['pose']['orientation']
                (raw, pitch, yaw) = euler_from_quaternion([orientation['x'], orientation['y'], orientation['z'], orientation['w']])
                orientation = {
                    'raw'     :  raw,
                    'pitch'   : pitch,
                    'yaw'     : yaw,
                }
                data.update({'pose': {'pose': {'position': data['pose']['pose']['position'], 'orientation': orientation}}})
            ##
            #print(data)
            ##
            createFile(dataPath=args['dataPath'], content=data) 
        except Exception as e:
            print(e)
        args['ROS_rate'].sleep()


if __name__ == '__main__':
    try:
        listenNodes(NODES=NODES)
    except rospy.ROSInterruptException:
        pass

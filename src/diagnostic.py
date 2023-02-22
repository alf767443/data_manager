#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile
from GlobalSets.util import msg_to_document

# Import nodes.py
from nodes import DIAGNOSTICS_NODES

# Import librarys
import rospy, bson
from datetime import datetime
from tf.transformations import euler_from_quaternion

class diagnosticsNodes:
    def __init__(self, NODES) -> None:
        rospy.init_node('platform_diagnostics', anonymous=False)
        self.NODES = NODES
        self.last_msg = {node['node']: None for node in NODES} 
        for node in self.NODES:
            self.newSubscriber(node=node)
        rospy.spin()

    def newSubscriber(self, node):
        rospy.Subscriber(name='/' + node['node'], data_class=node['msg'], callback=self.callback, callback_args=node)

    def callback(self, msg, args):
        rate = rospy.Rate(args['rate'])
        try:
            data = msg_to_document(msg=msg)
            print('-------------------------------------------')
            print(data)
            print('-------------------------------------------')
            print( self.last_msg[args['node']])
            print('-------------------------------------------')
            data.pop('header')
            if self.last_msg[args['node']] != data:
                self.last_msg[args['node']] = data
                data.update({'dateTime': datetime.now()})
                createFile(dataPath=args['dataPath'], content=data)      
        except Exception as e:
            print(e)
        rate.sleep()


if __name__ == '__main__':
    try:
        diagnosticsNodes(NODES=DIAGNOSTICS_NODES)
    except rospy.ROSInterruptException:
        pass

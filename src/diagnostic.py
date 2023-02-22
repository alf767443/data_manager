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
            print('1-------------------------------------------')
            print(data)
            print('2-------------------------------------------')
            print(self.last_msg[args['node']])
            print('3-------------------------------------------')
            data.pop('header')
            if self.last_msg[args['node']] != data:
                print(self.diff_dicts(dict1=data, dict2=self.last_msg[args['node']]))
                self.last_msg[args['node']] = data.copy()
                data.update({'dateTime': datetime.now()})
                createFile(dataPath=args['dataPath'], content=data)      
        except Exception as e:
            print('########################################')
            print(e)
            print('########################################')
        rate.sleep()

    def diff_dicts(self, dict1, dict2):
        diff = {}
        for chave, valor in dict1.items():
            if chave not in dict2:
                diff[chave] = valor
            elif isinstance(valor, dict):
                sub_diff = self.diff_dicts(valor, dict2[chave])
                if sub_diff:
                    diff[chave] = sub_diff
            elif valor != dict2[chave]:
                diff[chave] = (valor, dict2[chave])
        for chave, valor in dict2.items():
            if chave not in dict1:
                diff[chave] = valor
        return diff

if __name__ == '__main__':
    try:
        diagnosticsNodes(NODES=DIAGNOSTICS_NODES)
    except rospy.ROSInterruptException:
        pass

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
                self.test(dict1=data, dict2=self.last_msg[args['node']])
                self.last_msg[args['node']] = data
                data.update({'dateTime': datetime.now()})
                createFile(dataPath=args['dataPath'], content=data)      
        except Exception as e:
            print('########################################')
            print(e)
            print('########################################')
        rate.sleep()

    def test(self, dict1: dict, dict2:dict):
        try:
            # Encontra as chaves presentes no dict1 mas ausentes no dict2
            diff1 = {key: dict1[key] for key in dict1 if key not in dict2}
            # Encontra as chaves presentes no dict2 mas ausentes no dict1
            diff2 = {key: dict2[key] for key in dict2 if key not in dict1}
            # Encontra as chaves presentes em ambos dicionários, mas com valores diferentes
            diff3 = {key: (dict1[key], dict2[key]) for key in dict1 if key in dict2 and dict1[key] != dict2[key]}

            # Mostra as diferenças encontradas
            print("Diferenças encontradas:")
            print(diff1)
            print(diff2)
            print(diff3)
        except:
            print(Exception)
            pass

if __name__ == '__main__':
    try:
        diagnosticsNodes(NODES=DIAGNOSTICS_NODES)
    except rospy.ROSInterruptException:
        pass

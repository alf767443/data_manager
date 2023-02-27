#!/usr/bin/env python3

# Global imports
from GlobalSets.localSave import createFile
from GlobalSets.util import msg_to_document

# Import nodes.py
from nodes import DIAGNOSTICS_NODES

# Import librarys
import rospy, bson
from datetime import datetime
class diagnosticsNodes:
    status = {}

    def __init__(self, NODES) -> None:
        rospy.init_node('platform_diagnostics', anonymous=False)
        self.NODES = NODES
        self.last_msg = {node['node']: None for node in NODES} 
        for node in self.NODES:
            self.newSubscriber(node=node)
        rospy.spin()

    def newSubscriber(self, node):
        rospy.Subscriber(name='/' + node['node'], data_class=node['msg'], callback=self.callback, callback_args=node, queue_size=1)

    def callback(self, msg, args):
        rate = rospy.Rate(args['rate'])
        try:
            data = msg_to_document(msg=msg)
            try:
                data = data['status']
                # print(data)
                for diagnostics in data:
                    ## Verifica se existe a chave
                    try:
                        self.status[diagnostics['name']]
                    except:
                        self.status.update({diagnostics['name']: None})

                    if (self.status[diagnostics['name']] != diagnostics['level']):
                        self.status.update({diagnostics['name']: diagnostics['level']})
                        diagnostics.update({'dateTime': datetime.now()})
                        createFile(dataPath=args['dataPath'], content=diagnostics)
            except Exception as e:
                pass
            

        except Exception as e:
            print(e)

        rate.sleep()


if __name__ == '__main__':
    try:
        diagnosticsNodes(NODES=DIAGNOSTICS_NODES)
    except rospy.ROSInterruptException:
        pass

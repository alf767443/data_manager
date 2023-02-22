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
        rospy.Subscriber(name='/' + node['node'], data_class=node['msg'], callback=self.callback, callback_args=node)

    def callback(self, msg, args):
        rate = rospy.Rate(args['rate'])
        try:
            data = msg_to_document(msg=msg)
            try:
                data = data['status']
                # print(data)
                for diagnostics in data:
                    print(diagnostics)
                    if (self.status[diagnostics['name']] != diagnostics['level']):
                        print('&&&&&')
                        self.status.update({diagnostics['name']: diagnostics['level']})
                        diagnostics.update({'dateTime': datetime.now()})
                        createFile(dataPath=args['dataPath'], content=diagnostics)
                    print('-------------------------')
                print('+++++++++++++++++++++++++++++++++')
            except Exception as e:
                print('########################################')
                print(e)
                print('########################################')

            

        except Exception as e:
            print('########################################')
            print(e)
            print('########################################')
        rate.sleep()


        # try:
        #     data = msg_to_document(msg=msg)
        #     try:
        #         data.pop('header')
        #     except:
        #         pass


        #     print('1-------------------------------------------')
        #     print(data)
        #     print('2-------------------------------------------')
        #     print(self.last_msg[args['node']])
        #     print('3-------------------------------------------')
        #     if self.last_msg[args['node']] != data:
        #         print('diferenças')
        #         print(self.diff_dicts(dict1=data, dict2=self.last_msg[args['node']]))
        #         print('+++++++++++++++++++++++++++++++++++++++++++')
        #         self.last_msg[args['node']] = data.copy()
        #         data.update({'dateTime': datetime.now()})
        #         createFile(dataPath=args['dataPath'], content=data)      
        # except Exception as e:
        #     print('########################################')
        #     print(e)
        #     print('########################################')
        # rate.sleep()

    def diff_dicts(self, dict1, dict2):
        try:
            diff = {}
            for chave, valor in dict1.items():
                if chave not in dict2:
                    diff[chave] = valor
                elif isinstance(valor, dict):
                    sub_diff = self.diff_dicts(valor, dict2[chave])
                    if sub_diff:
                        diff[chave] = sub_diff
                elif isinstance(valor, list):
                    if len(valor) != len(dict2[chave]):
                        diff[chave] = (valor, dict2[chave])
                    else:
                        sub_diffs = []
                        for i in range(len(valor)):
                            sub_diff = self.diff_dicts(valor[i], dict2[chave][i])
                            if sub_diff:
                                sub_diffs.append(sub_diff)
                        if sub_diffs:
                            diff[chave] = sub_diffs
                elif valor != dict2[chave]:
                    diff[chave] = (valor, dict2[chave])
            for chave, valor in dict2.items():
                if chave not in dict1:
                    diff[chave] = valor
            return diff
        except:
            pass

if __name__ == '__main__':
    try:
        diagnosticsNodes(NODES=DIAGNOSTICS_NODES)
    except rospy.ROSInterruptException:
        pass

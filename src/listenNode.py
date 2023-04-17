#!/usr/bin/env python3

# Global imports
# from GlobalSets.localSave import createFile
from GlobalSets.util import msg_to_document

# Import nodes.py
from nodes import NODES, PATH

# Import librarys
import rospy, bson, os
from fractions import Fraction
from datetime import datetime

# Data storage path
path =  PATH
class listenNodes:
    def __init__(self, NODES) -> None:
        # Inicia o nó unico no ROS core com o nome de listenNode
        rospy.init_node('listenNodes', anonymous=False)

        # Lê a lista de nós presente no arquivo nodes.py
        self.NODES = NODES

        # Configura os subscriber para cada item em NODES
        for node in self.NODES:
            try:
                # Define rate e ticks do nó
                self.sleepDef(node=node)
                # Cria o subscriber
                self.newSubscriber(node=node)
            except Exception as e:
                rospy.logerr("Error in node.py error\n" + e)
                print(e)
        # Mantém o nó ativo
        rospy.spin()
               
# Cria novos subscriber
    def newSubscriber(self, node): 
        try:
            # Utiliza das informações presentes no dicionario 'node' para criar um subscriber
            rospy.Subscriber(name='/' + node['node'], data_class=node['msg'], callback=self.callback, callback_args=node, queue_size=1)
            rospy.loginfo("Subscriber to the node /" + node['node'] + " create")
            return True
        except Exception as e:
            rospy.logerr("Error in the creation of subscriber\n" + e)
            return False
        
# Callback para o nó
    def callback(self, msg, args):
        try:
            # Obtém os dados da mensagem
            data = msg_to_document(msg=msg)
            # Adiciona a data 
            data.update({'dateTime': datetime.now()})
        except Exception as e:
            rospy.logerr("Error to convert the mensage\n" + e)
        try:
            # Se o nó possuir uma função de callback executa
            if args['callback'] != None:
                # Executa a função de callback
                args['callback'](data)
        except Exception as e:
            rospy.logerr("Error in callback function\n" + e)
        # Cria o arquivo de armazenamento
            self.createFile(dataPath=args['dataPath'], content=data) 
        # Espera o tempo definido
        for i in range(1,args['ticks']): args['rate'].sleep()

# Define os parametros de rate e ticks para o nó
    def sleepDef(self, node):
        try: 
            # Encontra a frequencia para o nó e o número de tick de sleep
            fraction = Fraction(node['rate']).limit_denominator()
            rate = fraction.numerator
            ticks = fraction.denominator

            # Define estes dados node
            node['rate'] = rospy.Rate(rate)
            node['ticks'] = ticks

            rospy.logdebug("\tNode rate: " + str(rate) + "\n\t     ticks: " + str(ticks))
            return True
        except Exception as e:
                rospy.logerr("Error to create the timer\n" + e)
                print(e)
                return False
    
# Cria um arquivo que contenha as informações para armazenamento
    def createFile(dataPath: bson, content: bson):
        try:
            # Check if dataPath is valid
            test = dataPath['dataSource']
            test = dataPath['dataBase']
            test = dataPath['collection']
        except Exception as e:
            rospy.logerr("Error in storage data path\n" + e)
            return False
        try:
            # Create data string
            data = bson.encode(document={'dataPath': dataPath, 'content': content})
            # Create the file name
            fileName =  datetime.datetime.strftime(datetime.datetime.now(),"%Y%m%d%H%M%S_%f")
            # Define the extension
            extencion = '.cjson'
            # Create the extension
            fullPath = path+fileName+extencion
            # Create directory if it don't exist
            if not os.path.exists(path=path):
                os.chmod
                os.makedirs(name=path)
            # Create file
            file = open(file=fullPath, mode='a')
            file = open(file=fullPath, mode='wb')
            # Fill file
            file.write(data)
            file.close()
            return True
        except Exception as e:
            rospy.logerr("Error to create the file\n" + e)
            return False


if __name__ == '__main__':
    try:
        listenNodes(NODES=NODES)
    except rospy.ROSInterruptException:
        pass

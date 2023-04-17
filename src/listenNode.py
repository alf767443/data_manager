#!/usr/bin/env python3

# Global imports
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
        # Starts unique node in the ROS core with the name listenNode
        rospy.init_node('listenNodes', anonymous=False)
        # Reads out the list of nodes present in the file nodes.py
        self.NODES = NODES
        # Set up the subscribers for each item in NODES
        for node in self.NODES:
            try:
                # Set node rate and ticks
                self.sleepDef(node=node)
                # Creates the subscriber
                self.newSubscriber(node=node)
            except Exception as e:
                rospy.logerr("Error in node.py error\n" + e)
        # Keeps the node active
        rospy.spin()
               
# Create new subscriber
    def newSubscriber(self, node): 
        try:
            # Uses the information in the node dictionary to create a subscriber
            rospy.Subscriber(name='/' + node['node'], data_class=node['msg'], callback=self.callback, callback_args=node, queue_size=1)

            rospy.loginfo("Subscriber to the node /" + node['node'] + " create")
            return True
        except Exception as e:
            rospy.logerr("Error in the creation of subscriber\n" + e)
            return False
        
# Callback to the node
    def callback(self, msg, args):
        try:
            # Gets the message data
            data = msg_to_document(msg=msg)
            # Adds the date 
            data.update({'dateTime': datetime.now()})
        except Exception as e:
            rospy.logerr("Error to convert the mensage\n" + e)
        try:
            # If the node has a callback function it executes
            if args['callback'] != None:
                # Execute the callback function
                args['callback'](data)
        except Exception as e:
            rospy.logerr("Error in callback function\n" + e)
        # Create the storage file
            self.createFile(dataPath=args['dataPath'], content=data) 
        # Wait the set time
        for i in range(1,args['ticks']): args['rate'].sleep()

# Set the rate and ticks parameters for the node
    def sleepDef(self, node):
        try: 
            # Find the frequency for the node and the number of sleep ticks
            fraction = Fraction(node['rate']).limit_denominator()
            rate = fraction.numerator
            ticks = fraction.denominator
            # Define this data node
            node['rate'] = rospy.Rate(rate)
            node['ticks'] = ticks
            rospy.logdebug("\tNode rate: " + str(rate) + "\n\t     ticks: " + str(ticks))
            return True
        except Exception as e:
                rospy.logerr("Error to create the timer\n" + e)
                print(e)
                return False
    
# Create a file that contains the information for storage
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

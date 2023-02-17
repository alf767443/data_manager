
class getDiagnostic:
    def __init__(self, NODES) -> None:
        rospy.init_node('platform_diagnostics', anonymous=False)
        self.NODES = NODES
        for node in self.NODES:
            self.newSubscriber(node=node)
        rospy.spin()
               
    def newSubscriber(self, node):
        rospy.Subscriber(name='/' + node['node'], data_class=node['msg'], callback=self.callback, callback_args=node)
        
    def callback(self, msg, args):
        rate = rospy.Rate(args['rate'])
        try:
            data = msg_to_document(msg=msg)
            data.update({'dateTime': datetime.now()})
            ##
            #print(data)
            ##
            createFile(dataPath=args['dataPath'], content=data) 
        except Exception as e:
            print(e)
        rate.sleep()


if __name__ == '__main__':
    try:
        listenNodes(NODES=NODES)
    except rospy.ROSInterruptException:
        pass

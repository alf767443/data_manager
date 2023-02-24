#!/usr/bin/env python3

import rospy
from rospy import Message
from rostopic import get_topic_class
from rosgraph_msgs.msg import Log

def callback(msg: Message):
    if msg.name == "/rosout":
        if msg.level == Log.INFO and "registered as a publisher" in msg.msg:
            parts = msg.msg.split(" ")
            node_name = parts[0]
            topic_name = parts[-1]
            topic_type = get_topic_class(topic_name)[0].__name__
            print(f"Publisher node '{node_name}' is publishing to topic '{topic_name}' of type '{topic_type}'")
        elif msg.level == Log.INFO and "subscribing to topic" in msg.msg:
            parts = msg.msg.split(" ")
            node_name = parts[0]
            topic_name = parts[-1]
            topic_type = get_topic_class(topic_name)[0].__name__
            print(f"Subscriber node '{node_name}' is subscribing to topic '{topic_name}' of type '{topic_type}'")

if __name__ == '__main__':
    rospy.init_node('node_info')
    rospy.Subscriber('/rosout', Log, callback)
    rospy.spin()

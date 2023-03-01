#!/usr/bin/env python3

from GlobalSets.Mongo import DataSource as Source, Clients, DataBases as db, Collections as col
from GlobalSets.localSave import createFile
from tcppinglib import tcpping

import rospy, bson, rosnode, rosgraph
import psutil, os
from datetime import datetime
import re

dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase'  : db.dataLake,
    'collection': col.Processes
}

class getNodes:
    def __init__(self) -> None:
        rospy.init_node('getHTOP', anonymous=False)
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():  
            try:              
                data = []
                process = psutil.process_iter(attrs=['status', 'cpu_num', 'pid', 'memory_full_info', 'cpu_percent', 'username', 'name', 'num_threads', 'memory_percent'])
                for proc in process:
                    # print(proc.info)
                    try:
                        temp = proc.info
                            
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                    else:
                        data.append(temp)
                _data = {
                    'process': data, 
                    'dateTime': datetime.now()
                    }
                # print(data)
                createFile(dataPath=dataPath, content=_data) 

            except Exception as e:
                print(e)
            rate.sleep()

if __name__ == '__main__':
    try:
        getNodes()
    except rospy.ROSInterruptException:
        pass




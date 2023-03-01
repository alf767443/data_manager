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
    'collection': 'Processes'
}

class getNodes:
    def __init__(self) -> None:
        rospy.init_node('getHTOP', anonymous=False)
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():  
            try:              
                data = []
                for proc in psutil.pids():
                    try:
                        # Ignora data com acesso negado
                        # print(proc)

                        p = psutil.Process(proc)
                        with p.oneshot():
                            temp = {
                                'nome_executavel': os.path.basename(p.exe()),
                                'linha_comando': " ".join(p.cmdline()),
                                'mem_VMS': p.memory_info().vms,
                                'mem_RSS': p.memory_info().rss,
                                'mem_percent': p.memory_percent(),
                                'cpu_percent': p.cpu_percent(),
                                # 'create_time': p.create_time(),
                                'status': p.status(),
                                'terminal': p.terminal(),
                            }
                        print(temp)
                        # if(temp['cpu_percent']>0):
                        #     print(p.pid, p.cpu_times(), p.cpu_percent(), p.cpu_affinity(), temp['cpu_percent'])

                        # proc = proc.one
                        # info = proc.as_dict(['pid', 'name', 'status', 'cmdline', 'memory_percent'])
                        # info.update({
                        #     'mem_RSS' : proc.memory_info().rss
                        #     'cpu_percent': proc.
                        # })
                    
                        
                        # info = proc.as_dict(attrs=['pid', 'name', 'username', 'memory_info', 'cpu_percent', 'status', 'create_time'])
                        # p = psutil.Process(info['pid'])
                        # with p.oneshot():
                        #     _data = {
                        #         'nome_executavel': os.path.basename(p.exe()),
                        #         'linha_comando': " ".join(p.cmdline()),
                        #         'mem_info': p.memory_info(),
                        #         'mem_percent': p.memory_percent(),
                        #         'cpu_percent': p.cpu_percent(0.5),
                        #         'create_time': p.create_time(),
                        #         'status': p.status(),
                        #         'terminal': p.terminal(),
                        #     }
                            
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
                # data = sorted(data, key=lambda proc: proc['cpu_percent'], reverse=True)

                # print("PID    USER      %CPU  %MEM    VSZ   RSS   TTY   STAT  STARTED      TIME  COMMAND")
                # for processo in data:
                #     try:
                #         # Obtém informações adicionais sobre o processo
                #         p = psutil.Process(processo['pid'])
                #         with p.oneshot():
                #             nome_executavel = os.path.basename(p.exe())
                #             linha_comando = " ".join(p.cmdline())
                #             mem_info = p.memory_info()
                #             mem_percent = p.memory_percent()
                #             cpu_percent = p.cpu_percent(interval=0.5)
                #             create_time = datetime.fromtimestamp(p.create_time())
                #             create_time_str = create_time.strftime("%Y-%m-%d %H:%M:%S")
                #             status = p.status()
                #             terminal = p.terminal()
                #     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                #         # O processo pode ter terminado durante a execução do loop
                #         continue
                #     print(f"{processo['pid']:5d} {processo['username']:<10s} {cpu_percent:6.2f} {mem_percent:6.2f} {self.get_size(mem_info.vms):>6s} {self.get_size(mem_info.rss):>6s} {terminal or '-':<6s} {status:<4s} {create_time_str} {linha_comando[:40]:<40s}")


            except Exception as e:
                print(e)
            rate.sleep()
            
    def get_size(self, bytes, suffix="B"):
        """
        Converte bytes em um formato legível (exemplo: KB, MB, GB, TB)
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f} {unit}{suffix}"
            bytes /= factor



if __name__ == '__main__':
    try:
        getNodes()
    except rospy.ROSInterruptException:
        pass




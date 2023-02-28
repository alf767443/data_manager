#!/usr/bin/env python3

from GlobalSets.Mongo import DataSource as Source, Clients, DataBases as db, Collections as col
from GlobalSets.localSave import createFile
from tcppinglib import tcpping

import rospy, bson, rosnode, rosgraph
import psutil
from datetime import datetime
import re

dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase'  : db.dataLake,
    'collection': col.Nodes
}

class getNodes:
    def __init__(self) -> None:
        rospy.init_node('getHTOP', anonymous=False)
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():  
            try:              
                # Informações da CPU
                print("="*40, "Informações da CPU", "="*40)
                # Número de núcleos
                print("Número de núcleos físicos:", psutil.cpu_count(logical=False))
                print("Número de núcleos virtuais:", psutil.cpu_count(logical=True))
                # Frequência da CPU
                freq = psutil.cpu_freq()
                print(f"Frequência atual da CPU: {freq.current:.2f}MHz")
                print(f"Frequência máxima da CPU: {freq.max:.2f}MHz")
                print(f"Frequência mínima da CPU: {freq.min:.2f}MHz")
                # Uso da CPU
                print("Uso da CPU por núcleo:")
                for i, percent in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                    print(f"Núcleo {i}: {percent}%")
                print(f"Uso total da CPU: {psutil.cpu_percent()}%")

                # Informações da memória
                print("="*40, "Informações da memória", "="*40)
                svmem = psutil.virtual_memory()
                print(f"Total de memória: {self.get_size(svmem.total)}")
                print(f"Memória disponível: {self.get_size(svmem.available)}")
                print(f"Memória usada: {self.get_size(svmem.used)}")
                print(f"Percentual de uso da memória: {svmem.percent}%")

                # Informações do disco
                print("="*40, "Informações do disco", "="*40)
                partitions = psutil.disk_partitions()
                for partition in partitions:
                    print(f"Disco: {partition.device}")
                    print(f"Ponto de montagem: {partition.mountpoint}")
                    print(f"Tipo de sistema de arquivos: {partition.fstype}")
                    try:
                        partition_usage = psutil.disk_usage(partition.mountpoint)
                    except PermissionError:
                        # Acesso negado para o disco
                        continue
                    print(f"Total de espaço: {self.get_size(partition_usage.total)}")
                    print(f"Espaço usado: {self.get_size(partition_usage.used)}")
                    print(f"Espaço livre: {self.get_size(partition_usage.free)}")
                    print(f"Percentual de uso: {partition_usage.percent}%")

                # Informações da rede
                print("="*40, "Informações da rede", "="*40)
                # Endereços IP
                if_addrs = psutil.net_if_addrs()
                for interface_name, interface_addresses in if_addrs.items():
                    for address in interface_addresses:
                        print(f"Interface: {interface_name}")
                        if str(address.family) == 'AddressFamily.AF_INET':
                            print(f"Endereço IPv4: {address.address}")
                            print(f"Máscara de sub-rede: {address.netmask}")
                            print(f"Gateway padrão: {address.broadcast}")
                        elif str(address.family) == 'AddressFamily.AF_INET6':
                            print(f"Endereço IPv6: {address.address}")

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



from nodes import NODES
import os 

for node in NODES:
    os.system(f"python test.py {node}") 
    print(node)
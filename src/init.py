#!/usr/bin/env python3

import requests, json, os, socket
class initDatamanager():

  url = "http://192.168.217.183:8000/ugv/firstConnection"
  sudoPassword = 'ubuntu'

  def __init__(self) -> None:
    print('Try to sync')
    try: 
      self.syncDate(self.firstConnection())
    except Exception as e:
      print(e)
      pass
  
  def firstConnection(self) -> json:
    headers = {
      'Content-Type': 'text/plain'
    }

    payload = {
      'ip': socket.gethostbyname(socket.gethostname())
    }

    payload = json.dumps(payload)
    response = None
    # while response['timedate'] == None:
    response =  requests.request("POST", self.url, headers=headers, data=payload)   
    
    return response.json()

  def syncDate(self, request):
    command = 'timedatectl set-time "' + request['timedate'] + '"'
    p = os.system('echo %s|sudo -S %s' % (self.sudoPassword, command))
    if(not p):
      p = os.system('bash ../runROSnodes.sh')



if __name__ == '__main__':
    try:
        initDatamanager()
    except Exception as e:
        pass

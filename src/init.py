import requests, json, os


class initDatamanager():

  url = "http://192.168.217.183:8000/ugv/firstConnection"
  sudoPassword = 'ubuntu'

  def __init__(self) -> None:
    print('hello')
    self.syncDate(self.firstConnection())
    pass
  
  def firstConnection(self) -> json:
    headers = {
      'Content-Type': 'text/plain'
    }

    payload = {
      'ip': '0.0.0.0'
    }

    payload = json.dumps(payload)

    response = requests.request("POST", self.url, headers=headers, data=payload)

    print(response)

    return response

  def syncDate(self, request):
    print('here')
    command = 'timedatectl'
    p = os.system('echo %s|sudo -S %s' % (self.sudoPassword, command))
    print(p)


if __name__ == '__main__':
    try:
        initDatamanager()
    except Exception as e:
        pass

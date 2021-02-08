import socket
from requests import get
from json import loads


class IPTools():
    def getLocalIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        localIP = s.getsockname()[0]
        s.close()
        return localIP
    
    def getPublicIP(self):
        response = loads(get("https://wtfismyip.com/json").content.decode("utf-8"))
        return response["YourFuckingIPAddress"]

if __name__ == "__main__":
    tool = IPTools()
    print(tool.getLocalIP())
    print(tool.getPublicIP())
from bluepy.btle import Scanner, DefaultDelegate,Peripheral
import datetime
class device:
    def __init__(self,name,addr,rssi,valid):
        self.name = name
        self.addr = addr
        self.rssi = rssi
        self.valid = valid 

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.dev=None
        self.rssi = 10000
    def handleDiscovery(self, dev, isNewDev, isNewData):
        name = dev.getValueText(9)
        if isNewDev and self.dev is None:
            if name is not None and "netw0rk" in name:
                print("Found %s"%(name))
                self.dev = dev
                self.rssi = dev.rssi
                print(dev.rssi)
        elif isNewData and self.dev is None:
            if name is not None and "netw0rk" in name :
                print("Found %s"%(name))
                self.dev = dev
                self.rssi = dev.rssi
                print(dev.rssi)
    def ClearDev(self):
       self.dev=None
       print("Cleared Device")
def getTime():
 currentDT = datetime.datetime.now()
 return str(currentDT)

def SignDevice(dev):
 if dev.valid is True:
    read = "81353fc9-33e0-4c51-994b-b52235b4d585"
    write= "2de200df-7fe6-49e3-a768-5ff79e767fa6"
    print("trying to connect to device: %s"%dev.addr)
    connection = Peripheral(dev.addr,"random")
    for c in connection.getCharacteristics(): 
     if c.uuid==read: 
      data = c.read()
      print("".join(map(chr,data)))
     elif c.uuid==write:
       sig = "node-1_%s"%dev.rssi
       signature = '%s|%s'%(sig,getTime())
       res=c.write(str.encode(signature),True)
       if res['rsp'] is not None: 
        print("SUCCESFUL RESPONSE: ",res)
        return
 else: 
     print("Device is not connectable")
     return
def main():
 devices=[]
 d = ScanDelegate()
 scanner = Scanner().withDelegate(d)
 while True:
  scanner.scan(0.1)
  if d.dev is not None:
   net_device = None
   try:
    net_device = device(d.dev.getValueText(9),d.dev.addr,d.dev.rssi,d.dev.connectable)
    if True:# net_device.addr not in devices:
     SignDevice(net_device)
     devices.append(net_device.addr)
     scanner.clear()
     d.ClearDev()
    else: 
     print("Device %s already signed upon"%net_device.addr)
     return
   except Exception as e:
    print("Unable to Connect to Device at address: %s will try again | %s"%(d.dev.addr,d.dev.rssi)) 
if __name__ == "__main__": main()

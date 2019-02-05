from bluepy.btle import Scanner, DefaultDelegate,Peripheral
class device:
    def __init__(self,name,addr,rssi,valid):
        self.name = name
        self.addr = addr
        self.rssi = rssi
        self.valid = valid 
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.name=""
        self.found=False
        self.dev=device(0,0,0,False)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        name = dev.getValueText(9)
        if isNewDev:
            print("Discovered device", dev.addr,name)
            if name == "netw0rk - los":
                self.dev.valid = True
                self.dev.name = name
                self.dev.addr = dev.addr
                self.dev.rssi = dev.rssi
        elif isNewData:
            print("Received new data from", dev.addr)

d = ScanDelegate()
scanner = Scanner().withDelegate(d)
"""
scanner.start()
while d.dev.valid!=True: scanner.process(0.5)
scanner.stop()
"""
scanner.scan(10.0)
print(d.dev.name,d.dev.addr,d.dev.rssi,d.dev.valid)
if d.dev.valid is True:
        read = "81353fc9-33e0-4c51-994b-b52235b4d585"
        write= "2de200df-7fe6-49e3-a768-5ff79e767fa6"
        print("trying to connect")
        connection = Peripheral(d.dev.addr,"random")
        #print("Printing Services")
        #for s in connection.getServices(): print(s)
        print("Printing Characteristics")
        for c in connection.getCharacteristics(): 
             if c.uuid==read: 
                 data = c.read()
                 print("".join(map(chr,data)))
             if c.uuid==write:
                 res=c.write(b'hello|carlos',True)
                 print("RESPONSE: ",res)
else: print("UNABLE TO CONNECT")

"""
for dev in devices:
    print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
    for (adtype, desc, value) in dev.getScanData():
        print("  %s = %s" % (desc, value))
"""

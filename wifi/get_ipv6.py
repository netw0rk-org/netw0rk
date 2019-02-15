import os
f = open('~/cjdns/cjdroute.conf')
address_line = ''
for l in f:
 if '"ipv6"' in l:
  address_line = l
  break
f.close()
print(address_line)
address = address_line.split('"')[3]

file = open('interfaces.adhoc','w')
interface_file = ["auto wlan0","iface wlan0 inet6 static","address","netmask 64", "wireless-channel 1", "wireless-essid netw0rk", "wireless-mode ad-hoc",]
for line in interface_file:
    if line == "address":
        file.write(line+" "+address+"\n")
    else:
        file.write(line+"\n")
file.close()

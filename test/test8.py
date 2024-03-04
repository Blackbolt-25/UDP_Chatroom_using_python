import netifaces

addrs = netifaces.ifaddresses('en0')
ip_addr = addrs[netifaces.AF_INET][0]['addr']

print(ip_addr)

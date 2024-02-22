import socket 
import netifaces

def get_ip_address(interface):
    try:
        addrs = netifaces.ifaddresses(interface)
        ip_info = {}
        if netifaces.AF_INET in addrs:  # Check for IPv4 address
            ip_info['IPv4'] = addrs[netifaces.AF_INET][0]['addr']
        return ip_info
    except ValueError:
        return "Interface not found or doesn't have an IP address."

interface_name = 'en0'
ipd_addr = get_ip_address(interface_name)

print(f"IP Address of {interface_name} : {ipd_addr}")

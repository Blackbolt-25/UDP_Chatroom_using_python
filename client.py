import socket
import threading
import random
import sys
import time
import subprocess
import ipaddress
import re

#Netifaces part
try:
    import netifaces
except ModuleNotFoundError:
    try:
        result = subprocess.run("pip3 install netifaces", shell=True, capture_output=True, text=True)
        print(result.stdout)
        print("Installed netifaces")
    except subprocess.CalledProcessError as e:
        print(f"Error installing netifaces with pip3: {e}")
        try:
            result = subprocess.run("pip install netifaces", shell=True, capture_output=True, text=True)
            print(result.stdout)
            print("Installed netifaces")
        except subprocess.CalledProcessError as e:
            print(f"Error installing netifaces with pip: {e}")
            print("pip not installed, please install it manually and try again")
            sys.exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit()

# Now try to import netifaces again
try:
    import netifaces
    # print("netifaces is successfully imported")
except ModuleNotFoundError:
    print("netifaces is not installed, please install it manually")
    sys.exit()


def get_ipv4_address(interface_name):
    try:
        result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception("Failed to run ipconfig command")
        
        output_lines = result.stdout.split('\n')
        interface_section = False
        ipv4_address = None

        for line in output_lines:
            if line.strip().startswith(interface_name):
                interface_section = True
            elif interface_section:
                if 'IPv4 Address' in line:
                    ipv4_address = re.search(r'(\d+\.\d+\.\d+\.\d+)', line).group(1)
                    break
        
        if not ipv4_address:
            raise Exception(f"IPv4 address not found for interface {interface_name}")
        
        return ipv4_address

    except Exception as e:
        print(f"Error: {e}")
        return None




try:
    addrs = netifaces.ifaddresses('en0')
    ip_addr = addrs[netifaces.AF_INET][0]['addr']
except:
    interface_name = "Wireless"
    ip_addr = get_ipv4_address(interface_name)
    if ip_addr == None:
        print("Wi-Fi couldn't get fetched")
        sys.exit()


client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.bind(("localhost" , random.randint(8000,9000)))

global name
name = input("Nickname :")


def receive():
    global cond
    while cond:
        try:
            message, _ = client.recvfrom(1024)
            sys.stdout.write('\r')
            if message.decode().startswith("Kicked:"):
                print(message.decode()[message.decode().index(" ")+1 :])
                cond = False
                client.close()
                sys.exit()
            elif message.decode().startswith("Taken"):
                print(message.decode()[message.decode().find(":") + 2 :])
                print("Enter a new username:- ")
                cond = False
                client.close()
                print("Exiting....\n Press Enter \n")
                sys.exit()
            elif message.decode().startswith("List:"):
                mes = (message.decode()[message.decode().find(" ") + 1 : ]).split()
                print("The list of Clients are:-")
                for clients in mes:
                    print(clients,end="\n")
            else:
                print(message.decode())
        except:
            pass


cond = True
t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode() , ("localhost",9999))

while True:
    try:
        message=input()
        if message == "Exit":
            client.sendto(f"exit:{name}".encode(),("localhost",9999))
            cond = False
            client.close()
            sys.exit()
        elif message[0:5] == "Kick:":
            message = message + " " + name
            client.sendto(message.encode(),("localhost", 9999))
        elif message.startswith("Direct:"):
            message = message + " " + name 
            client.sendto(message.encode(),("localhost",9999))
        elif message.startswith("Leave:"):
            message = message + " " + name 
            client.sendto(message.encode(),("localhost",9999))
        elif message.startswith("List:"):
            message =  message + " " + name 
            client.sendto(message.encode(),("localhost",9999))
        else:
            client.sendto(f"{name}: {message}".encode(), ("localhost",9999))
    except:
        sys.exit()



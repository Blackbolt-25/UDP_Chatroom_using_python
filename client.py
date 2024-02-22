import socket
import threading
import random
import netifaces
import sys

#To get the ip addr of en0
addrs = netifaces.ifaddresses('en0')
ip_addr = addrs[netifaces.AF_INET][0]['addr']

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.bind(("localhost" , random.randint(8000,9000)))

name = input("Nickname :")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            sys.stdout.write('\r')
            print(message.decode())
        except:
            pass


t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode() , ("localhost",9999))

while True:
    message=input()
    if message == "Exit":
        client.sendto(f"exit:{name}".encode(),("localhost",9999))
        exit()
    elif message[0:5] == "Kick:":
        message = message + " " +name
        client.sendto(message.encode(),("localhost"),9999)
        print("Request to kick has been sent to the admin")
    else:
        client.sendto(f"{name}: {message}".encode(), ("localhost",9999))



def kick(message):
    print(message.decode()[message.decode().index(":") + 2 :])
    vote = input()
    if(vote in ["yes" , "YES" , "Y" , "y" , "Yes"]):
        client.sendto("1".encode(),client)
    else:
        client.sendto("0".encode(),client)
    waiter() 
         
        
def waiter():
    while True: 
        try:
            message , _ = client.recvfrom(1024)
            if(message.decode() == "You have been removed"):
                print(message.decode())
                exit()
            else:
                print(message.decode())
        except:
            pass
        
def get_ip_address():
    try:
        addrs = netifaces.ifaddresses('en0')
        if netifaces.AF_INET in addrs:
            return addrs[netifaces.AF_INET][0]['addr']
    except:
        return "Not found"


t2 = threading.Thread(target=waiter)
t2.start()


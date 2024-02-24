import socket
import threading
import random
import netifaces
import sys
import time

addrs = netifaces.ifaddresses('en0')
ip_addr = addrs[netifaces.AF_INET][0]['addr']

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.bind(("localhost" , random.randint(8000,9000)))

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
            print("Request to kick has been sent to the admin")
        else:
            client.sendto(f"{name}: {message}".encode(), ("localhost",9999))
    except:
        sys.exit()

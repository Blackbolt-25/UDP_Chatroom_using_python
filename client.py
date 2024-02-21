import socket
import threading
import random


client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.bind(("localhost" , random.randint(8000,9000)))

name = input("Nickname :")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode(),end='\r')
        except:
            pass


t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode() , ("localhost",9999))
message, _ = client.recvfrom(1024)
print(message.decode(),end='\r')
print()

while True:
    print(name," : ",end="")
    message = input("")
    if message == "Exit":
        client.sendto(f"exit:{name}".encode(),("localhost",9999))
        exit()
    elif message[0:9] == "Complain:":
        print("\n")
        
    else:
        client.sendto(f"{name}: {message}".encode(), ("localhost",9999))



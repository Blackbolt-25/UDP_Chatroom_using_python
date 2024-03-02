import socket
import threading
import os
import random
import select
import re
timeout=3
client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.bind(("localhost",random.randint(8000,9000)))
name=input("NICKNAME: ")
flag=0
def process_file_name(file_name):
    # Check if the string contains "FILE:"
    if "FILE:" in file_name:
        # Extract the filename after "FILE:"
        _, file_name = file_name.split("FILE:")
        # Split the filename and extension
        file_name, extension = os.path.splitext(file_name)
        # Add "(1)" before the extension
        file_name = f"{file_name}(1){extension}"
        return file_name
    else:
        return None

def receive():
    while True:
        try :
            k=r"C:\Users\ESHANYA\Documents\sender\\"+output_f
            file=open(k,"wb")
            i=0
            while True:
                message,_=client.recvfrom(1024)
                i+=1
                print(i)
                if i==100:
                    file.close()
                    i=0
                    break
                if message:
                    print(file.write(message))
                    
                    file.write(message)
                    
                else:
                    file.close()
                    print("done")


            
        except:
                pass
t=threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG :{name}".encode(),("localhost",9999))
while True:
    message=input("")
    if "FILE:" in message:
        output_f = process_file_name(message)
    if message=="!q":
        exit()

    else:
        client.sendto(f"{name}:{message}".encode(),("localhost",9999))




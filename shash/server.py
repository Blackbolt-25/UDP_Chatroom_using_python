import socket
import threading
import queue
import os
import re
import time
messages = queue.Queue()
clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# "C:\Users\LEN0VO\PROGRAMS JAVA\hello.txt"
server.bind(("localhost", 9999))
def delete_until_file(text):
    file_index = text.find("FILE:")
    if file_index != -1:
        return text[file_index + len("FILE:"):]
    else:
        return text
def contains_file_word(sentence):
    pattern = 'FILE:'
    if re.search(pattern, sentence):
        return True
    else:
        return False
def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message)

            p=message.decode()
            if addr not in clients:
                clients.append(addr)
            if message.decode().startswith("SIGNUP_TAG: "):
                name = message.decode()[message.decode().index(":") + 1:]
                broadcast_message(f"{name} joined the chat")
            elif contains_file_word(p):
                print("file__sending")
                file_name = delete_until_file(p).strip()
                file_path = os.path.join(r"C:\Users\ESHANYA\Documents", file_name)
                with open(file_path, "rb") as file:
                 while True:
                    data = file.read(1024)
                    if data:
                        print("-")
                        server.sendto(data, addr)
                        time.sleep(0.02)
                    else:
                        break

            else:
                broadcast_message(message, addr)

def broadcast_message(message, sender=None):
    for client in clients:
        try:
            if sender != client:
                server.sendto(message, client)

        except:
            clients.remove(client)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()

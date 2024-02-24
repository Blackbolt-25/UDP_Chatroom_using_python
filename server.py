import socket 
import threading
import queue

messages = queue.Queue()
clients = []
client_2 = {}

server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(("localhost",9999))

def receive():  
    while True:
        try:    
            message, addr = server.recvfrom(1024)
            messages.put((message,addr))
        except:
            pass


def broadcast():
    while True:
        while not messages.empty():
            message,addr = messages.get()
            try:
                to_be_kicked = message.decode()[message.decode().index("Kick:") + 2: message.decode().index("from")]
            except:
                pass
            print(message.decode())
            if addr not in clients:
                clients.append(addr)
                name = message.decode()[message.decode().index(":") + 1 : ]
                client_2.update({name:addr})
                greeting(addr)
            for client in clients:
                try:
                    if client == addr:
                        continue
                    elif message.decode().startswith("SIGNUP_TAG"):
                        name = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} joined!".encode(),client)
                    elif message.decode().startswith("exit"):
                        name = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} has left the Chatroom!".encode(),client)
                        clients.remove(client)
                    elif message.decode().startswith("Kick"):
                        list = message.decode().split()
                        if client == client_2[list[1]]:
                            server.sendto(f"Kicked: {list[-1]} has kicked you.".encode(),client)
                            clients.remove[client_2[list[1]]] 
                            del client_2[list[1]]
                        else:
                            server.sendto(f"{list[-1]} has kicked {list[1]}".encode(),client)
                    else:
                        server.sendto(message,client)
                except:
                    clients.remove(client)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()

def greeting(addr):
    mes = """Welcome to the Chatroom
    Instructions:-
    1.Please be friendly to everyone in the chatroom.
    2.To exit just type "Exit" <Enter>.
    3.Remember the admin can always kick you for misbehaving.
    4.If you want to request to kick a user.
        Type Kick: <User_name>\n"""
    server.sendto(mes.encode(),addr)

import socket 
import threading
import queue

messages = queue.Queue()
clients = []

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
            print(message.decode())
            if addr not in clients:
                clients.append(addr)
                mes = """Welcome to the UDP Chatroom
    Instructions:-
    1.Please be friendly to everyone in the chatroom.
    2.To exit just type "Exit".
    3.Remeber the admin can always kick you for misbehaving.
    4.If you want to complain about a user. 
    Type "Complain: <Enter> (Type the rest of your complaint)\n\n """
                server.sendto(mes.encode(),addr)
            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG"):
                        name = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} joined!".encode(),client)
                    elif message.decode().startswith("exit"):                #For exiting
                        name = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} has left the Chatroom!".encode(),client)
                        clients.remove(client)
                    else:
                        server.sendto(message,client)
                except:
                    clients.remove(client)
                   
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()



                    






import socket
import threading
host=socket.gethostname()
port=5000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Socket Creation Is Successful")
s.bind((host,port))
print("Socket successfully binded to port "+str(port))
s.listen(4)
print("Waiting for clients to join the chat")
clients={}
def handle_client(c,name):
    while True:
        try:
            data=c.recv(1024).decode('utf-8')
            if not data:
                break
            broadcast_message(f'{name}: {data}')
        except ConnectionResetError:
            break
    del clients[name]
    c.close()
    broadcast_message(f'{name} has left the chat')
def broadcast_message(message):
    for c in clients.values():
        try:
            c.send(message.encode('utf-8'))
        except ConnectionResetError:
            pass
while True:
    c,addr=s.accept()
    name=c.recv(1024).decode('utf-8')
    clients[name]=c
    print(f"Got connection from {addr} with name {name}")
    broadcast_message(f'{name} has joined the chat')
    t=threading.Thread(target=handle_client,args=(c,name))
    t.start()
import socket
import threading
host=socket.gethostname()
port=5000
name=input("Enter your name: ")
c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.connect((host,port))
c.send(name.encode('utf-8'))
def receive_messages():
    try:
        while True:
            try:
                message=c.recv(1024).decode('utf-8')
                print(message)
            except ConnectionResetError:
                break
    except ConnectionAbortedError:
        pass
t=threading.Thread(target=receive_messages)
t.start()
while True:
    message=input()
    if(message=="!CLOSECHAT"):
        print(f"Bye {name}!")
        break
    c.send(message.encode('utf-8'))
c.close()
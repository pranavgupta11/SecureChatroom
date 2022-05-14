import threading
import socket
#import argparse
import os

class Server(threading.Thread):
    def __init__(self,host,port):
        super().__init__()
        self.host = host
        self.port = port
        self.clients = []
    def run(self):
        s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)
        s.bind((self.host , self.port))
        s.listen(5)
        print(f"Listening at: [ {self.host} : {self.port} ]...")
        while True:
            #accepting connections
            clt, adr = s.accept()
            print(f"{adr} connected!")
            #creating anew thread
            server_socket = ServerSocket(clt,adr,self)
            #starting thread
            server_socket.start()
            #adding thread to list of connections/clients
            self.clients.append(server_socket)
            print("Ready for recieving messages from "+str(adr[0]))

    def broadcastMessage(self, message, source):
        for client in self.clients:
            if client.adr != source:
                client.send(message)
    
    def removeclt(self, client):
        if client in self.clients:
            self.clients.remove(client)

class ServerSocket(threading.Thread):
    def __init__(self, clt, adr, server):
        super().__init__()
        self.clt = clt
        self.adr = adr
        self.server = server
    def run(self):
        while True:
            try:
                msg = self.clt.recv(2048).decode("utf-8")
                if msg:
                    print(msg)
                    self.server.broadcastMessage(msg,self.adr)
                else:
                    print(f"Closing connection with {self.adr}")
                    self.clt.close()
                    self.server.removeclt(self)
                    return
            except:
                print(f"Closing connection with {self.adr}")
                self.clt.close()
                self.server.removeclt(self)
                return

    def send(self , msg):
        self.clt.sendall(msg.encode("utf-8"))
def exit(server):
    while True:
        inp = input("Admin: ")
        if inp =="q":
            print("Closing all connections...")
            for client in server.clients:
                client.clt.close()
            print("Shutting the server down...")
            os._exit(0)
if __name__ == '__main__':
    
    server = Server(socket.gethostbyname(socket.gethostname()) , 5000)
    server.start()

    exit = threading.Thread(target = exit , args = (server,))
    exit.start()


        
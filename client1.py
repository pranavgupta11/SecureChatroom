from cProfile import run
import socket
import threading
import os
import sys
import hashlib
from getpass import getpass

def printMenu():
        found = 0
        name = ""
        while found != 1:
            enroll = input("Enter your Enroll : ")
            # Opwd = input("Enter your Password : ")
            Opwd = getpass("Enter your Password :")
            h = hashlib.new('sha256')
            byteForm = bytes(Opwd, 'utf-8')
            h.update(byteForm)
            pwd = h.hexdigest()
            file1 = open("db.txt", "r")
            L = file1.readlines()
            for i in L:
                data = i.split()
                # print(data)
                currEnroll = data[0]
                currPwd = data[3]
                if(currEnroll == enroll):
                    if(currPwd == pwd):
                        found = 1
                        Fname = data[1]
                        Lname = data[2]
                        name = Fname + " " + Lname
                        print(enroll + " : " + name)
                        break
                    else:
                        print("\nInvalid Password")
            if(found == 0):
                print("--------------------Access Denied ------------------\n")
                print("-----------Invalid Username or Password ------------------\n")   
            file1.close()
        return name, enroll


class Send(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        while True:
            sys.stdout.flush()
            my_msg = input()
            if my_msg.lower() =="quit":
                self.sock.sendall(f"{self.name} is quitting the chat...".encode("utf-8"))
                break
            else:
                self.sock.sendall(f"<<{self.name}>> : {my_msg}\n".encode("utf-8"))
        print("Quitting chat...\n")
        os._exit(0)

class Recieve(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
    
    def run(self):
        while True:
            msg = self.sock.recv(2048).decode("utf-8")
            if msg:
                print('\r'+msg)
                print('\n<<You>> : ',end='')
            else:
                print("Looks like the connection is lost...\nQuitting...\n")
                self.sock.close()
                os._exit(0)
    
class Client():
    def __init__(self , host , port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        print(f"Trying to connect to [ {self.host} : {self.port} ]...")
        self.sock.connect((self.host, self.port))
        print(f"Connected to host...")
        print()
        print('''

        ##########################################################################################
                                    
                                    JIIT CHATROOM - CN LAB
                                      Connecting People

        ##########################################################################################                            

        ''')
        name, enroll = printMenu()
        send = Send(self.sock , name)
        recieve = Recieve(self.sock, name)

        
        print()
        print(f"All set, type 'QUIT' to leave...\n<<{enroll}>> : ",end='')
        recieve.start()
        send.start()
        
        self.sock.sendall(f"{name} has entered the chat! ".encode("utf-8"))

if __name__ == "__main__":
    client = Client(socket.gethostbyname(socket.gethostname()) , 5000)
    client.start()

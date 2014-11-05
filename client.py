import socket
from subprocess import call
import threading
import os

class Client(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.sock = socket.socket(socket.AF_INET, 	
                                  socket.SOCK_STREAM) 	
        self.port = 1234
        
    def register(self,serverIP):
        #self.sock.setsockopt(socket.SOL_SOCKET, 25, self.device)
        self.sock.connect((serverIP, self.port))
        self.serverIP = serverIP
        self.running = True
        self.start()
        
    def run(self):
        while self.running:
            msg = self.sock.recv(1024)
            if msg == '':
                print 'no server'
                exit()
            #msg = msg.split()
            #call(["notify-send", msg[0], msg[1]])
            call = 'notify-send '+self.serverIP+' "'+msg+'"'
            print call
            os.system(call)

    def unregister(self):
        self.running = False
        self.sock.close()
        

if __name__=='__main__':
    import time
    print 'start network notify client'
    c = Client()
    c.register('192.168.0.3')
    time.sleep(1500)
    c.unregister()
    
    
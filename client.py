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
    c.register('163.152.71.180')
    c.join()
    c.unregister()
    
    
import socket
from subprocess import call
import threading
import os
import signal

class Client(threading.Thread):

    def __init__(self, port = 1234):
        threading.Thread.__init__(self)
        self.daemon = True
        self.sock = socket.socket(socket.AF_INET, 	
                                  socket.SOCK_STREAM) 	
        self.port = port
        
    def connect(self,serverIP):
        try:
            self.sock.connect((serverIP, self.port))
        except socket.error:
            print 'no server available'
            return
        self.serverIP = serverIP
        self.running = True
        self.start()
        
    def run(self):
        while self.running:
            msg = self.sock.recv(1024)
            if msg == '':
                print 'server shut down'
                exit()
            call = 'notify-send '+self.serverIP+' "'+msg+'"'
            print call
            os.system(call)

    def disconnect(self):
        self.running = False
        self.sock.close()


def signalHandler(signal, frame):
    exit(0)

if __name__=='__main__':
    import time
    print 'start network notify client'
    c = Client()
    c.connect('127.0.0.0')

    signal.signal(signal.SIGINT, signalHandler)

    # wait for kill signal
    signal.pause()
    
    
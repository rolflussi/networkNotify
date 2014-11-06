import socket
from subprocess import call
import os
import threading

class Server(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.sock = socket.socket(socket.AF_INET, 	
                                  socket.SOCK_STREAM) 	
        self.port = 1234
        self.interface = 'eth0'
        self.connections = []
        
        p = os.popen('ifconfig '+self.interface+' | grep "inet addr"')
        s = p.read()
        s = s.split()[1]
        self.serverIP = s.split(':')[1]
        self.sock.bind((self.serverIP, self.port))

        # listen for incoming connections
        self.sock.listen(1)
        
        
    def run(self):
        while True:
            connection, clientAddress = self.sock.accept()
            (clientIP, clientPort) = clientAddress
            print 'new client at '+clientIP
            self.connections.append(connection)


    def send(self, msg):
        for con in self.connections:
            try:
                con.send(msg)
            except socket.error:
                del con

def pipeRead():
    path = '/tmp/networkNotify'
    try:
        os.mkfifo(path)
    except IOError:
        os.remove(path)
        os.mkfifo(path)
    fifo = open(path,'r')
    msg = ''
    for line in fifo:
        msg += line + ' '
    fifo.close()
    os.remove(path)
    return msg
    
                
if __name__=='__main__':
    print 'start network notify deamon'
    s = Server()
    s.start()

    import time

    while True:
        msg = pipeRead()
        s.send(msg)

        
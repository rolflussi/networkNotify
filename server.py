import socket
from subprocess import call
import os
import threading
import logging

class Server(threading.Thread):

    def __init__(self, port = 1234):
        threading.Thread.__init__(self)
        self.daemon = True
        self.sock = socket.socket(socket.AF_INET, 	
                                  socket.SOCK_STREAM) 	
        self.port = port
        self.connections = []
        
        try:
            self.sock.bind(('', self.port))
        except socket.error:
            logging.warning("""port is already assigned to other service
                            notifyDaemon already running?""")
            return
        # listen for incoming connections
        self.sock.listen(1)
        
        
    def run(self):
        while True:
            try:
                connection, clientAddress = self.sock.accept()
            except:
                continue
            (clientIP, clientPort) = clientAddress
            logging.info('new client at '+clientIP)
            self.connections.append(connection)


    def send(self, msg):
        for con in self.connections:
            try:
                con.send(msg)
            except socket.error:
                logging.info('removed client')
                del con

class Pipe:
    @staticmethod
    def read():
        path = '/tmp/networkNotify'
        try:
            os.mkfifo(path)
        except OSError:
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
    
    s = Server()
    s.start()

    import time

    while True:
        msg = Pipe.read()
        s.send(msg)

        
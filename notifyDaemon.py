from server import Server,Pipe
from client import Client
from ConfigParser import SafeConfigParser
from os.path import expanduser
import signal

def signalHandler(signal, frame):
    exit(0)

if __name__=='__main__':

    # keyboard interrupt handler
    signal.signal(signal.SIGINT,signalHandler)

    # load the configuration files
    parser = SafeConfigParser()
    homeDir = expanduser("~")
    files = [homeDir+'/.config/network-notify/network-notify.conf',
             '/etc/network-notify/network-notify.conf',
             'config/network-notify.conf']
    configs = parser.read(files)

    if not configs:
        print 'no config file found, using default settings'
        port = 5678
        mode = 'both'
        serverIP = '127.0.0.1'
    else:
        port = int(parser.get('general','port'))
        mode = parser.get('general','mode')
        
    if mode == 'both' or mode == 'server':
        # start server
        server = Server(port)
        server.start()

    if mode == 'both' or mode == 'client':
        # start client
        serverIP = parser.get('client','server')
        client = Client(port)
        client.connect(serverIP)

    if mode == 'both' or mode == 'server':
        while True:
            msg = Pipe.read()
            server.send(msg)
    else:
        
        # wait for kill signal
        signal.pause()

        
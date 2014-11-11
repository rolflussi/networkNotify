from server import Server,Pipe
from client import Client
from ConfigParser import SafeConfigParser
from os.path import expanduser,isdir
import signal
import logging

def signalHandler(signal, frame):
    logging.info('shut down daemon')
    exit(0)

if __name__=='__main__':

    # setup the log files
    if isdir('log'):
        logfile = 'log/network-notify.log'
    else:
        logfile = 'network-notify.log'
    logging.basicConfig(filename=logfile,format='%(asctime)s %(levelname)s: %(message)s',datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
    logging.info('started notify daemon')
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
        logging.warning('no config file found, using default settings')
        port = 5678
        mode = 'both'
    else:
        port = int(parser.get('general','port'))
        mode = parser.get('general','mode')
        
    if mode == 'both' or mode == 'server':
        # start server
        server = Server(port)
        server.start()
        logging.info('started server at port '+str(port))

    if mode == 'both' or mode == 'client':
        # start client
        serverIP = parser.get('client','server')
        client = Client(port)
        logging.info('started client at port '+str(port))
        client.connect(serverIP)

    if mode == 'both' or mode == 'server':
        while True:
            msg = Pipe.read()
            server.send(msg)
    else:
        
        # wait for kill signal
        signal.pause()

        
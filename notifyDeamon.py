from server import Server,Pipe
from client import Client


if __name__=='__main__':

    # start server
    s = Server()
    s.start()

    # start client
    c = Client()
    c.register('163.152.71.180')

    while True:
        msg = Pipe.read()
        s.send(msg)
import sys
path = '/tmp/networkNotify'
fifo = open(path,'w')
del sys.argv[0]

for arg in sys.argv:
    fifo.write(arg+' ')

fifo.close()

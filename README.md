networkNotify
=============

networkNotify is a tool to extend the use of notify-send in ubuntu to be triggered from a remote device. The notification is sent over a TCP connection. The connection is established between the server and client script. In the moment the notification transfer is just possible in the direction from the server to the client. While the server.py and client.py are running as daemon is the script networkNotify.py used to send the notification over the network. It interacts with the server deamon and sends the notification to all connected client devices. 


The interface needs the command notify-send on the client side to show the notification. This requires the package libnotify-bin to be installed. 

`sudo apt-get install libnotify-bin`

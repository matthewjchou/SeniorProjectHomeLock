#SERVER SIDE (PYTHON)

import socket
import time
####ENABLE FOR USE ON PI####
#import RPi.IO as IO 
import os

#IO.setmode(IO.BOARD)
#IO.setup(7, IO.OUT, initial = IO.LOW) # Green (blue really)
#IO.setup(11, IO.OUT, initial = IO.LOW) # Red 


HOST = ''
PORT = 5007

statusFile = open('Status.txt', 'w+')
statusFile.write('0')
statusFile.close()

#whitelist = open('whitelist.txt', 'w+')


#create a socket on the network using port 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#name of the host (router, unless it has no name, then return IP address)
HOSTNAME = socket.gethostname()
server_address = (HOST, PORT)
print('Hostname: %s' % HOSTNAME)
print('starting up on %s port %s' % (server_address[0], server_address[1]))

#binds to the host and port
s.bind(server_address)
#listens to the bound host's port
#waits for (1) connection
s.listen(1)
print('listening for a connection...')

while(True):
    try:
        #if a connection` is found, accept it and create (object, string)
        (CONNECTION, ADDRESS) = s.accept()
        print(ADDRESS)
        print('connection found...')
        #receive the data (up to 3 bytes or 24 bits or 2^24)
        
        data = CONNECTION.recv(1024).decode("utf-8")
        #(data, phoneName) = data.split('|')
        #print(data + ', ' + phoneName)

        #123 temp password, for changing by the android app
        if data == '123':
            msg = 'Authorized'
            print('Authorized Connection for: ' + ADDRESS[0])

            CONNECTION.send(msg.encode("utf-8"))

            #IO.output(7, IO.HIGH)
            #IO.output(11, IO.LOW)

            #disable the motion detection for this
            statusFile = open('Status.txt', 'w+')
            statusFile.write('1')
            statusFile.close()

            #whitelist = open('whitelist.txt', 'a+')
            #whitelist.write(phoneName + '\n')
            #whitelist.close()
            CONNECTION.close()

            time.sleep(1)
            #make a new socket for broadcasting
            (BROADCAST, ADDRESS) = s.accept()
            print("Accepting broadcast connection on: " + ADDRESS[0])
            
            msg2 = "here"
            response = "in range"

            while(response == "in range"):
                print("Entering loop")
                response = "checking"
                response = BROADCAST.recv(1024).decode("utf-8")
                time.sleep(3)
                BROADCAST.send(msg2.encode("utf-8"))
                reponse = BROADCAST.recv(1024).decode("utf-8")
                print(response)

        elif(data == 'stop'):
            CONNECTION.close()
            break;

        else:
            msg = 'Denied'
            print('Unauthorized Connection')
            statusFile = open('Status.txt', 'w+')
            statusFile.write('0')
            statusFile.close()
            
            CONNECTION.send(msg.encode("utf-8"))

            #IO.output(7, IO.LOW)
            #IO.output(11, IO.HIGH)

            CONNECTION.close()

    except KeyboardInterrupt:
       s.close()
       CONNECTION.close()
       #IO.cleanup()



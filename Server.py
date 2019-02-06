#Server side, Python

import socket
import time
import os

#Only used if on a Raspberry Pi
import RPi.IO as IO

CONNECTED_OUTPUT_PIN = 7 
NOT_CONNECTED_OUPUT_PIN = 11

HOST = ''
HOSTNAME = socket.gethostname()
PORT = 5007

SERVER_ADDRESS = (HOST, PORT)

MASTER_PASSWORD = '123'

BOARD_IN_USE = false

def pi_board_setup():
    IO.setmode(IO.BOARD)
    IO.setup(CONNECTED_OUTPUT_PIN, IO.OUT, initial = IO.LOW)
    IO.setup(NOT_CONNECTED_OUPUT_PIN, IO.OUT, initial = IO.LOW)

def socket_setup():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Hostname: ' + HOSTNAME)
    print('Starting on ' + SERVER_ADDRESS[0] + 'using port' + PORT)
    s.bind(SERVER_ADDRESS)

    try:
        s.listen(1)
        print('Listening for connection...')
        (CONNECTION, ADDRESS) = s.accept()
        print('Connection found')
    except socket.timeout:
        print('Connection not found')
        sys.exit(1)

    return CONNECTION, ADDRESS

def check_authorized_connection(passcode, connection_address):
    if (passcode == MASTER_PASSWORD):
        print('Authorized connection for '+ connection_address)
        status_file_write('1')

        return True

    else:
        print('Unauthorized connection')
        status_file_write('0')
        return False

def status_file_write(status):
    statusFile = open('Status.txt', 'w+')
    statusFile.write(status)
    statusFile.close()

def main():
    if (BOARD_IN_USE):
        pi_board_setup()
    
    (connection, connection_address) = socket_setup()

    data = connection.recv(1024).decode('utf-8')

    if (check_authorized_connection(data, connection_address)):
        msg = 'Authorized'
        connection.send(msg.encode('utf-8'))
        
    




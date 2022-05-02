import socket
import os
import shutil

SERVER_ADDRESS = '04:6C:59:F1:F3:E1'
SERVER_PORT = 4


def create_temp_files():
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.mkdir('temp')


def remove_temp_files():
    if os.path.exists('temp'):
        shutil.rmtree('temp')


if __name__ == '__main__':
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))
    data = sock.recv(1024)
    print(data)
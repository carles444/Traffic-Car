import socket
import os
import shutil


def create_temp_files():
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.mkdir('temp')


def remove_temp_files():
    if os.path.exists('temp'):
        shutil.rmtree('temp')


if __name__ == '__main__':
    create_temp_files()
    os.system('hcitool dev | grep -o "[[:xdigit:]:]\{11,17\}" > temp/address.txt')
    with open('temp/address.txt', 'r') as file:
        MY_ADDRESS = file.readline()
    MY_ADDRESS = MY_ADDRESS.replace('\n', '')
    PORT = 4
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    sock.bind((MY_ADDRESS, PORT))
    sock.listen(1)
    print('listening')
    while True:
        c, addr = sock.accept()
        print('new connection')
        c.send('Connected'.encode())
        c.close()
        print(addr)

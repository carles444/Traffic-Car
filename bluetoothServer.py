import socket
import os
import shutil



def create_temp_files():
    if os.path.exists('../../Documents/Uni/4rt/2nSem/Robotica/projecte/Traffic-Car/temp'):
        shutil.rmtree('../../Documents/Uni/4rt/2nSem/Robotica/projecte/Traffic-Car/temp')
    os.mkdir('../../Documents/Uni/4rt/2nSem/Robotica/projecte/Traffic-Car/temp')


def remove_temp_files():
    if os.path.exists('../../Documents/Uni/4rt/2nSem/Robotica/projecte/Traffic-Car/temp'):
        shutil.rmtree('../../Documents/Uni/4rt/2nSem/Robotica/projecte/Traffic-Car/temp')


if __name__ == '__main__':
    create_temp_files()
    os.system('hcitool dev | grep -o "[[:xdigit:]:]\{11,17\}" > temp/address.txt')
    with open('../../Documents/Uni/4rt/2nSem/Robotica/projecte/Traffic-Car/temp/address.txt', 'r') as file:
        MY_ADDRESS = file.readline()
    MY_ADDRESS = MY_ADDRESS.replace('\n', '')
    PORT = 4
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    sock.bind((MY_ADDRESS, PORT))
    sock.listen(1)
    while True:
        c, addr = sock.accept()
        c.send('Connected'.encode())
        c.close()
        print(addr)

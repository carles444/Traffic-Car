import socket
import os
import shutil

SERVER_ADDRESS = '04:6C:59:F1:F3:E1'
SERVER_PORT = 4


def create_temp_files():
    if os.path.exists('../../Documents/Uni/4rt/2nSem/Robotica/projecte/Traffic-Car/temp'):
        shutil.rmtree('../../Documents/Uni/4rt/2nSem/Robotica/projecte/Traffic-Car/temp')
    os.mkdir('../../Documents/Uni/4rt/2nSem/Robotica/projecte/Traffic-Car/temp')


def remove_temp_files():
    if os.path.exists('../../Documents/Uni/4rt/2nSem/Robotica/projecte/Traffic-Car/temp'):
        shutil.rmtree('../../Documents/Uni/4rt/2nSem/Robotica/projecte/Traffic-Car/temp')


if __name__ == '__main__':
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))
import socket
import os
import shutil
import time
from manualController import manualDriver
from logger import *

RP_ADDR = 'DC:A6:32:AA:AA:E6'
SERVER_ADDRESS = '04:6C:59:F1:F3:E1'
SERVER_PORT = '00000000000000000000000000000005'


def create_temp_files():
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.mkdir('temp')


def remove_temp_files():
    if os.path.exists('temp'):
        shutil.rmtree('temp')


class Controller:
    def __init__(self, server_addr, port):
        self.modes = ['manual', 'autonomous', 'exit']
        self.connected = False
        self.DEFAULT_TIMEOUT = 5
        self.logger = Logger().getLogger('controller', logging.DEBUG)
        self.server_addr = server_addr
        self.port = port
        self.logger.debug(f'Controller initializated with Server addr: {self.server_addr}')
        self.logger.debug(f'Controller initializated with port: {self.port}')
        
    def connect(self):
        self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.sock.settimeout(self.DEFAULT_TIMEOUT)
        self.logger.info(f'Connecting to controller...')
        while not self.connected:
            try:
                self.sock.connect((SERVER_ADDRESS, SERVER_PORT))
                self.connected = True
            except socket.gaierror as exc:
                self.logger.error(f"{exc}, retrying in {self.DEFAULT_TIMEOUT} seconds...")
                time.sleep(self.DEFAULT_TIMEOUT)
                
        self.logger.info('Connected to controller successfully')
    
    def manual_mode(self):
        self.logger.info('Entering in manual mode')
        if self.manual_driver is None:
            self.manual_driver = manualDriver(self.sock)
        self.manual_driver()
    
    def autonomous_mode(self):
        self.logger.info('Entering in autonomous mode')
        
    def __call__(self):
        self.connect()
        data = self.sock.recv(1024).decode().lower()
        while data not in self.modes:
            if data == 'manual':
                self.logger.info('Using manual mode')
                self.manual_mode()
            elif data == 'autonomous':
                self.logger.info('Using autonomous mode')
                self.autonomous_mode()
            elif data == 'exit':
                self.logger.info(f'Exited')
                exit(0)
            data = self.sock.recv(1024).decode().lower()

                

if __name__ == '__main__':
    controller = Controller(SERVER_ADDRESS, SERVER_PORT)
    controller()

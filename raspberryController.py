import socket
import os
import shutil
import logging
import time
from datetime import datetime


RP_ADDR = 'DC:A6:32:AA:AA:E6'
SERVER_ADDRESS = '04:6C:59:F1:F3:E1'
SERVER_PORT = 5


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
        self.init_logger(logging.INFO)
        self.server_addr = server_addr
        self.port = port
        self.logger.debug(f'Controller initializated with Server addr: {self.server_addr}')
        self.logger.debug(f'Controller initializated with port: {self.port}')

    
    def init_logger(self, level):
        with open('raspberryController.log', 'a') as log_file:
            log_file.write('\n\n')
            log_file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            log_file.write('\n\n')

        self.logger = logging.getLogger('Controller')
        logging.basicConfig(filename='raspberryController.log')
        self.logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s: %(name)s  [%(levelname)s]  %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        
    def connect(self):
        self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.sock.settimeout(self.DEFAULT_TIMEOUT)
        self.logger.info(f'Connecting to controller...')
        while not self.connected:
            try:
                self.sock.connect((SERVER_ADDRESS, SERVER_PORT))
                self.connected = True
            except socket.error:
                self.logger.error(f"Error: Couldn't connect to controller, retrying in {self.DEFAULT_TIMEOUT} seconds...")
                time.sleep(self.DEFAULT_TIMEOUT)
                
        self.logger.info('Connected to controller successfully')
    
    def manual_mode(self):
        pass
    
    def autonomous_mode(self):
        pass
        
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

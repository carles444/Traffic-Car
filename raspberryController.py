import socket
import os
import shutil
import time
from manualController import manualDriver
from logger import *
import bluetooth

RP_ADDR = 'DC:A6:32:AA:AA:E6'
SERVER_ADDRESS = '04:6C:59:F1:F3:E1'
SERVER_PORT = 5
UUID = '00000000-0000-0000-0000-000000000005'

def create_temp_files():
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.mkdir('temp')


def remove_temp_files():
    if os.path.exists('temp'):
        shutil.rmtree('temp')


class Controller:
    def __init__(self, uuid_service):
        self.modes = ['manual', 'autonomous', 'exit']
        self.uuid_service = uuid_service
        self.connected = False
        self.DEFAULT_TIMEOUT = 5
        self.logger = Logger().getLogger('Raspberry Controller', logging.DEBUG)
        self.logger.debug(f'Controller initializated with uuid: {self.uuid_service}')

    def connect(self):
        services = []
        while len(services) == 0:
            self.logger.info('Connecting to controller...')
            services = bluetooth.find_service(uuid=self.uuid_service)
        self.port = services[0]['port']
        self.name = services[0]['name']
        self.address = services[0]['host']
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((self.address, self.port))
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
        while True:
            data = self.sock.recv(4)
            self.logger.debug(data)
            if data == 'manual':
                self.logger.info('Using manual mode')
                self.manual_mode()
            elif data == 'autonomous':
                self.logger.info('Using autonomous mode')
                self.autonomous_mode()
            elif data == 'exit':
                self.logger.info(f'Exited')
                exit(0)
            

                

if __name__ == '__main__':
    controller = Controller(UUID)
    controller()

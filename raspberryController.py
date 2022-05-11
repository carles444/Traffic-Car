from enum import IntEnum
import os
import shutil
import time
from manualDriver import *
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
        self.manual_driver = None
        self.autonomous_driver = None
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
        return self.manual_driver()
    
    def autonomous_mode(self):
        self.logger.info('Entering in autonomous mode')
        
    def __call__(self):
        self.connect()
        data = None
        while True:
            if data is None:
                data = int.from_bytes(self.sock.recv(1), 'big')
            packet_id = (data >> 4) & 0xf
            if packet_id != Packet.SET_MODE:
                continue
            metadata = data & 0xf
            if metadata == RobotState.AUTONOMOUS:
                self.logger.info('Using autonomous mode')
                data = self.autonomous_mode()
            elif metadata == RobotState.MANUAL:
                self.logger.info('Using manual mode')
                data = self.manual_mode()
            elif metadata == RobotState.EXIT:
                self.sock.close()
                self.logger.info(f'Exited')
                exit(0)
                

if __name__ == '__main__':
    controller = Controller(UUID)
    controller()

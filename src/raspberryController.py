from enum import IntEnum
import os
import shutil
import time
from Driver import *
from autonomousDriver import *
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


class Packet(IntEnum):
    SET_MODE = 1
    MOVE = 2


class RobotState(IntEnum):
    MANUAL = 1
    AUTONOMOUS = 2
    EXIT = 3
    SEND_VIDEO = 4


class Controller:
    def __init__(self, uuid_service):
        self.sock = None
        self.address = None
        self.name = None
        self.port = None
        self.modes = ['manual', 'autonomous', 'exit']
        self.driver = None
        self.autonomous_driver = None
        self.uuid_service = uuid_service
        self.connected = False
        self.DEFAULT_TIMEOUT = 5
        self.logger = Logger().getLogger('Raspberry Controller', logging.DEBUG)
        self.logger.debug(f'Controller initializated with uuid: {self.uuid_service}')
        self.ad_thread = None

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
        if self.driver is None:
            self.driver = Driver()
        while True:
            data = int.from_bytes(self.sock.recv(1), 'big')
            packet_id = (data >> 4) & 0xf
            if packet_id == Packet.SET_MODE:
                self.logger.info("Changing mode... ")
                return data
            elif packet_id != Packet.MOVE:
                continue
            metadata = data & 0xf
            self.driver.apply_movement(metadata)
         
    def autonomous_mode(self):
        self.logger.info('Entering in autonomous mode')
        if self.driver is None:
            self.driver = Driver()
        if self.autonomous_driver is None:
            self.autonomous_driver = AutonomousDriver(self.driver)
        self.ad_thread = threading.Thread(target=self.autonomous_driver)
        self.ad_thread.start()
            
    def stop_autonomous_mode(self):
        if self.autonomous_driver is not None:
            self.autonomous_driver.stop_running()
            self.ad_thread.join()
        
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
                self.autonomous_mode()
            elif metadata == RobotState.MANUAL:
                self.logger.info('Using manual mode')
                self.stop_autonomous_mode()
                data = self.manual_mode()
            elif metadata == RobotState.EXIT:
                self.logger.info(f'Exited')
                self.stop_autonomous_mode()
                self.sock.close()
                break
                
        del self.driver


if __name__ == '__main__':
    controller = Controller(UUID)
    main_t = threading.Thread(target=controller)
    main_t.start()
    main_t.join()

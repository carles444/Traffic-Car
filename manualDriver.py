#import RPi.GPIO as gpio
from enum import IntEnum
from logger import *

class Packet(IntEnum):
    SET_MODE = 1
    MOVE = 2

class RobotState(IntEnum):
    MANUAL = 1
    AUTONOMOUS = 2
    EXIT = 3

class MovementState(IntEnum):
    FORWARD = 1
    RIGHT = 8
    BREAKS = 2
    LEFT = 4
    

class manualDriver:
    def __init__(self, comunication_socket):
        self.communication_socket = comunication_socket
        self.logger = Logger().getLogger('Manual Driver', logging.DEBUG)
        #gpio.setmode(gpio.BOARD)
    
    def apply_movement(self, forward_bit, breaks_bit, left_bit, right_bit):
        if forward_bit:
            self.logger.debug('forward')
        if breaks_bit >> 1:
            self.logger.debug('breaks')
        if left_bit >> 2:
            self.logger.debug('left')
        if right_bit >> 3:
            self.logger.debug('right')
            
    def __call__(self):
        while True:
            data = int.from_bytes(self.communication_socket.recv(1), 'big')
            packet_id = (data >> 4) & 0xf
            if packet_id == Packet.SET_MODE:
                self.logger.info("Changing mode... ")
                return data
            elif packet_id != Packet.MOVE:
                continue
            metadata = data & 0xf
            forward_bit = metadata & 0x1
            breaks_bit = metadata & 0x2
            left_bit = metadata & 0x4
            right_bit = metadata & 0x8
            self.apply_movement(forward_bit, breaks_bit, left_bit, right_bit)
        

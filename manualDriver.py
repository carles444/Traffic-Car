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
    FORWARD = 9
    RIGHT = 8
    BREAKS = 6
    LEFT = 2
    

class manualDriver:
    def __init__(self, comunication_socket):
        self.communication_socket = comunication_socket
        self.logger = logging.getLogger('manualDriver', logging.DEBUG)
        #gpio.setmode(gpio.BOARD)

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
            if metadata == MovementState.FORWARD:
                self.logger.debug("forward")
            elif metadata == MovementState.BREAKS:
                self.logger.debug("breaks")
            elif metadata == MovementState.RIGHT:
                self.logger.debug("right")
            elif metadata == MovementState.LEFT:
                self.logger.debug("left")

#import RPi.GPIO as gpio
from enum import IntEnum

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
        #gpio.setmode(gpio.BOARD)

    def __call__(self):
        while True:
            data = int.from_bytes(self.sock.recv(1), 'big')
            packet_id = (data >> 4) & 0xf
            if packet_id == Packet.SET_MODE:
                return data
            elif packet_id != Packet.MOVE:
                continue
            metadata = data & 0xf
            if metadata == MovementState.FORWARD:
                pass
            elif metadata == MovementState.BREAKS:
                pass
            elif metadata == MovementState.RIGHT:
                pass
            elif metadata == MovementState.LEFT:
                pass
import RPi.GPIO as gpio
from enum import IntEnum
from logger import *
from gpiozero import Servo

class Pins(IntEnum):
    DC_0 = 16
    DC_1 = 18
    SERVO = 25

class Packet(IntEnum):
    SET_MODE = 1
    MOVE = 2

class RobotState(IntEnum):
    MANUAL = 1
    AUTONOMOUS = 2
    EXIT = 3

class MovementState(IntEnum):
    FORWARD = 0
    RIGHT = 3
    BREAKS = 1
    LEFT = 2
    

class manualDriver:
    def __init__(self, comunication_socket):
        self.communication_socket = comunication_socket
        self.logger = Logger().getLogger('Manual Driver', logging.DEBUG)
        gpio.setmode(gpio.BOARD)
        gpio.setup(Pins.DC_0, gpio.OUT)
        gpio.setup(Pins.DC_1, gpio.OUT)
        self.servo = Servo(Pins.SERVO)
    
    def apply_movement(self, forward_bit, breaks_bit, left_bit, right_bit):
        """
        if forward_bit >> MovementState.FORWARD:
            self.logger.debug('forward')
            gpio.output(Pins.DC_0, True)
            gpio.output(Pins.DC_1, True)
        elif breaks_bit >> MovementState.BREAKS:
            self.logger.debug('breaks')
            gpio.output(Pins.DC_0, False)
            gpio.output(Pins.DC_1, True)
        else:
            self.logger.debug('rest power')
            gpio.output(Pins.DC_0, False)
            gpio.output(Pins.DC_1, False)
            """
        if left_bit >> MovementState.LEFT:
            self.logger.debug('left')
            self.servo.min()
        elif right_bit >> MovementState.RIGHT:
            self.logger.debug('right')
            self.servo.max()
        else:
            self.logger.debug('rest steering')
            self.servo.mid()
            
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
        

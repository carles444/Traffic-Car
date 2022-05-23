import RPi.GPIO as gpio
from enum import IntEnum
from logger import *
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo, Device
import os
import threading

class Pins(IntEnum):
    DC_0 = 23
    DC_1 = 24
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
 
def init_igpiod(logger):
    # TODO: fer que s'executi al iniciar la raspberry
    """try:
        os.system('sudo killall pigpiod')
    except OSError:
        logger.warning('pigpiod not running')"""
    try:
        os.system('sudo pigpiod')
    except OSError:
        logger.warning("pigpiod already running")
    # avoiding jitter on servomotor
    Device.pin_factory = PiGPIOFactory()

class manualDriver:
    def __init__(self, comunication_socket):
        # globals
        self.ACCELERATION_RATE = 0.5
        self.ACCELERATION = 10
        self.SPEED = 0
        self.MAX_SPEED = 100
        
        # socket and logger
        self.communication_socket = comunication_socket
        self.logger = Logger().getLogger('Manual Driver', logging.DEBUG)
        init_igpiod(self.logger)
        
        # io management
        gpio.setmode(gpio.BCM)
        gpio.setup(Pins.DC_0, gpio.OUT)
        gpio.setup(Pins.DC_1, gpio.OUT)
        self.fw_pwm = gpio.PWM(Pins.DC_1, self.MAX_SPEED) # 100Hz
        self.fw_pwm.start(self.SPEED)
        self.servo = Servo(Pins.SERVO)
        self.last_action = None
        
        # accelerating timer
        self.fw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate)

    
    def accelerate(self):
        self.fw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate)
        self.fw_timer.start()
        if self.SPEED < self.MAX_SPEED:
            self.SPEED += self.ACCELERATION
            self.fw_pwm.ChangeDutyCycle(self.SPEED)
        else:
            self.fw_timer.cancel()
    def decelerate(self):
        self.fw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate)
        self.fw_timer.start()
        if self.SPEED > 0:
            self.SPEED -= self.ACCELERATION
            self.fw_pwm.ChangeDutyCycle(self.SPEED)
        else:
            self.fw_timer.cancel()
            gpio.output(Pins.DC_0, False)

            
    def apply_movement(self, forward_bit, breaks_bit, left_bit, right_bit):
        if forward_bit >> MovementState.FORWARD:
            self.logger.debug('forward')
            gpio.output(Pins.DC_0, True)
            #gpio.output(Pins.DC_1, True)
            if self.SPEED > 0:
                self.SPEED = 0
            self.accelerate()
            self.last_action = 'forward'
        elif breaks_bit >> MovementState.BREAKS:
            self.logger.debug('breaks')
            gpio.output(Pins.DC_0, False)
            if self.SPEED > 0:
                self.SPEED = -20
            self.accelerate()
            #gpio.output(Pins.DC_1, True)
            self.last_action = 'breaks'
        else:
            pin = True if self.last_action == 'forward_bit' else False
            self.fw_timer.cancel()
            self.logger.debug('rest power')
            gpio.output(Pins.DC_0, pin)
            #gpio.output(Pins.DC_1, False)
            self.decelerate()            
        
            
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
        

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


class Driver:
    def __init__(self):
        # globals
        self.ACCELERATION_RATE = 0.5
        self.ACCELERATION = 10
        self.speed = 0
        self.MAX_SPEED = 100
        
        # logger
        self.logger = Logger().getLogger('Manual Driver', logging.DEBUG)
        init_igpiod(self.logger)
        
        # io management
        gpio.setmode(gpio.BCM)
        gpio.setup(Pins.DC_0, gpio.OUT)
        gpio.setup(Pins.DC_1, gpio.OUT)
        self.pwm = gpio.PWM(Pins.DC_1, self.MAX_SPEED) # 100Hz
        self.pwm.start(self.speed)
        self.servo = Servo(Pins.SERVO)
        self.last_action = None
        
        # accelerating timer
        self.fw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate, [0])
        self.bw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate, [0])
        self.rst_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate, [0])

    def check_bit(self, value, bit):
        return (value & (1 << bit)) != 0
    
    def accelerate(self, acceleration):
        self.logger.debug(self.speed)
        if acceleration > 0:
            self.bw_timer.cancel()
            self.rst_timer.cancel()
            self.speed = min(self.MAX_SPEED, self.speed + acceleration)
            self.pwm.ChangeDutyCycle(abs(self.speed))
            if self.speed < self.MAX_SPEED:
                self.fw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate, [acceleration])
                self.fw_timer.start()
        else:
            self.fw_timer.cancel()
            self.rst_timer.cancel()
            self.speed = max(-self.MAX_SPEED, self.speed + acceleration)
            self.pwm.ChangeDutyCycle(abs(self.speed))
            if abs(self.speed) < self.MAX_SPEED:
                self.bw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate, [acceleration])
                self.bw_timer.start()
        gpio.output(Pins.DC_0, self.speed > 0)

    def breaks(self, acceleration):
        self.logger.debug(self.speed)
        self.fw_timer.cancel()
        self.bw_timer.cancel()
        acceleration = abs(acceleration)
        if self.speed > 0:
            self.speed = max(0, self.speed - acceleration)
            self.pwm.ChangeDutyCycle(self.speed)
        elif self.speed < 0:
            self.speed = min(0, self.speed + acceleration)
            self.pwm.ChangeDutyCycle(abs(self.speed))
        self.rst_timer = threading.Timer(self.ACCELERATION_RATE, self.breaks, [acceleration])
        self.rst_timer.start()

        if self.speed == 0:
            self.rst_timer.cancel()

            
    def apply_movement(self, metadata):
        if self.check_bit(metadata, MovementState.FORWARD):
            self.logger.debug('forward')
            # gpio.output(Pins.DC_1, True)
            self.accelerate(self.ACCELERATION)
        elif self.check_bit(metadata, MovementState.BREAKS):
            self.logger.debug('breaks')
            self.accelerate(-(self.ACCELERATION))
            # gpio.output(Pins.DC_1, True)
        else:
            self.logger.debug('rest power')
            # gpio.output(Pins.DC_0, False)
            self.breaks(int(self.ACCELERATION/2))
                 
        if self.check_bit(metadata, MovementState.LEFT):
            self.logger.debug('left')
            self.servo.min()
        elif self.check_bit(metadata, MovementState.RIGHT):
            self.logger.debug('right')
            self.servo.max()
        else:
            self.logger.debug('rest steering')
            self.servo.mid()
            
        self.last_action = metadata
            
